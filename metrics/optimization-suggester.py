#!/usr/bin/env python3
"""
Optimization Suggester - Week 1 Day 2-3 Implementation
Generates actionable optimization recommendations based on tool metrics and ROI
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class OptimizationSuggester:
    """Generates optimization suggestions for tool usage"""

    def __init__(self, metrics_file: str = None, roi_file: str = None):
        """Initialize with metrics and ROI data"""
        self.metrics_file = metrics_file
        self.roi_file = roi_file
        self.metrics_data = None
        self.roi_data = None

        if metrics_file:
            self.load_metrics(metrics_file)
        if roi_file:
            self.load_roi(roi_file)

    def load_metrics(self, metrics_file: str):
        """Load metrics from JSON file"""
        with open(metrics_file, 'r', encoding='utf-8') as f:
            self.metrics_data = json.load(f)

    def load_roi(self, roi_file: str):
        """Load ROI data from JSON file"""
        with open(roi_file, 'r', encoding='utf-8') as f:
            self.roi_data = json.load(f)

    def suggest_high_performers(self) -> List[Dict[str, Any]]:
        """Suggest using high-performing tools more often"""
        if not self.metrics_data:
            return []

        suggestions = []
        high_performers = self.metrics_data.get('high_performers', [])

        for tool in high_performers:
            if tool['success_rate'] >= 90.0 and tool['call_count'] < 20:
                suggestions.append({
                    'type': 'UNDERUTILIZATION',
                    'priority': 'HIGH',
                    'tool': tool['skill'],
                    'recommendation': f"Increase usage of '{tool['skill']}' - currently {tool['success_rate']:.1f}% success rate with only {tool['call_count']} calls",
                    'action': f"Consider integrating '{tool['skill']}' into more workflows",
                    'expected_benefit': "Higher success rate tools provide more reliable outcomes",
                    'metrics': tool
                })

        return suggestions

    def suggest_low_performers(self) -> List[Dict[str, Any]]:
        """Suggest investigating or improving low-performing tools"""
        if not self.metrics_data:
            return []

        suggestions = []
        all_tools = self.metrics_data.get('high_performers', []) + self.metrics_data.get('underutilized', [])

        for tool in all_tools:
            if tool['success_rate'] < 70.0 and tool['call_count'] >= 5:
                suggestions.append({
                    'type': 'LOW_PERFORMANCE',
                    'priority': 'HIGH',
                    'tool': tool['skill'],
                    'recommendation': f"Investigate '{tool['skill']}' - only {tool['success_rate']:.1f}% success rate across {tool['call_count']} calls",
                    'action': f"Review error logs, improve error handling, or consider alternatives",
                    'expected_benefit': f"Improving success rate from {tool['success_rate']:.1f}% to 80%+ would save significant time",
                    'metrics': tool
                })

        return suggestions

    def suggest_expensive_tools(self) -> List[Dict[str, Any]]:
        """Suggest optimizing expensive tools"""
        if not self.metrics_data:
            return []

        suggestions = []
        expensive = self.metrics_data.get('expensive_tools', [])

        for tool in expensive[:5]:  # Top 5 most expensive
            suggestions.append({
                'type': 'HIGH_COST',
                'priority': 'MEDIUM',
                'tool': tool['skill'],
                'recommendation': f"Optimize '{tool['skill']}' - estimated {tool['estimated_tokens']} tokens/call",
                'action': "Review prompts for efficiency, cache repeated queries, or use cheaper alternatives",
                'expected_benefit': f"Reducing token usage by 30% would save ~{int(tool['estimated_tokens'] * 0.3)} tokens/call",
                'metrics': tool
            })

        return suggestions

    def suggest_roi_improvements(self) -> List[Dict[str, Any]]:
        """Suggest ROI-based optimizations"""
        if not self.roi_data:
            return []

        suggestions = []

        # Negative ROI tools
        negative_roi = self.roi_data.get('negative_roi_tools', [])
        for tool in negative_roi:
            suggestions.append({
                'type': 'NEGATIVE_ROI',
                'priority': 'CRITICAL',
                'tool': tool['tool'],
                'recommendation': f"'{tool['tool']}' has negative ROI ({tool['roi_percentage']:.1f}%) - cost exceeds value",
                'action': "Improve success rate, reduce cost, increase value, or deprecate",
                'expected_benefit': f"Eliminating would save {abs(tool['net_value_hours']):.1f} hours",
                'metrics': tool
            })

        # Low ROI tools (positive but < 100%)
        all_tools = self.roi_data.get('all_tools', [])
        low_roi = [t for t in all_tools if 0 <= t['roi_percentage'] < 100]
        for tool in low_roi[:5]:
            suggestions.append({
                'type': 'LOW_ROI',
                'priority': 'MEDIUM',
                'tool': tool['tool'],
                'recommendation': f"'{tool['tool']}' has low ROI ({tool['roi_percentage']:.1f}%) - barely breaking even",
                'action': "Improve automation, reduce manual steps, or increase value delivered",
                'expected_benefit': f"Doubling ROI would add {tool['net_value_hours']:.1f} hours of value",
                'metrics': tool
            })

        return suggestions

    def suggest_underutilized(self) -> List[Dict[str, Any]]:
        """Suggest leveraging underutilized tools"""
        if not self.metrics_data:
            return []

        suggestions = []
        underutilized = self.metrics_data.get('underutilized', [])

        for tool in underutilized:
            if tool['success_rate'] >= 80.0:  # High success rate but low usage
                suggestions.append({
                    'type': 'UNTAPPED_POTENTIAL',
                    'priority': 'LOW',
                    'tool': tool['skill'],
                    'recommendation': f"'{tool['skill']}' shows {tool['success_rate']:.1f}% success but only {tool['call_count']} calls",
                    'action': "If tool is valuable, integrate into regular workflows. If not needed, consider deprecation.",
                    'expected_benefit': "Leverage proven tools more often or clean up unused tools",
                    'metrics': tool
                })

        return suggestions

    def generate_weekly_recommendations(self) -> Dict[str, Any]:
        """Generate comprehensive weekly optimization recommendations"""
        all_suggestions = []

        # Collect all suggestions
        all_suggestions.extend(self.suggest_high_performers())
        all_suggestions.extend(self.suggest_low_performers())
        all_suggestions.extend(self.suggest_expensive_tools())
        all_suggestions.extend(self.suggest_roi_improvements())
        all_suggestions.extend(self.suggest_underutilized())

        # Sort by priority
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        all_suggestions.sort(key=lambda x: priority_order.get(x['priority'], 9))

        # Group by type
        by_type = {}
        for suggestion in all_suggestions:
            type_name = suggestion['type']
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(suggestion)

        # Calculate potential impact
        total_potential_hours = sum(
            abs(s['metrics'].get('net_value_hours', 0))
            for s in all_suggestions
            if 'metrics' in s and 'net_value_hours' in s['metrics']
        )

        return {
            'summary': {
                'total_suggestions': len(all_suggestions),
                'critical': len([s for s in all_suggestions if s['priority'] == 'CRITICAL']),
                'high': len([s for s in all_suggestions if s['priority'] == 'HIGH']),
                'medium': len([s for s in all_suggestions if s['priority'] == 'MEDIUM']),
                'low': len([s for s in all_suggestions if s['priority'] == 'LOW']),
                'potential_impact_hours': total_potential_hours
            },
            'suggestions': all_suggestions,
            'by_type': by_type,
            'timestamp': datetime.now().isoformat()
        }

    def export_json(self, output_path: str = None):
        """Export recommendations to JSON"""
        if output_path is None:
            output_path = str(Path(__file__).parent.parent / 'reports' / f'optimization-recommendations-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')

        recommendations = self.generate_weekly_recommendations()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, indent=2)

        print(f"Recommendations exported to: {output_path}")
        return output_path

    def export_markdown(self, output_path: str = None):
        """Export recommendations to human-readable Markdown"""
        if output_path is None:
            output_path = str(Path(__file__).parent.parent / 'reports' / 'tool-usage-report.md')

        recommendations = self.generate_weekly_recommendations()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Tool Usage Optimization Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Summary
            summary = recommendations['summary']
            f.write("## Summary\n\n")
            f.write(f"- **Total Suggestions:** {summary['total_suggestions']}\n")
            f.write(f"- **Critical:** {summary['critical']}\n")
            f.write(f"- **High Priority:** {summary['high']}\n")
            f.write(f"- **Medium Priority:** {summary['medium']}\n")
            f.write(f"- **Low Priority:** {summary['low']}\n")
            f.write(f"- **Potential Impact:** {summary['potential_impact_hours']:.1f} hours\n\n")

            # Critical/High priority suggestions
            critical_and_high = [s for s in recommendations['suggestions'] if s['priority'] in ['CRITICAL', 'HIGH']]
            if critical_and_high:
                f.write("## Critical & High Priority Actions\n\n")
                for i, suggestion in enumerate(critical_and_high, 1):
                    f.write(f"### {i}. {suggestion['tool']} ({suggestion['priority']})\n\n")
                    f.write(f"**Type:** {suggestion['type']}\n\n")
                    f.write(f"**Recommendation:** {suggestion['recommendation']}\n\n")
                    f.write(f"**Action:** {suggestion['action']}\n\n")
                    f.write(f"**Expected Benefit:** {suggestion['expected_benefit']}\n\n")

            # Medium/Low priority suggestions
            medium_and_low = [s for s in recommendations['suggestions'] if s['priority'] in ['MEDIUM', 'LOW']]
            if medium_and_low:
                f.write("## Medium & Low Priority Optimizations\n\n")
                for suggestion in medium_and_low:
                    f.write(f"- **{suggestion['tool']}** ({suggestion['priority']}): {suggestion['recommendation']}\n")

            # By type breakdown
            f.write("\n## Breakdown by Type\n\n")
            for type_name, suggestions in recommendations['by_type'].items():
                f.write(f"### {type_name.replace('_', ' ').title()}\n\n")
                for suggestion in suggestions:
                    f.write(f"- {suggestion['tool']}: {suggestion['recommendation']}\n")
                f.write("\n")

        print(f"Markdown report exported to: {output_path}")
        return output_path


def main():
    """Main entry point"""
    import glob

    print("=== Optimization Suggester ===\n")

    reports_dir = Path(__file__).parent.parent / 'reports'

    # Find latest files
    metrics_files = glob.glob(str(reports_dir / 'tool-metrics-*.json'))
    roi_files = glob.glob(str(reports_dir / 'roi-report-*.json'))

    if not metrics_files:
        print("Error: No metrics files found. Run tool-performance-tracker.py first.")
        sys.exit(1)

    if not roi_files:
        print("Error: No ROI files found. Run roi-calculator.py first.")
        sys.exit(1)

    latest_metrics = max(metrics_files, key=lambda x: Path(x).stat().st_mtime)
    latest_roi = max(roi_files, key=lambda x: Path(x).stat().st_mtime)

    print(f"Loading metrics from: {latest_metrics}")
    print(f"Loading ROI data from: {latest_roi}\n")

    suggester = OptimizationSuggester(latest_metrics, latest_roi)
    recommendations = suggester.generate_weekly_recommendations()

    # Print summary
    summary = recommendations['summary']
    print(f"Total Suggestions: {summary['total_suggestions']}")
    print(f"  Critical: {summary['critical']}")
    print(f"  High: {summary['high']}")
    print(f"  Medium: {summary['medium']}")
    print(f"  Low: {summary['low']}")
    print(f"Potential Impact: {summary['potential_impact_hours']:.1f} hours\n")

    # Show critical/high priority
    critical_high = [s for s in recommendations['suggestions'] if s['priority'] in ['CRITICAL', 'HIGH']]
    if critical_high:
        print("=== Critical & High Priority ===")
        for suggestion in critical_high:
            print(f"\n[{suggestion['priority']}] {suggestion['tool']}")
            print(f"  {suggestion['recommendation']}")
            print(f"  => {suggestion['action']}")

    # Export
    json_file = suggester.export_json()
    md_file = suggester.export_markdown()

    print(f"\n[OK] JSON report: {json_file}")
    print(f"[OK] Markdown report: {md_file}")


if __name__ == '__main__':
    main()
