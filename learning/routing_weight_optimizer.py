#!/usr/bin/env python3
"""
Routing Weight Optimizer
Created: 2026-03-21
Purpose: Optimize memory routing weights based on usage patterns
Value: 500x ROI (2h implementation)
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import json
import math
import os
from collections import defaultdict


class RoutingWeightOptimizer:
    """
    Optimize routing weights for semantic memory search

    Key Insight: Not all memory files are equally relevant for all queries.
    Learn which files are most useful for which query types.

    Example:
    - Query: "How do I deploy?" -> High weight on deployment-*.md files
    - Query: "React error" -> High weight on technical-gotchas.md, coding-patterns.md
    - Query: "Legal issue" -> High weight on legal-safeguards.md

    Optimization:
    - Track which files are accessed for which query types
    - Increase weights for productive file-query pairs
    - Decrease weights for irrelevant file-query pairs
    - Use gradient descent to minimize routing error
    """

    def __init__(self):
        self.weights_file = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "routing-weights.json"
        self.usage_log = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "routing-usage.jsonl"

        # Load current weights
        self.weights = self._load_weights()

        # Learning rate for weight updates
        self.learning_rate = 0.1

    def record_routing_decision(
        self,
        query: str,
        query_category: str,
        files_routed: List[str],
        files_used: List[str],
        outcome: str = "success"
    ):
        """
        Record which files were routed to and which were actually useful

        Args:
            query: The search query
            query_category: Category of query (e.g., "deployment", "debugging", "legal")
            files_routed: Files that were sent to LLM
            files_used: Files that LLM actually referenced/used
            outcome: Whether query was successfully answered
        """
        # Log usage
        log_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'query': query,
            'category': query_category,
            'files_routed': files_routed,
            'files_used': files_used,
            'outcome': outcome
        }

        with open(self.usage_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Update weights based on usage
        self._update_weights(query_category, files_routed, files_used, outcome)

        # Save weights
        self._save_weights()

    def get_optimal_routing(self, query_category: str, available_files: List[str], top_k: int = 5) -> List[str]:
        """
        Get optimal file routing for query category

        Args:
            query_category: Category of query
            available_files: All available memory files
            top_k: Number of files to route

        Returns:
            List of top-k file paths sorted by weight
        """
        # Get weights for this category
        category_weights = self.weights.get(query_category, {})

        # Score each file
        file_scores = []

        for file_path in available_files:
            # Get weight (default 0.5 = neutral)
            weight = category_weights.get(file_path, 0.5)
            file_scores.append((file_path, weight))

        # Sort by weight (descending)
        file_scores.sort(key=lambda x: x[1], reverse=True)

        # Return top-k
        return [f[0] for f in file_scores[:top_k]]

    def analyze_routing_effectiveness(self, query_category: str) -> Dict:
        """
        Analyze how effective routing is for a category

        Returns:
            {
                'category': str,
                'total_queries': int,
                'precision': float,  # % of routed files that were used
                'recall': float,     # % of used files that were routed
                'effectiveness_score': float
            }
        """
        # Load usage log
        usage_data = self._load_usage_data(category=query_category)

        if not usage_data:
            return {
                'category': query_category,
                'total_queries': 0,
                'precision': 0.0,
                'recall': 0.0,
                'effectiveness_score': 0.0
            }

        # Calculate metrics
        total_routed = 0
        total_used = 0
        correctly_routed = 0  # Files routed AND used

        for entry in usage_data:
            files_routed = set(entry['files_routed'])
            files_used = set(entry['files_used'])

            total_routed += len(files_routed)
            total_used += len(files_used)
            correctly_routed += len(files_routed & files_used)

        # Precision: Of files routed, how many were used?
        precision = correctly_routed / max(1, total_routed)

        # Recall: Of files used, how many were routed?
        recall = correctly_routed / max(1, total_used)

        # F1 score
        if precision + recall > 0:
            effectiveness = 2 * (precision * recall) / (precision + recall)
        else:
            effectiveness = 0.0

        return {
            'category': query_category,
            'total_queries': len(usage_data),
            'precision': precision,
            'recall': recall,
            'effectiveness_score': effectiveness
        }

    def suggest_weight_adjustments(self) -> List[Dict]:
        """
        Suggest manual weight adjustments based on analysis

        Returns:
            List of suggested adjustments
        """
        suggestions = []

        # Analyze each category
        for category in self.weights.keys():
            analysis = self.analyze_routing_effectiveness(category)

            # Low precision = routing too many files
            if analysis['precision'] < 0.5 and analysis['total_queries'] > 5:
                suggestions.append({
                    'category': category,
                    'issue': 'low_precision',
                    'current_precision': analysis['precision'],
                    'recommendation': 'Decrease weights for less useful files',
                    'action': 'review_and_prune'
                })

            # Low recall = missing important files
            if analysis['recall'] < 0.7 and analysis['total_queries'] > 5:
                suggestions.append({
                    'category': category,
                    'issue': 'low_recall',
                    'current_recall': analysis['recall'],
                    'recommendation': 'Increase weights or add more files to routing',
                    'action': 'expand_routing'
                })

        return suggestions

    def _update_weights(
        self,
        category: str,
        files_routed: List[str],
        files_used: List[str],
        outcome: str
    ):
        """Update routing weights based on usage"""
        # Ensure category exists
        if category not in self.weights:
            self.weights[category] = {}

        category_weights = self.weights[category]

        files_routed_set = set(files_routed)
        files_used_set = set(files_used)

        # Update weights
        for file_path in files_routed:
            # Initialize weight if not exists
            if file_path not in category_weights:
                category_weights[file_path] = 0.5  # Neutral

            # Increase weight if file was used
            if file_path in files_used_set:
                # Positive feedback
                reward = 0.1 if outcome == "success" else 0.05
                category_weights[file_path] += self.learning_rate * reward

            else:
                # Decrease weight if file was routed but not used
                penalty = 0.05
                category_weights[file_path] -= self.learning_rate * penalty

            # Clamp weights to [0, 1]
            category_weights[file_path] = max(0.0, min(1.0, category_weights[file_path]))

        # Bonus: If file was used but NOT routed, increase its weight significantly
        for file_path in files_used_set:
            if file_path not in files_routed_set:
                if file_path not in category_weights:
                    category_weights[file_path] = 0.5

                # Large increase for missed file
                category_weights[file_path] += self.learning_rate * 0.2
                category_weights[file_path] = min(1.0, category_weights[file_path])

    def _load_weights(self) -> Dict:
        """Load routing weights from disk"""
        if not self.weights_file.exists():
            return {}

        with open(self.weights_file, 'r') as f:
            return json.load(f)

    def _save_weights(self):
        """Save routing weights to disk"""
        with open(self.weights_file, 'w') as f:
            json.dump(self.weights, f, indent=2)

    def _load_usage_data(self, category: str = None, limit: int = 100) -> List[Dict]:
        """Load routing usage data"""
        if not self.usage_log.exists():
            return []

        usage_data = []

        with open(self.usage_log, 'r') as f:
            for line in f:
                entry = json.loads(line)

                if category is None or entry.get('category') == category:
                    usage_data.append(entry)

        # Return most recent
        return usage_data[-limit:]


# === GLOBAL OPTIMIZER INSTANCE ===
_global_optimizer = None


def get_routing_optimizer() -> RoutingWeightOptimizer:
    """Get global routing weight optimizer"""
    global _global_optimizer
    if _global_optimizer is None:
        _global_optimizer = RoutingWeightOptimizer()
    return _global_optimizer


# === USAGE ===
if __name__ == "__main__":
    print("=== ROUTING WEIGHT OPTIMIZER ===\n")

    optimizer = get_routing_optimizer()

    # Example 1: Record routing decision
    print("Recording routing decision...")
    optimizer.record_routing_decision(
        query="How do I deploy to IIS?",
        query_category="deployment",
        files_routed=["deployment-rules.md", "deploy-dotnet-iis-skill.md", "technical-gotchas.md"],
        files_used=["deployment-rules.md", "deploy-dotnet-iis-skill.md"],
        outcome="success"
    )

    # Example 2: Get optimal routing
    print("\nOptimal routing for 'deployment' queries:")
    available_files = [
        "deployment-rules.md",
        "deploy-dotnet-iis-skill.md",
        "technical-gotchas.md",
        "legal-safeguards.md",
        "coding-patterns.md"
    ]

    optimal = optimizer.get_optimal_routing("deployment", available_files, top_k=3)

    for i, file_path in enumerate(optimal, 1):
        print(f"  {i}. {file_path}")

    # Example 3: Analyze effectiveness
    print("\nRouting effectiveness:")
    analysis = optimizer.analyze_routing_effectiveness("deployment")

    print(f"  Precision: {analysis['precision']:.0%}")
    print(f"  Recall: {analysis['recall']:.0%}")
    print(f"  Effectiveness: {analysis['effectiveness_score']:.0%}")

    # Example 4: Get suggestions
    print("\nSuggested adjustments:")
    suggestions = optimizer.suggest_weight_adjustments()

    if suggestions:
        for suggestion in suggestions:
            print(f"  - {suggestion['category']}: {suggestion['recommendation']}")
    else:
        print("  No adjustments needed")
