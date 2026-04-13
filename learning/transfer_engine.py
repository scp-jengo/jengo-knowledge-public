#!/usr/bin/env python3
"""
Transfer Learning Engine
Enable explicit transfer of patterns from domain A to domain B

Created: 2026-03-21
Purpose: Cross-domain knowledge transfer (AGI Criterion #9)
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict

class TransferLearningEngine:
    def __init__(self):
        self.patterns_file = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "transferable-patterns.json"
        self.transfer_log = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "transfer-history.jsonl"
        self.patterns = self._load_patterns()

    def _load_patterns(self) -> Dict:
        """Load existing transferable patterns"""
        if not self.patterns_file.exists():
            return {"patterns": []}

        with open(self.patterns_file, 'r') as f:
            return json.load(f)

    def extract_abstract_pattern(self, concrete_situation: Dict) -> Dict:
        """
        Extract abstract pattern from concrete situation

        Args:
            concrete_situation: {
                "domain": "git",
                "problem": "merge conflict",
                "solution": "merge develop, resolve conflicts, test",
                "structure": ["prepare", "execute", "validate"]
            }

        Returns:
            Abstract pattern applicable across domains
        """
        abstract = {
            "pattern_id": f"pattern_{len(self.patterns['patterns'])}",
            "original_domain": concrete_situation.get("domain"),
            "abstract_problem_type": self._abstract_problem_type(concrete_situation["problem"]),
            "abstract_solution_structure": concrete_situation.get("structure", []),
            "transferability_score": self._estimate_transferability(concrete_situation),
            "created": datetime.utcnow().isoformat() + "Z",
            "concrete_example": concrete_situation
        }

        return abstract

    def _abstract_problem_type(self, concrete_problem: str) -> str:
        """Abstract the problem type"""
        problem_lower = concrete_problem.lower()

        if "conflict" in problem_lower:
            return "conflict_resolution"
        elif "error" in problem_lower or "fail" in problem_lower:
            return "error_recovery"
        elif "optimiz" in problem_lower or "improv" in problem_lower:
            return "optimization"
        elif "integrat" in problem_lower:
            return "integration"
        elif "validat" in problem_lower or "verif" in problem_lower:
            return "validation"
        else:
            return "generic_problem_solving"

    def _estimate_transferability(self, situation: Dict) -> float:
        """Estimate how transferable this pattern is (0-1)"""
        # Heuristics for transferability
        score = 0.5  # Base score

        # Patterns with clear structure transfer better
        if "structure" in situation and len(situation["structure"]) > 2:
            score += 0.2

        # Generic problem types transfer better
        if situation.get("domain") in ["logic", "algorithm", "workflow"]:
            score += 0.2

        # Domain-specific patterns transfer less
        if situation.get("domain") in ["hardware", "biology", "physics"]:
            score -= 0.2

        return min(1.0, max(0.0, score))

    def find_analogous_patterns(self, target_situation: Dict, threshold: float = 0.6) -> List[Dict]:
        """
        Find patterns from other domains that might apply to target situation

        Args:
            target_situation: Current problem in domain X
            threshold: Minimum structural similarity (0-1)

        Returns:
            List of analogous patterns sorted by similarity
        """
        target_problem_type = self._abstract_problem_type(target_situation.get("problem", ""))

        analogous = []

        for pattern in self.patterns.get("patterns", []):
            # Skip patterns from same domain (not transfer learning)
            if pattern.get("original_domain") == target_situation.get("domain"):
                continue

            # Check if problem types match
            if pattern.get("abstract_problem_type") == target_problem_type:
                similarity = self._calculate_structural_similarity(pattern, target_situation)

                if similarity >= threshold:
                    analogous.append({
                        **pattern,
                        "similarity_score": similarity,
                        "transfer_potential": similarity * pattern.get("transferability_score", 0.5)
                    })

        # Sort by transfer potential
        analogous.sort(key=lambda x: x["transfer_potential"], reverse=True)

        return analogous

    def _calculate_structural_similarity(self, pattern: Dict, situation: Dict) -> float:
        """Calculate structural similarity between pattern and situation"""
        pattern_structure = pattern.get("abstract_solution_structure", [])
        situation_structure = situation.get("structure", [])

        if not pattern_structure or not situation_structure:
            return 0.5  # Unknown

        # Simple overlap-based similarity
        overlap = len(set(pattern_structure).intersection(set(situation_structure)))
        union = len(set(pattern_structure).union(set(situation_structure)))

        return overlap / max(1, union)

    def transfer_pattern(self, source_pattern: Dict, target_domain: str, target_problem: str) -> Dict:
        """
        Adapt a pattern from source domain to target domain

        Args:
            source_pattern: Pattern from domain A
            target_domain: Domain B where pattern will be applied
            target_problem: Specific problem in domain B

        Returns:
            Adapted pattern for target domain
        """
        adapted = {
            "source_pattern_id": source_pattern.get("pattern_id"),
            "source_domain": source_pattern.get("original_domain"),
            "target_domain": target_domain,
            "target_problem": target_problem,
            "adapted_solution_structure": source_pattern.get("abstract_solution_structure", []),
            "adaptation_notes": self._generate_adaptation_notes(source_pattern, target_domain),
            "confidence": source_pattern.get("transferability_score", 0.5),
            "transferred_at": datetime.utcnow().isoformat() + "Z"
        }

        # Log transfer
        self._log_transfer(adapted)

        return adapted

    def _generate_adaptation_notes(self, pattern: Dict, target_domain: str) -> str:
        """Generate notes on how to adapt pattern to target domain"""
        source_domain = pattern.get("original_domain", "unknown")
        problem_type = pattern.get("abstract_problem_type", "generic")

        notes = f"Pattern from {source_domain} (problem type: {problem_type}) transferred to {target_domain}. "
        notes += f"Follow the abstract structure: {' -> '.join(pattern.get('abstract_solution_structure', []))}. "
        notes += "Adapt domain-specific details while preserving core logic."

        return notes

    def _log_transfer(self, transfer: Dict):
        """Log pattern transfer event"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": "pattern_transfer",
            **transfer
        }

        with open(self.transfer_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def add_pattern(self, pattern: Dict):
        """Add a new transferable pattern"""
        abstract_pattern = self.extract_abstract_pattern(pattern)
        self.patterns["patterns"].append(abstract_pattern)

        # Save updated patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)

    def get_transfer_statistics(self) -> Dict:
        """Get statistics on pattern transfers"""
        if not self.transfer_log.exists():
            return {"total_transfers": 0}

        transfers = []
        with open(self.transfer_log, 'r') as f:
            for line in f:
                transfers.append(json.loads(line))

        # Count by domain
        source_domains = defaultdict(int)
        target_domains = defaultdict(int)

        for t in transfers:
            source_domains[t.get("source_domain", "unknown")] += 1
            target_domains[t.get("target_domain", "unknown")] += 1

        return {
            "total_transfers": len(transfers),
            "unique_patterns_transferred": len(set(t.get("source_pattern_id") for t in transfers)),
            "most_transferred_from": max(source_domains.items(), key=lambda x: x[1])[0] if source_domains else None,
            "most_transferred_to": max(target_domains.items(), key=lambda x: x[1])[0] if target_domains else None
        }


# === USAGE ===
if __name__ == "__main__":
    engine = TransferLearningEngine()

    print("=== TRANSFER LEARNING ENGINE ===\n")

    # Example 1: Extract abstract pattern from concrete situation
    print("Example 1: Extract Abstract Pattern")

    git_conflict_pattern = {
        "domain": "git",
        "problem": "merge conflict on feature branch",
        "solution": "merge develop into branch, resolve conflicts, run tests, verify build",
        "structure": ["prepare_base", "merge", "resolve_conflicts", "validate", "commit"]
    }

    abstract = engine.extract_abstract_pattern(git_conflict_pattern)
    print(f"Abstract problem type: {abstract['abstract_problem_type']}")
    print(f"Transferability score: {abstract['transferability_score']:.0%}")
    print(f"Structure: {' -> '.join(abstract['abstract_solution_structure'])}\n")

    # Add pattern to library
    engine.add_pattern(git_conflict_pattern)

    # Example 2: Add another pattern (API version conflict)
    api_conflict_pattern = {
        "domain": "api_integration",
        "problem": "api version conflict between services",
        "solution": "upgrade dependency to latest, resolve breaking changes, run integration tests, deploy",
        "structure": ["prepare_base", "merge", "resolve_conflicts", "validate", "commit"]
    }

    engine.add_pattern(api_conflict_pattern)

    # Example 3: Find analogous patterns for new problem
    print("Example 2: Find Analogous Patterns")

    database_migration_problem = {
        "domain": "database",
        "problem": "schema migration conflict",
        "structure": ["prepare_base", "apply_changes", "resolve_issues", "validate"]
    }

    analogous = engine.find_analogous_patterns(database_migration_problem, threshold=0.5)

    print(f"Found {len(analogous)} analogous patterns:")
    for pattern in analogous:
        print(f"  From {pattern['original_domain']}: {pattern['abstract_problem_type']}")
        print(f"    Similarity: {pattern['similarity_score']:.0%}, Transfer potential: {pattern['transfer_potential']:.0%}")
    print()

    # Example 4: Transfer pattern to new domain
    if analogous:
        print("Example 3: Transfer Pattern to New Domain")

        transferred = engine.transfer_pattern(
            source_pattern=analogous[0],
            target_domain="database",
            target_problem="schema migration conflict"
        )

        print(f"Transferred from: {transferred['source_domain']}")
        print(f"To: {transferred['target_domain']}")
        print(f"Adapted structure: {' -> '.join(transferred['adapted_solution_structure'])}")
        print(f"Confidence: {transferred['confidence']:.0%}")
        print(f"Notes: {transferred['adaptation_notes']}\n")

    # Example 5: Transfer statistics
    print("Example 4: Transfer Statistics")
    stats = engine.get_transfer_statistics()
    print(f"Total transfers: {stats['total_transfers']}")
    print(f"Unique patterns: {stats['unique_patterns_transferred']}")

    print("\nTransfer learning enables cross-domain knowledge application")
