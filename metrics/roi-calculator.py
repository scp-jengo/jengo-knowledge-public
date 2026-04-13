#!/usr/bin/env python3
"""
ROI Calculator - Week 1 Day 2-3 Implementation
Calculates return on investment for tools/skills
Formula: ROI = (Value - Cost) / Cost
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ROICalculator:
    """Calculates ROI for tools and skills"""

    # Value estimates (in hours saved per successful call)
    TOOL_VALUE_ESTIMATES = {
        # Deployment tools (HIGH value - automation)
        'deploy-dotnet-iis': 0.5,  # 30 minutes saved per deployment
        'deploy-dotnet-iis-skill': 0.5,

        # Development tools (MEDIUM-HIGH value)
        'implement-todo': 2.0,  # 2 hours saved per task
        'allocate-worktree': 0.1,  # 6 minutes saved
        'release-worktree': 0.05,  # 3 minutes saved

        # Review/Analysis tools (MEDIUM value)
        'clickup-reviewer': 0.5,  # 30 minutes per review
        'auto-pr-review': 0.75,  # 45 minutes per review
        'task-review': 0.5,

        # Intelligence tools (HIGH value - strategic)
        'expert-analysis': 3.0,  # 3 hours of research
        'kaizen': 2.0,  # 2 hours of optimization
        'continuous-optimization': 1.0,

        # Utility tools (LOW-MEDIUM value)
        'worktree-status': 0.02,  # 1 minute
        'debug-mode': 0.05,  # 3 minutes
        'feature-mode': 0.05,

        # Default for unknown tools
        '__default__': 0.25  # 15 minutes
    }

    # Cost estimates (in hours per call - LLM time + compute)
    TOOL_COST_ESTIMATES = {
        # Expensive tools (long running, high token count)
        'expert-analysis': 0.5,  # 30 minutes of LLM time
        'kaizen': 0.33,  # 20 minutes
        'implement-todo': 0.33,  # 20 minutes
        'continuous-optimization': 0.25,  # 15 minutes

        # Medium cost tools
        'clickup-reviewer': 0.17,  # 10 minutes
        'auto-pr-review': 0.17,
        'task-review': 0.17,
        'deploy-dotnet-iis': 0.08,  # 5 minutes

        # Low cost tools
        'allocate-worktree': 0.02,  # 1 minute
        'release-worktree': 0.02,
        'worktree-status': 0.01,  # 30 seconds
        'debug-mode': 0.01,
        'feature-mode': 0.01,

        # Default
        '__default__': 0.08  # 5 minutes
    }

    def __init__(self, metrics_file: str = None):
        """Initialize with metrics from tool-performance-tracker"""
        self.metrics_file = metrics_file
        self.metrics_data = None

        if metrics_file:
            self.load_metrics(metrics_file)

    def load_metrics(self, metrics_file: str):
        """Load metrics from JSON file"""
        with open(metrics_file, 'r', encoding='utf-8') as f:
            self.metrics_data = json.load(f)

    def get_tool_value(self, tool: str) -> float:
        """Get estimated value (hours saved) for a tool"""
        return self.TOOL_VALUE_ESTIMATES.get(tool, self.TOOL_VALUE_ESTIMATES['__default__'])

    def get_tool_cost(self, tool: str) -> float:
        """Get estimated cost (hours spent) for a tool"""
        return self.TOOL_COST_ESTIMATES.get(tool, self.TOOL_COST_ESTIMATES['__default__'])

    def calculate_roi(self, tool: str, call_count: int, success_rate: float) -> Dict[str, Any]:
        """
        Calculate ROI for a tool

        ROI = (Value - Cost) / Cost
        Where:
        - Value = hours_saved_per_call * successful_calls
        - Cost = hours_spent_per_call * total_calls
        """
        value_per_call = self.get_tool_value(tool)
        cost_per_call = self.get_tool_cost(tool)

        # Calculate successful calls
        successful_calls = (success_rate / 100) * call_count

        # Total value and cost
        total_value = value_per_call * successful_calls
        total_cost = cost_per_call * call_count

        # ROI calculation
        if total_cost == 0:
            roi = 0.0
        else:
            roi = ((total_value - total_cost) / total_cost) * 100

        return {
            'tool': tool,
            'call_count': call_count,
            'success_rate': success_rate,
            'successful_calls': int(successful_calls),
            'value_per_call_hours': value_per_call,
            'cost_per_call_hours': cost_per_call,
            'total_value_hours': total_value,
            'total_cost_hours': total_cost,
            'net_value_hours': total_value - total_cost,
            'roi_percentage': roi
        }

    def calculate_all_rois(self) -> List[Dict[str, Any]]:
        """Calculate ROI for all tools in metrics"""
        if not self.metrics_data:
            return []

        roi_results = []

        # Process high performers
        for tool_data in self.metrics_data.get('high_performers', []):
            roi = self.calculate_roi(
                tool_data['skill'],
                tool_data['call_count'],
                tool_data['success_rate']
            )
            roi_results.append(roi)

        # Process underutilized
        for tool_data in self.metrics_data.get('underutilized', []):
            roi = self.calculate_roi(
                tool_data['skill'],
                tool_data['call_count'],
                tool_data['success_rate']
            )
            roi_results.append(roi)

        return sorted(roi_results, key=lambda x: x['roi_percentage'], reverse=True)

    def get_high_roi_tools(self, min_roi: float = 1000.0) -> List[Dict[str, Any]]:
        """Get tools with >10x ROI (1000%)"""
        all_rois = self.calculate_all_rois()
        return [tool for tool in all_rois if tool['roi_percentage'] >= min_roi]

    def get_negative_roi_tools(self) -> List[Dict[str, Any]]:
        """Get tools with negative ROI (cost > value)"""
        all_rois = self.calculate_all_rois()
        return [tool for tool in all_rois if tool['roi_percentage'] < 0]

    def generate_report(self) -> Dict[str, Any]:
        """Generate ROI analysis report"""
        all_rois = self.calculate_all_rois()
        high_roi = self.get_high_roi_tools()
        negative_roi = self.get_negative_roi_tools()

        # Calculate totals
        total_value = sum(tool['total_value_hours'] for tool in all_rois)
        total_cost = sum(tool['total_cost_hours'] for tool in all_rois)
        net_value = total_value - total_cost
        overall_roi = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0

        return {
            'summary': {
                'total_tools': len(all_rois),
                'total_value_hours': total_value,
                'total_cost_hours': total_cost,
                'net_value_hours': net_value,
                'overall_roi_percentage': overall_roi
            },
            'high_roi_tools': high_roi,
            'negative_roi_tools': negative_roi,
            'all_tools': all_rois,
            'timestamp': datetime.now().isoformat()
        }

    def export_json(self, output_path: str = None):
        """Export ROI report to JSON"""
        if output_path is None:
            output_path = str(Path(__file__).parent.parent / 'reports' / f'roi-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')

        report = self.generate_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"ROI report exported to: {output_path}")
        return output_path


def main():
    """Main entry point"""
    import glob

    print("=== Tool ROI Calculator ===\n")

    # Find latest metrics file
    reports_dir = Path(__file__).parent.parent / 'reports'
    metrics_files = glob.glob(str(reports_dir / 'tool-metrics-*.json'))

    if not metrics_files:
        print("Error: No metrics files found. Run tool-performance-tracker.py first.")
        sys.exit(1)

    latest_metrics = max(metrics_files, key=lambda x: Path(x).stat().st_mtime)
    print(f"Loading metrics from: {latest_metrics}\n")

    calculator = ROICalculator(latest_metrics)
    report = calculator.generate_report()

    # Print summary
    summary = report['summary']
    print(f"Total Tools Analyzed: {summary['total_tools']}")
    print(f"Total Value: {summary['total_value_hours']:.1f} hours")
    print(f"Total Cost: {summary['total_cost_hours']:.1f} hours")
    print(f"Net Value: {summary['net_value_hours']:.1f} hours")
    print(f"Overall ROI: {summary['overall_roi_percentage']:.1f}%\n")

    # High ROI tools
    print("=== High ROI Tools (>1000%) ===")
    for tool in report['high_roi_tools'][:10]:
        print(f"  {tool['tool']}: {tool['roi_percentage']:.0f}% ROI")
        print(f"    => {tool['net_value_hours']:.1f}h net value ({tool['successful_calls']} successful calls)")

    # Negative ROI tools
    if report['negative_roi_tools']:
        print(f"\n=== Negative ROI Tools (Cost > Value) ===")
        for tool in report['negative_roi_tools'][:10]:
            print(f"  {tool['tool']}: {tool['roi_percentage']:.1f}% ROI")
            print(f"    => {tool['net_value_hours']:.1f}h net value ({tool['call_count']} calls)")

    # Export
    output_file = calculator.export_json()
    print(f"\n[OK] Full ROI report exported to: {output_file}")


if __name__ == '__main__':
    main()
