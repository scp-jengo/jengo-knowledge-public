#!/usr/bin/env python3
"""
Pseudo-Plasticity System
Learning within frozen LLM constraints via routing weight updates

Created: 2026-03-21
Purpose: Continuous learning despite frozen transformer weights
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

class PseudoPlasticityEngine:
    """Update routing weights, pattern priorities, thresholds (not LLM weights)"""

    def __init__(self):
        self.routing_weights_file = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "routing-weights.json"
        self.experience_replay_file = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "experience-replay.jsonl"
        self.learning_log = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "lifelong-learning.jsonl"
        self.weights = self._load_routing_weights()

    def _load_routing_weights(self) -> Dict:
        """Load routing weights (pattern priorities)"""
        if not self.routing_weights_file.exists():
            return {
                "pattern_priorities": {},
                "skill_routing": {},
                "decision_thresholds": {}
            }

        with open(self.routing_weights_file, 'r') as f:
            return json.load(f)

    def record_experience(self, pattern_id: str, success: bool, context: Dict = None):
        """Record experience for later replay and weight update"""
        experience = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pattern_id": pattern_id,
            "success": success,
            "context": context or {}
        }

        with open(self.experience_replay_file, 'a') as f:
            f.write(json.dumps(experience) + "\n")

        # Update weight immediately
        self._update_pattern_weight(pattern_id, success)

    def _update_pattern_weight(self, pattern_id: str, success: bool):
        """Update routing weight based on outcome"""
        if pattern_id not in self.weights["pattern_priorities"]:
            self.weights["pattern_priorities"][pattern_id] = {
                "priority": 0.5,  # Neutral
                "success_count": 0,
                "failure_count": 0,
                "total_uses": 0
            }

        pattern = self.weights["pattern_priorities"][pattern_id]
        pattern["total_uses"] += 1

        if success:
            pattern["success_count"] += 1
            # Increase priority (learning rate = 0.05)
            pattern["priority"] = min(1.0, pattern["priority"] + 0.05)
        else:
            pattern["failure_count"] += 1
            # Decrease priority
            pattern["priority"] = max(0.0, pattern["priority"] - 0.05)

        self._save_weights()

    def replay_experiences(self, last_n: int = 100):
        """
        Experience replay: Review past experiences and adjust weights

        This is analogous to REM sleep consolidation but for procedural learning
        """
        if not self.experience_replay_file.exists():
            return

        experiences = []
        with open(self.experience_replay_file, 'r') as f:
            for line in f:
                experiences.append(json.loads(line))

        # Replay last N experiences
        recent = experiences[-last_n:] if len(experiences) > last_n else experiences

        # Aggregate by pattern
        pattern_stats = defaultdict(lambda: {"success": 0, "failure": 0})

        for exp in recent:
            pattern_id = exp["pattern_id"]
            if exp["success"]:
                pattern_stats[pattern_id]["success"] += 1
            else:
                pattern_stats[pattern_id]["failure"] += 1

        # Adjust weights based on aggregate performance
        for pattern_id, stats in pattern_stats.items():
            total = stats["success"] + stats["failure"]
            success_rate = stats["success"] / total

            if pattern_id not in self.weights["pattern_priorities"]:
                self.weights["pattern_priorities"][pattern_id] = {
                    "priority": 0.5,
                    "success_count": 0,
                    "failure_count": 0,
                    "total_uses": 0
                }

            # Set priority based on success rate
            self.weights["pattern_priorities"][pattern_id]["priority"] = success_rate

        self._save_weights()

        return {
            "experiences_replayed": len(recent),
            "patterns_updated": len(pattern_stats)
        }

    def get_pattern_priority(self, pattern_id: str) -> float:
        """Get current routing priority for pattern"""
        if pattern_id not in self.weights["pattern_priorities"]:
            return 0.5  # Neutral

        return self.weights["pattern_priorities"][pattern_id]["priority"]

    def get_learning_summary(self) -> Dict:
        """Get summary of all learned patterns"""
        summary = {
            "total_patterns": len(self.weights["pattern_priorities"]),
            "high_priority_patterns": [],
            "low_priority_patterns": [],
            "most_used_pattern": None
        }

        for pattern_id, data in self.weights["pattern_priorities"].items():
            if data["priority"] > 0.7:
                summary["high_priority_patterns"].append(pattern_id)
            elif data["priority"] < 0.3:
                summary["low_priority_patterns"].append(pattern_id)

        # Find most used
        if self.weights["pattern_priorities"]:
            most_used = max(
                self.weights["pattern_priorities"].items(),
                key=lambda x: x[1]["total_uses"]
            )
            summary["most_used_pattern"] = most_used[0]

        return summary

    def _save_weights(self):
        """Save routing weights"""
        self.weights["last_updated"] = datetime.utcnow().isoformat() + "Z"

        with open(self.routing_weights_file, 'w') as f:
            json.dump(self.weights, f, indent=2)

    def log_learning_event(self, pattern_id: str, learning_type: str, description: str):
        """Log learning event to lifelong learning log"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pattern_id": pattern_id,
            "learning_type": learning_type,
            "description": description,
            "priority_after": self.get_pattern_priority(pattern_id)
        }

        with open(self.learning_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")


# === USAGE ===
if __name__ == "__main__":
    engine = PseudoPlasticityEngine()

    print("=== PSEUDO-PLASTICITY SYSTEM ===\n")

    # Example: Learn from pattern successes/failures
    print("Learning from experiences:")

    # Pattern 167: Rapid Quality Gate Implementation (successful)
    for _ in range(10):
        engine.record_experience("pattern_167_quality_gates", success=True)

    # Pattern 999: Hypothetical failed pattern
    for _ in range(3):
        engine.record_experience("pattern_999_failed_approach", success=False)

    # Check learned priorities
    priority_167 = engine.get_pattern_priority("pattern_167_quality_gates")
    priority_999 = engine.get_pattern_priority("pattern_999_failed_approach")

    print(f"Pattern 167 priority: {priority_167:.2f} (high - successful)")
    print(f"Pattern 999 priority: {priority_999:.2f} (low - failed)\n")

    # Experience replay
    print("Running experience replay...")
    result = engine.replay_experiences(last_n=50)
    print(f"  Experiences replayed: {result['experiences_replayed']}")
    print(f"  Patterns updated: {result['patterns_updated']}\n")

    # Learning summary
    summary = engine.get_learning_summary()
    print(f"Total patterns learned: {summary['total_patterns']}")
    print(f"High priority patterns: {len(summary['high_priority_patterns'])}")
    print(f"Low priority patterns: {len(summary['low_priority_patterns'])}")
    print(f"Most used: {summary['most_used_pattern']}")

    print("\nPseudo-plasticity enables learning despite frozen LLM weights")
