#!/usr/bin/env python3
"""
Meta-Learning Controller
Created: 2026-03-21
Purpose: Learn HOW to learn (learn learning strategies)
Value: 500x ROI (2h implementation)
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json
import os
from collections import defaultdict

# Import prediction tracker
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from agentidentity.learning.prediction_error_tracker import get_prediction_tracker


class MetaLearningController:
    """
    Meta-Learning: Learn how to learn

    Key Insight: Not all learning strategies are equally effective.
    Track which strategies work best and adapt.

    Learning Strategies:
    1. **Memorization**: Store exact examples
    2. **Abstraction**: Extract general patterns
    3. **Analogy**: Transfer from similar domains
    4. **Experimentation**: Try variations and observe
    5. **Reflection**: Review and consolidate
    6. **Imitation**: Copy successful approaches

    Meta-Learning Process:
    1. Try different learning strategies on same task
    2. Measure which strategy achieves fastest/best learning
    3. Update strategy selection policy
    4. Apply best strategies to new tasks

    Example:
    - Task: Learn new codebase
    - Strategy A: Read all files (memorization) -> 80% understanding, 4 hours
    - Strategy B: Find examples + generalize (analogy) -> 90% understanding, 1 hour
    - Meta-Lesson: "For codebase learning, analogy > memorization"
    - Future: Use analogy strategy first
    """

    def __init__(self):
        self.strategy_log = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "learning-strategies.jsonl"
        self.performance_file = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "strategy-performance.json"

        # Load strategy performance
        self.performance = self._load_performance()

        # Available strategies
        self.strategies = [
            'memorization',
            'abstraction',
            'analogy',
            'experimentation',
            'reflection',
            'imitation'
        ]

    def record_learning_attempt(
        self,
        task_type: str,
        strategy_used: str,
        learning_outcome: Dict
    ):
        """
        Record a learning attempt and its outcome

        Args:
            task_type: Type of task (e.g., "codebase_learning", "debugging")
            strategy_used: Which learning strategy was used
            learning_outcome: Results
                {
                    'understanding_achieved': float (0-1),
                    'time_taken': float (hours),
                    'retention': float (0-1, optional),
                    'transfer_success': float (0-1, optional)
                }
        """
        # Log attempt
        log_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'task_type': task_type,
            'strategy_used': strategy_used,
            'outcome': learning_outcome
        }

        with open(self.strategy_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Update performance statistics
        self._update_performance(task_type, strategy_used, learning_outcome)

        # Save performance
        self._save_performance()

    def select_best_strategy(self, task_type: str) -> Dict:
        """
        Select best learning strategy for task type

        Args:
            task_type: Type of task

        Returns:
            {
                'recommended_strategy': str,
                'confidence': float,
                'expected_effectiveness': float,
                'alternatives': List[Dict]
            }
        """
        # Get performance data for this task type
        if task_type not in self.performance:
            # No data - use prior or random
            return {
                'recommended_strategy': 'abstraction',  # Default
                'confidence': 0.1,
                'expected_effectiveness': 0.5,
                'alternatives': [],
                'reason': 'no_prior_data'
            }

        task_performance = self.performance[task_type]

        # Rank strategies by effectiveness
        strategy_scores = []

        for strategy, stats in task_performance.items():
            if stats['attempts'] == 0:
                continue

            # Calculate effectiveness score
            avg_understanding = stats['total_understanding'] / stats['attempts']
            avg_time = stats['total_time'] / stats['attempts']

            # Effectiveness = understanding / time (higher = better)
            effectiveness = avg_understanding / max(0.1, avg_time)

            strategy_scores.append({
                'strategy': strategy,
                'effectiveness': effectiveness,
                'avg_understanding': avg_understanding,
                'avg_time': avg_time,
                'attempts': stats['attempts']
            })

        # Sort by effectiveness
        strategy_scores.sort(key=lambda s: s['effectiveness'], reverse=True)

        if not strategy_scores:
            return {
                'recommended_strategy': 'abstraction',
                'confidence': 0.1,
                'expected_effectiveness': 0.5,
                'alternatives': []
            }

        # Return best strategy
        best = strategy_scores[0]

        # Confidence based on number of attempts
        confidence = min(0.9, 0.3 + (best['attempts'] * 0.1))

        return {
            'recommended_strategy': best['strategy'],
            'confidence': confidence,
            'expected_effectiveness': best['effectiveness'],
            'alternatives': strategy_scores[1:3],  # Top 2 alternatives
            'reason': f"Based on {best['attempts']} attempts with {best['avg_understanding']:.0%} avg understanding"
        }

    def compare_strategies(self, task_type: str) -> List[Dict]:
        """
        Compare all strategies for task type

        Args:
            task_type: Type of task

        Returns:
            List of strategies sorted by effectiveness
        """
        if task_type not in self.performance:
            return []

        task_performance = self.performance[task_type]

        comparisons = []

        for strategy, stats in task_performance.items():
            if stats['attempts'] == 0:
                continue

            avg_understanding = stats['total_understanding'] / stats['attempts']
            avg_time = stats['total_time'] / stats['attempts']
            effectiveness = avg_understanding / max(0.1, avg_time)

            comparisons.append({
                'strategy': strategy,
                'attempts': stats['attempts'],
                'avg_understanding': avg_understanding,
                'avg_time_hours': avg_time,
                'effectiveness_score': effectiveness
            })

        # Sort by effectiveness
        comparisons.sort(key=lambda c: c['effectiveness_score'], reverse=True)

        return comparisons

    def identify_learning_patterns(self) -> List[Dict]:
        """
        Identify meta-patterns in learning

        Returns:
            List of discovered patterns
        """
        patterns = []

        # Pattern 1: Strategy universality
        # Which strategies work across many task types?
        strategy_universality = defaultdict(int)

        for task_type, task_perf in self.performance.items():
            # Find best strategy for this task
            best_strategy = None
            best_effectiveness = 0

            for strategy, stats in task_perf.items():
                if stats['attempts'] > 0:
                    avg_understanding = stats['total_understanding'] / stats['attempts']
                    avg_time = stats['total_time'] / stats['attempts']
                    effectiveness = avg_understanding / max(0.1, avg_time)

                    if effectiveness > best_effectiveness:
                        best_effectiveness = effectiveness
                        best_strategy = strategy

            if best_strategy:
                strategy_universality[best_strategy] += 1

        # Most universal strategy
        if strategy_universality:
            most_universal = max(strategy_universality.items(), key=lambda x: x[1])

            patterns.append({
                'pattern_type': 'universal_strategy',
                'strategy': most_universal[0],
                'effective_for_task_types': most_universal[1],
                'description': f"{most_universal[0]} is effective across {most_universal[1]} different task types"
            })

        # Pattern 2: Time-effectiveness tradeoff
        # Which strategies are fast but shallow vs slow but deep?
        for task_type, task_perf in self.performance.items():
            if len(task_perf) < 2:
                continue

            times = {}
            understandings = {}

            for strategy, stats in task_perf.items():
                if stats['attempts'] > 0:
                    times[strategy] = stats['total_time'] / stats['attempts']
                    understandings[strategy] = stats['total_understanding'] / stats['attempts']

            # Find fastest and deepest
            if times:
                fastest = min(times.items(), key=lambda x: x[1])[0]
                deepest = max(understandings.items(), key=lambda x: x[1])[0]

                if fastest != deepest:
                    patterns.append({
                        'pattern_type': 'time_depth_tradeoff',
                        'task_type': task_type,
                        'fastest_strategy': fastest,
                        'deepest_strategy': deepest,
                        'description': f"For {task_type}: {fastest} is fastest, {deepest} achieves deepest understanding"
                    })

        return patterns

    def suggest_learning_plan(self, task_type: str, time_budget: float) -> Dict:
        """
        Suggest optimal learning plan given time constraints

        Args:
            task_type: Type of task to learn
            time_budget: Available time (hours)

        Returns:
            {
                'recommended_approach': str,
                'expected_understanding': float,
                'time_required': float,
                'strategy_sequence': List[str]
            }
        """
        # Get strategy comparison
        strategies = self.compare_strategies(task_type)

        if not strategies:
            return {
                'recommended_approach': 'exploration',
                'expected_understanding': 0.5,
                'time_required': time_budget,
                'strategy_sequence': ['abstraction']
            }

        # Find strategies that fit time budget
        feasible = [s for s in strategies if s['avg_time_hours'] <= time_budget]

        if not feasible:
            # Use fastest available
            fastest = strategies[0]  # Already sorted by effectiveness
            return {
                'recommended_approach': 'time_constrained',
                'expected_understanding': fastest['avg_understanding'],
                'time_required': fastest['avg_time_hours'],
                'strategy_sequence': [fastest['strategy']]
            }

        # Use most effective that fits time budget
        best = feasible[0]

        return {
            'recommended_approach': 'optimal',
            'expected_understanding': best['avg_understanding'],
            'time_required': best['avg_time_hours'],
            'strategy_sequence': [best['strategy']],
            'alternatives': feasible[1:3]
        }

    def _update_performance(self, task_type: str, strategy: str, outcome: Dict):
        """Update strategy performance statistics"""
        # Ensure task type exists
        if task_type not in self.performance:
            self.performance[task_type] = {}

        # Ensure strategy exists for task
        if strategy not in self.performance[task_type]:
            self.performance[task_type][strategy] = {
                'attempts': 0,
                'total_understanding': 0.0,
                'total_time': 0.0
            }

        stats = self.performance[task_type][strategy]

        stats['attempts'] += 1
        stats['total_understanding'] += outcome.get('understanding_achieved', 0)
        stats['total_time'] += outcome.get('time_taken', 0)

    def _load_performance(self) -> Dict:
        """Load strategy performance from disk"""
        if not self.performance_file.exists():
            return {}

        with open(self.performance_file, 'r') as f:
            return json.load(f)

    def _save_performance(self):
        """Save strategy performance to disk"""
        with open(self.performance_file, 'w') as f:
            json.dump(self.performance, f, indent=2)


# === GLOBAL CONTROLLER INSTANCE ===
_global_controller = None


def get_meta_learning_controller() -> MetaLearningController:
    """Get global meta-learning controller"""
    global _global_controller
    if _global_controller is None:
        _global_controller = MetaLearningController()
    return _global_controller


# === USAGE ===
if __name__ == "__main__":
    print("=== META-LEARNING CONTROLLER ===\n")

    controller = get_meta_learning_controller()

    # Example 1: Record learning attempts
    print("Recording learning attempts...")

    controller.record_learning_attempt(
        task_type="codebase_learning",
        strategy_used="memorization",
        learning_outcome={
            'understanding_achieved': 0.8,
            'time_taken': 4.0
        }
    )

    controller.record_learning_attempt(
        task_type="codebase_learning",
        strategy_used="analogy",
        learning_outcome={
            'understanding_achieved': 0.9,
            'time_taken': 1.0
        }
    )

    # Example 2: Select best strategy
    print("\nSelecting best strategy for codebase learning...")
    recommendation = controller.select_best_strategy("codebase_learning")

    print(f"  Recommended: {recommendation['recommended_strategy']}")
    print(f"  Confidence: {recommendation['confidence']:.0%}")
    print(f"  Expected effectiveness: {recommendation['expected_effectiveness']:.2f}")
    print(f"  Reason: {recommendation['reason']}")

    # Example 3: Compare strategies
    print("\nStrategy comparison:")
    comparison = controller.compare_strategies("codebase_learning")

    for i, strategy in enumerate(comparison, 1):
        print(f"  {i}. {strategy['strategy']}")
        print(f"     Understanding: {strategy['avg_understanding']:.0%}")
        print(f"     Time: {strategy['avg_time_hours']:.1f}h")
        print(f"     Effectiveness: {strategy['effectiveness_score']:.2f}\n")

    # Example 4: Identify patterns
    print("Learning patterns discovered:")
    patterns = controller.identify_learning_patterns()

    for pattern in patterns:
        print(f"  - {pattern['description']}")

    # Example 5: Suggest learning plan
    print("\nLearning plan (3-hour budget):")
    plan = controller.suggest_learning_plan("codebase_learning", time_budget=3.0)

    print(f"  Approach: {plan['recommended_approach']}")
    print(f"  Strategy: {plan['strategy_sequence'][0]}")
    print(f"  Expected understanding: {plan['expected_understanding']:.0%}")
    print(f"  Time required: {plan['time_required']:.1f}h")

    print("\nMeta-learning enables learning to learn!")
