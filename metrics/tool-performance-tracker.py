#!/usr/bin/env python3
"""
Tool Performance Tracker - Week 1 Day 2-3 Implementation
Tracks tool/skill usage statistics from skills-usage-log.jsonl
Calculates frequency, duration, success rate, and token cost
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any
import statistics


class ToolPerformanceTracker:
    """Tracks and analyzes tool/skill performance metrics"""

    def __init__(self, log_path: str = None):
        if log_path is None:
            log_path = str(Path(os.environ.get("JENGO_STATE_PATH", ".")) / "skills-usage-log.jsonl")
        self.log_path = Path(log_path)
        self.metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.load_data()

    def load_data(self):
        """Load skills usage data from JSONL file"""
        if not self.log_path.exists():
            print(f"Warning: Log file not found: {self.log_path}")
            return

        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                    skill_name = entry.get('skill', 'unknown')
                    self.metrics[skill_name].append(entry)
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON line: {e}")
                    continue

    def calculate_success_rate(self, skill: str) -> float:
        """Calculate success rate for a skill (percentage)"""
        if not self.metrics[skill]:
            return 0.0

        total = len(self.metrics[skill])
        successes = sum(1 for entry in self.metrics[skill] if entry.get('outcome') == 'success')
        return (successes / total) * 100

    def calculate_avg_duration(self, skill: str) -> float:
        """Calculate average duration in milliseconds"""
        if not self.metrics[skill]:
            return 0.0

        durations = [entry.get('duration_ms', 0) for entry in self.metrics[skill]]
        return statistics.mean(durations) if durations else 0.0

    def calculate_call_frequency(self, skill: str, days: int = 7) -> int:
        """Calculate calls per time period (default: 7 days)"""
        return len(self.metrics[skill])

    def estimate_token_cost(self, skill: str) -> int:
        """Estimate token cost based on duration (rough heuristic)"""
        avg_duration = self.calculate_avg_duration(skill)
        # Rough estimate: 100 tokens per 10 seconds (10,000ms)
        return int((avg_duration / 10000) * 100)

    def get_high_performers(self, min_success_rate: float = 70.0) -> List[Dict[str, Any]]:
        """Get tools with >70% success rate"""
        high_performers = []

        for skill, entries in self.metrics.items():
            success_rate = self.calculate_success_rate(skill)
            if success_rate >= min_success_rate:
                high_performers.append({
                    'skill': skill,
                    'success_rate': success_rate,
                    'call_count': len(entries),
                    'avg_duration_ms': self.calculate_avg_duration(skill)
                })

        return sorted(high_performers, key=lambda x: x['success_rate'], reverse=True)

    def get_underutilized_tools(self, max_calls: int = 5) -> List[Dict[str, Any]]:
        """Get tools called <5x in the tracked period"""
        underutilized = []

        for skill, entries in self.metrics.items():
            if len(entries) < max_calls:
                underutilized.append({
                    'skill': skill,
                    'call_count': len(entries),
                    'success_rate': self.calculate_success_rate(skill),
                    'avg_duration_ms': self.calculate_avg_duration(skill)
                })

        return sorted(underutilized, key=lambda x: x['call_count'])

    def get_expensive_tools(self, min_tokens: int = 1000) -> List[Dict[str, Any]]:
        """Get tools with >1000 tokens/call (estimated)"""
        expensive = []

        for skill, entries in self.metrics.items():
            estimated_tokens = self.estimate_token_cost(skill)
            if estimated_tokens >= min_tokens:
                expensive.append({
                    'skill': skill,
                    'estimated_tokens': estimated_tokens,
                    'call_count': len(entries),
                    'avg_duration_ms': self.calculate_avg_duration(skill)
                })

        return sorted(expensive, key=lambda x: x['estimated_tokens'], reverse=True)

    def generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        total_calls = sum(len(entries) for entries in self.metrics.values())
        total_skills = len(self.metrics)

        success_rates = [self.calculate_success_rate(skill) for skill in self.metrics.keys()]
        avg_success_rate = statistics.mean(success_rates) if success_rates else 0.0

        return {
            'total_skills_tracked': total_skills,
            'total_calls': total_calls,
            'avg_success_rate': avg_success_rate,
            'high_performers': self.get_high_performers(),
            'underutilized': self.get_underutilized_tools(),
            'expensive_tools': self.get_expensive_tools(),
            'timestamp': datetime.now().isoformat()
        }

    def export_json(self, output_path: str = None):
        """Export metrics to JSON file"""
        if output_path is None:
            output_path = str(Path(__file__).parent.parent / 'reports' / f'tool-metrics-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')

        summary = self.generate_summary()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)

        print(f"Metrics exported to: {output_path}")
        return output_path


def main():
    """Main entry point"""
    print("=== Tool Performance Tracker ===")
    print("Loading skills usage data...\n")

    tracker = ToolPerformanceTracker()

    # Generate summary
    summary = tracker.generate_summary()

    print(f"Total Skills Tracked: {summary['total_skills_tracked']}")
    print(f"Total Calls: {summary['total_calls']}")
    print(f"Average Success Rate: {summary['avg_success_rate']:.1f}%\n")

    # Show high performers
    print("=== High Performers (>70% success rate) ===")
    for tool in summary['high_performers'][:10]:
        print(f"  {tool['skill']}: {tool['success_rate']:.1f}% ({tool['call_count']} calls)")

    # Show underutilized tools
    print(f"\n=== Underutilized Tools (<5 calls) ===")
    for tool in summary['underutilized'][:10]:
        print(f"  {tool['skill']}: {tool['call_count']} calls ({tool['success_rate']:.1f}% success)")

    # Show expensive tools
    print(f"\n=== Expensive Tools (>1000 tokens/call) ===")
    for tool in summary['expensive_tools'][:10]:
        print(f"  {tool['skill']}: ~{tool['estimated_tokens']} tokens/call ({tool['call_count']} calls)")

    # Export
    output_file = tracker.export_json()
    print(f"\n[OK] Full metrics exported to: {output_file}")


if __name__ == '__main__':
    main()
