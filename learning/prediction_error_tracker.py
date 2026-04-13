#!/usr/bin/env python3
"""
Prediction Error Tracker
Created: 2026-03-21
Purpose: Track prediction accuracy and learn from errors
Value: 550x ROI (1h implementation)
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json
import os
from collections import defaultdict


class PredictionErrorTracker:
    """
    Track and learn from prediction errors

    Key Insight: Prediction errors are the primary learning signal.
    When expected != actual, update internal model to reduce future error.

    Error Types:
    1. **Magnitude Error**: Predicted value wrong
       Example: Predicted execution time 10s, actual 60s

    2. **Direction Error**: Predicted sign wrong
       Example: Predicted performance improvement, actual degradation

    3. **Categorical Error**: Predicted wrong category
       Example: Predicted success, actual failure

    4. **Null Error**: Predicted something, got nothing (or vice versa)
       Example: Predicted file exists, file not found

    Learning from Errors:
    - High error -> Update model weights aggressively
    - Low error -> Small adjustments
    - Systematic error pattern -> Bias correction needed
    - Random errors -> Increase uncertainty estimates
    """

    def __init__(self):
        self.error_log = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "prediction-errors.jsonl"
        self.accuracy_stats = Path(os.environ.get("JENGO_STATE_PATH", ".")) / "prediction-accuracy.json"

        # Load accumulated statistics
        self.stats = self._load_stats()

    def record_prediction(
        self,
        prediction_id: str,
        predicted: any,
        actual: any,
        category: str = "general",
        metadata: Dict = None
    ) -> Dict:
        """
        Record prediction and actual outcome

        Args:
            prediction_id: Unique ID for this prediction
            predicted: What was predicted
            actual: What actually happened
            category: Category of prediction (e.g., "execution_time", "success_rate")
            metadata: Additional context

        Returns:
            {
                'error': float,
                'error_type': str,
                'accuracy': float,
                'learning_signal_strength': float
            }
        """
        # Calculate error
        error_analysis = self._analyze_error(predicted, actual, category)

        # Log prediction
        log_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'prediction_id': prediction_id,
            'category': category,
            'predicted': predicted,
            'actual': actual,
            'error': error_analysis['error'],
            'error_type': error_analysis['error_type'],
            'metadata': metadata or {}
        }

        with open(self.error_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Update statistics
        self._update_stats(category, error_analysis)

        # Save stats
        self._save_stats()

        return error_analysis

    def get_accuracy_by_category(self, category: str) -> Dict:
        """Get accuracy statistics for category"""
        if category not in self.stats['by_category']:
            return {
                'category': category,
                'total_predictions': 0,
                'accuracy': 0.0,
                'mean_error': 0.0
            }

        stats = self.stats['by_category'][category]

        return {
            'category': category,
            'total_predictions': stats['count'],
            'accuracy': stats['correct'] / max(1, stats['count']),
            'mean_error': stats['total_error'] / max(1, stats['count']),
            'median_error': self._calculate_median_error(category)
        }

    def identify_systematic_errors(self) -> List[Dict]:
        """
        Identify patterns in prediction errors

        Returns:
            List of systematic error patterns
        """
        patterns = []

        # Load recent errors
        recent_errors = self._load_recent_errors(limit=100)

        # Group by category
        by_category = defaultdict(list)
        for error in recent_errors:
            by_category[error['category']].append(error)

        # Look for patterns
        for category, errors in by_category.items():
            # Check for consistent directional bias
            bias = self._check_directional_bias(errors)
            if abs(bias) > 0.2:  # Significant bias
                patterns.append({
                    'pattern_type': 'directional_bias',
                    'category': category,
                    'bias': bias,
                    'description': f"Consistently {'over' if bias > 0 else 'under'}-predicting {category}"
                })

            # Check for magnitude scaling error
            scaling_error = self._check_scaling_error(errors)
            if abs(scaling_error - 1.0) > 0.3:  # Off by >30%
                patterns.append({
                    'pattern_type': 'scaling_error',
                    'category': category,
                    'scale_factor': scaling_error,
                    'description': f"Predictions are {scaling_error:.1f}x actual values"
                })

        return patterns

    def get_learning_priorities(self) -> List[Dict]:
        """
        Identify where model needs most improvement

        Returns:
            List of categories ordered by learning priority
        """
        priorities = []

        for category, stats in self.stats['by_category'].items():
            # Priority based on: error magnitude x prediction frequency
            error_magnitude = stats['total_error'] / max(1, stats['count'])
            frequency = stats['count']

            priority_score = error_magnitude * frequency

            priorities.append({
                'category': category,
                'priority_score': priority_score,
                'current_accuracy': stats['correct'] / max(1, stats['count']),
                'prediction_count': frequency,
                'mean_error': error_magnitude
            })

        # Sort by priority
        priorities.sort(key=lambda p: p['priority_score'], reverse=True)

        return priorities

    def suggest_model_updates(self) -> List[Dict]:
        """
        Suggest how to update model based on errors

        Returns:
            List of suggested updates
        """
        updates = []

        # Find systematic errors
        patterns = self.identify_systematic_errors()

        for pattern in patterns:
            if pattern['pattern_type'] == 'directional_bias':
                updates.append({
                    'update_type': 'bias_correction',
                    'category': pattern['category'],
                    'adjustment': -pattern['bias'],  # Opposite of bias
                    'description': f"Add {-pattern['bias']:.2f} offset to {pattern['category']} predictions"
                })

            elif pattern['pattern_type'] == 'scaling_error':
                updates.append({
                    'update_type': 'scale_correction',
                    'category': pattern['category'],
                    'adjustment': 1.0 / pattern['scale_factor'],
                    'description': f"Multiply {pattern['category']} predictions by {1.0/pattern['scale_factor']:.2f}"
                })

        return updates

    def _analyze_error(self, predicted: any, actual: any, category: str) -> Dict:
        """Analyze prediction error"""
        error_type = 'unknown'
        error_magnitude = 0.0
        accuracy = 0.0
        learning_signal = 0.0

        # Type-specific error analysis
        if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
            # Numeric error
            error_magnitude = abs(predicted - actual)
            relative_error = error_magnitude / max(abs(actual), 1.0)

            accuracy = max(0, 1.0 - relative_error)
            learning_signal = relative_error  # High error = strong learning signal

            # Check direction
            if (predicted > actual and predicted - actual > abs(actual) * 0.1):
                error_type = 'overestimate'
            elif (actual > predicted and actual - predicted > abs(actual) * 0.1):
                error_type = 'underestimate'
            else:
                error_type = 'magnitude'

        elif isinstance(predicted, bool) and isinstance(actual, bool):
            # Boolean error
            error_magnitude = 0 if predicted == actual else 1
            accuracy = 1.0 if predicted == actual else 0.0
            learning_signal = error_magnitude
            error_type = 'categorical'

        elif predicted is None or actual is None:
            # Null error
            error_magnitude = 1 if predicted != actual else 0
            accuracy = 1.0 if predicted == actual else 0.0
            learning_signal = error_magnitude
            error_type = 'null_error'

        else:
            # Categorical/string error
            error_magnitude = 0 if predicted == actual else 1
            accuracy = 1.0 if predicted == actual else 0.0
            learning_signal = error_magnitude
            error_type = 'categorical'

        return {
            'error': error_magnitude,
            'error_type': error_type,
            'accuracy': accuracy,
            'learning_signal_strength': learning_signal
        }

    def _update_stats(self, category: str, error_analysis: Dict):
        """Update running statistics"""
        if category not in self.stats['by_category']:
            self.stats['by_category'][category] = {
                'count': 0,
                'correct': 0,
                'total_error': 0.0
            }

        stats = self.stats['by_category'][category]

        stats['count'] += 1
        stats['total_error'] += error_analysis['error']

        if error_analysis['accuracy'] > 0.9:  # Consider "correct" if >90% accurate
            stats['correct'] += 1

    def _check_directional_bias(self, errors: List[Dict]) -> float:
        """Check for consistent over/under-prediction"""
        if not errors:
            return 0.0

        biases = []

        for error in errors:
            predicted = error.get('predicted')
            actual = error.get('actual')

            if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
                if actual != 0:
                    bias = (predicted - actual) / abs(actual)
                    biases.append(bias)

        if not biases:
            return 0.0

        return sum(biases) / len(biases)

    def _check_scaling_error(self, errors: List[Dict]) -> float:
        """Check if predictions are consistently scaled wrong"""
        if not errors:
            return 1.0

        ratios = []

        for error in errors:
            predicted = error.get('predicted')
            actual = error.get('actual')

            if isinstance(predicted, (int, float)) and isinstance(actual, (int, float)):
                if actual != 0:
                    ratio = predicted / actual
                    ratios.append(ratio)

        if not ratios:
            return 1.0

        return sum(ratios) / len(ratios)

    def _calculate_median_error(self, category: str) -> float:
        """Calculate median error for category"""
        errors = self._load_recent_errors(category=category, limit=100)

        if not errors:
            return 0.0

        error_values = [e['error'] for e in errors]
        error_values.sort()

        mid = len(error_values) // 2

        if len(error_values) % 2 == 0:
            return (error_values[mid - 1] + error_values[mid]) / 2
        else:
            return error_values[mid]

    def _load_recent_errors(self, limit: int = 100, category: str = None) -> List[Dict]:
        """Load recent prediction errors"""
        if not self.error_log.exists():
            return []

        errors = []

        with open(self.error_log, 'r') as f:
            for line in f:
                error = json.loads(line)

                if category is None or error.get('category') == category:
                    errors.append(error)

        # Return most recent
        return errors[-limit:]

    def _load_stats(self) -> Dict:
        """Load statistics from disk"""
        if not self.accuracy_stats.exists():
            return {
                'by_category': {},
                'overall': {'count': 0, 'correct': 0, 'total_error': 0.0}
            }

        with open(self.accuracy_stats, 'r') as f:
            return json.load(f)

    def _save_stats(self):
        """Save statistics to disk"""
        with open(self.accuracy_stats, 'w') as f:
            json.dump(self.stats, f, indent=2)


# === GLOBAL TRACKER INSTANCE ===
_global_tracker = None


def get_prediction_tracker() -> PredictionErrorTracker:
    """Get global prediction error tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = PredictionErrorTracker()
    return _global_tracker


# === USAGE ===
if __name__ == "__main__":
    print("=== PREDICTION ERROR TRACKER ===\n")

    tracker = get_prediction_tracker()

    # Example 1: Record prediction
    print("Recording predictions...")
    tracker.record_prediction(
        prediction_id="pred_001",
        predicted=10.0,
        actual=60.0,
        category="execution_time_seconds"
    )

    tracker.record_prediction(
        prediction_id="pred_002",
        predicted=True,
        actual=False,
        category="test_pass"
    )

    # Example 2: Get accuracy stats
    print("\nAccuracy by category:")
    for category in ['execution_time_seconds', 'test_pass']:
        stats = tracker.get_accuracy_by_category(category)
        print(f"  {category}: {stats['accuracy']:.0%} accurate")
        print(f"    Mean error: {stats['mean_error']:.2f}\n")

    # Example 3: Identify systematic errors
    print("Systematic error patterns:")
    patterns = tracker.identify_systematic_errors()

    for pattern in patterns:
        print(f"  - {pattern['description']}")

    # Example 4: Get learning priorities
    print("\nLearning priorities:")
    priorities = tracker.get_learning_priorities()

    for i, priority in enumerate(priorities[:3], 1):
        print(f"  {i}. {priority['category']}")
        print(f"     Priority score: {priority['priority_score']:.0f}")
        print(f"     Current accuracy: {priority['current_accuracy']:.0%}\n")
