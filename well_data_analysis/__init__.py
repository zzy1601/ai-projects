"""
Well Data Analysis Package

A comprehensive solution for analyzing well data based on statistical and depth information.
Provides capabilities for lithology identification and metric calculations across multiple 
stratigraphic periods.

Author: AI Projects Team
Version: 1.0.0
"""

from .well_analyzer import WellDataAnalyzer, load_sample_data, create_sample_intervals

__version__ = "1.0.0"
__author__ = "AI Projects Team"

__all__ = [
    'WellDataAnalyzer',
    'load_sample_data', 
    'create_sample_intervals'
]