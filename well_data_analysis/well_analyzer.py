"""
Well Data Analysis Module

This module provides functionality to analyze well data based on statistical and depth information.
It identifies mudstone and sandstone from lithology data and calculates various metrics for 
different stratigraphic periods.

Author: AI Projects Team
Date: 2024
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')


class WellDataAnalyzer:
    """
    A comprehensive analyzer for well data that processes lithology information
    and calculates statistical metrics for different stratigraphic periods.
    """
    
    def __init__(self):
        """Initialize the WellDataAnalyzer with default stratigraphic periods."""
        self.stratigraphic_periods = [
            '沙三下',
            '沙四上晚期', 
            '沙四上中期',
            '沙四上早期'
        ]
        
        self.results = {}
        
    def identify_lithology(self, lithology_text: str) -> str:
        """
        Identify lithology type from Chinese text.
        
        Args:
            lithology_text (str): Chinese text describing lithology
            
        Returns:
            str: 'mudstone' if contains '泥岩', 'sandstone' if contains '砂岩', 'other' otherwise
        """
        if not isinstance(lithology_text, str):
            return 'other'
            
        if '泥岩' in lithology_text:
            return 'mudstone'
        elif '砂岩' in lithology_text:
            return 'sandstone'
        else:
            return 'other'
    
    def calculate_mudstone_thickness(self, data: pd.DataFrame, top_depth: float, bottom_depth: float) -> float:
        """
        Calculate cumulative mudstone thickness within depth range.
        
        Args:
            data (pd.DataFrame): Well data with depth and lithology columns
            top_depth (float): Top depth of the interval
            bottom_depth (float): Bottom depth of the interval
            
        Returns:
            float: Cumulative mudstone thickness
        """
        # Filter data within depth range
        depth_filter = (data['depth'] >= top_depth) & (data['depth'] <= bottom_depth)
        interval_data = data[depth_filter].copy()
        
        if interval_data.empty:
            return 0.0
        
        # Identify mudstone layers
        interval_data['lithology_type'] = interval_data['lithology'].apply(self.identify_lithology)
        mudstone_data = interval_data[interval_data['lithology_type'] == 'mudstone']
        
        # Calculate thickness (assuming each row represents a certain thickness interval)
        # If thickness column exists, use it; otherwise estimate from depth intervals
        if 'thickness' in mudstone_data.columns:
            return mudstone_data['thickness'].sum()
        else:
            # Estimate thickness from depth differences
            if len(mudstone_data) <= 1:
                return 0.0
            
            mudstone_data = mudstone_data.sort_values('depth')
            thickness = 0.0
            
            for i in range(len(mudstone_data) - 1):
                thickness += mudstone_data.iloc[i+1]['depth'] - mudstone_data.iloc[i]['depth']
            
            return thickness
    
    def calculate_stratigraphic_thickness(self, top_depth: float, bottom_depth: float) -> float:
        """
        Calculate stratigraphic thickness as difference between bottom and top depths.
        
        Args:
            top_depth (float): Top depth (顶深)
            bottom_depth (float): Bottom depth (底深)
            
        Returns:
            float: Stratigraphic thickness
        """
        return abs(bottom_depth - top_depth)
    
    def calculate_mud_to_layer_ratio(self, mudstone_thickness: float, stratigraphic_thickness: float) -> float:
        """
        Calculate mud-to-layer ratio.
        
        Args:
            mudstone_thickness (float): Cumulative mudstone thickness
            stratigraphic_thickness (float): Total stratigraphic thickness
            
        Returns:
            float: Mud-to-layer ratio (0 if stratigraphic_thickness is 0)
        """
        if stratigraphic_thickness == 0:
            return 0.0
        return mudstone_thickness / stratigraphic_thickness
    
    def calculate_average_attributes(self, data: pd.DataFrame, top_depth: float, bottom_depth: float) -> Dict[str, float]:
        """
        Calculate average values for TOC, S1, Brittleness index, and Ro within depth range.
        
        Args:
            data (pd.DataFrame): Well data containing the attribute columns
            top_depth (float): Top depth of the interval
            bottom_depth (float): Bottom depth of the interval
            
        Returns:
            Dict[str, float]: Dictionary with average values for each attribute
        """
        # Filter data within depth range
        depth_filter = (data['depth'] >= top_depth) & (data['depth'] <= bottom_depth)
        interval_data = data[depth_filter]
        
        attributes = ['TOC', 'S1', 'brittleness_index', 'Ro']
        averages = {}
        
        for attr in attributes:
            if attr in interval_data.columns:
                # Remove NaN values and calculate mean
                valid_values = interval_data[attr].dropna()
                if len(valid_values) > 0:
                    averages[attr] = valid_values.mean()
                else:
                    averages[attr] = np.nan
            else:
                averages[attr] = np.nan
                
        return averages
    
    def analyze_well_data(self, data: pd.DataFrame, well_intervals: Dict[str, Dict[str, Tuple[float, float]]]) -> Dict[str, pd.DataFrame]:
        """
        Analyze well data for all wells and stratigraphic periods.
        
        Args:
            data (pd.DataFrame): Complete well data
            well_intervals (Dict): Dictionary with structure:
                {
                    'well_name': {
                        'period_name': (top_depth, bottom_depth),
                        ...
                    },
                    ...
                }
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with results for each stratigraphic period
        """
        results_by_period = {period: [] for period in self.stratigraphic_periods}
        
        for well_name, intervals in well_intervals.items():
            # Filter data for current well
            well_data = data[data['well_name'] == well_name].copy()
            
            for period, (top_depth, bottom_depth) in intervals.items():
                if period in self.stratigraphic_periods:
                    # Calculate metrics
                    mudstone_thickness = self.calculate_mudstone_thickness(well_data, top_depth, bottom_depth)
                    stratigraphic_thickness = self.calculate_stratigraphic_thickness(top_depth, bottom_depth)
                    mud_to_layer_ratio = self.calculate_mud_to_layer_ratio(mudstone_thickness, stratigraphic_thickness)
                    avg_attributes = self.calculate_average_attributes(well_data, top_depth, bottom_depth)
                    
                    # Create result record
                    result_record = {
                        'well_name': well_name,
                        'stratigraphic_period': period,
                        'top_depth': top_depth,
                        'bottom_depth': bottom_depth,
                        'mudstone_thickness': mudstone_thickness,
                        'stratigraphic_thickness': stratigraphic_thickness,
                        'mud_to_layer_ratio': mud_to_layer_ratio,
                        'avg_TOC': avg_attributes.get('TOC', np.nan),
                        'avg_S1': avg_attributes.get('S1', np.nan),
                        'avg_brittleness_index': avg_attributes.get('brittleness_index', np.nan),
                        'avg_Ro': avg_attributes.get('Ro', np.nan)
                    }
                    
                    results_by_period[period].append(result_record)
        
        # Convert results to DataFrames
        final_results = {}
        for period, records in results_by_period.items():
            if records:
                final_results[period] = pd.DataFrame(records)
            else:
                # Create empty DataFrame with expected columns
                final_results[period] = pd.DataFrame(columns=[
                    'well_name', 'stratigraphic_period', 'top_depth', 'bottom_depth',
                    'mudstone_thickness', 'stratigraphic_thickness', 'mud_to_layer_ratio',
                    'avg_TOC', 'avg_S1', 'avg_brittleness_index', 'avg_Ro'
                ])
        
        self.results = final_results
        return final_results
    
    def generate_summary_tables(self) -> Dict[str, pd.DataFrame]:
        """
        Generate formatted summary tables for each stratigraphic period.
        
        Returns:
            Dict[str, pd.DataFrame]: Formatted summary tables
        """
        summary_tables = {}
        
        for period, df in self.results.items():
            if not df.empty:
                # Create a formatted summary table
                summary = df[['well_name', 'mudstone_thickness', 'stratigraphic_thickness', 
                             'mud_to_layer_ratio', 'avg_TOC', 'avg_S1', 
                             'avg_brittleness_index', 'avg_Ro']].copy()
                
                # Round numerical values for better presentation
                numerical_cols = ['mudstone_thickness', 'stratigraphic_thickness', 'mud_to_layer_ratio',
                                'avg_TOC', 'avg_S1', 'avg_brittleness_index', 'avg_Ro']
                
                for col in numerical_cols:
                    if col in summary.columns:
                        summary[col] = summary[col].round(3)
                
                # Rename columns for better presentation
                summary.columns = [
                    '井名', '泥岩厚度', '地层厚度', '泥地比', 
                    '平均TOC', '平均S1', '平均脆性指数', '平均Ro'
                ]
                
                summary_tables[period] = summary
            else:
                summary_tables[period] = pd.DataFrame(columns=[
                    '井名', '泥岩厚度', '地层厚度', '泥地比', 
                    '平均TOC', '平均S1', '平均脆性指数', '平均Ro'
                ])
        
        return summary_tables
    
    def export_results(self, output_file: str, format: str = 'excel') -> None:
        """
        Export analysis results to file.
        
        Args:
            output_file (str): Output file path
            format (str): Export format ('excel', 'csv')
        """
        summary_tables = self.generate_summary_tables()
        
        if format.lower() == 'excel':
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                for period, table in summary_tables.items():
                    # Clean sheet name for Excel compatibility
                    sheet_name = period.replace('/', '_').replace('\\', '_')[:31]
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
                    
        elif format.lower() == 'csv':
            # For CSV, create separate files for each period
            base_name = output_file.rsplit('.', 1)[0]
            for period, table in summary_tables.items():
                filename = f"{base_name}_{period}.csv"
                table.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"Results exported successfully to {output_file}")


def load_sample_data() -> pd.DataFrame:
    """
    Create sample well data for testing purposes.
    
    Returns:
        pd.DataFrame: Sample well data
    """
    np.random.seed(42)
    
    wells = ['井1', '井2', '井3']
    data = []
    
    for well in wells:
        # Generate depth range
        depths = np.arange(1000, 2000, 5)  # Every 5m from 1000m to 2000m
        
        for depth in depths:
            # Random lithology assignment
            lithology_types = ['泥岩', '砂岩', '石灰岩', '泥质砂岩', '砂质泥岩']
            weights = [0.4, 0.3, 0.1, 0.1, 0.1]  # Higher probability for mudstone and sandstone
            lithology = np.random.choice(lithology_types, p=weights)
            
            # Generate random attribute values
            toc = np.random.normal(2.5, 1.0) if lithology in ['泥岩', '泥质砂岩'] else np.random.normal(1.0, 0.5)
            s1 = np.random.normal(1.2, 0.5)
            brittleness = np.random.uniform(0.3, 0.8)
            ro = np.random.normal(0.8, 0.2)
            
            # Ensure positive values
            toc = max(0.1, toc)
            s1 = max(0.05, s1)
            brittleness = max(0.1, min(1.0, brittleness))
            ro = max(0.3, ro)
            
            data.append({
                'well_name': well,
                'depth': depth,
                'lithology': lithology,
                'TOC': toc,
                'S1': s1,
                'brittleness_index': brittleness,
                'Ro': ro,
                'thickness': 5.0  # 5m thickness per interval
            })
    
    return pd.DataFrame(data)


def create_sample_intervals() -> Dict[str, Dict[str, Tuple[float, float]]]:
    """
    Create sample well intervals for different stratigraphic periods.
    
    Returns:
        Dict: Sample well intervals
    """
    return {
        '井1': {
            '沙三下': (1000, 1200),
            '沙四上晚期': (1200, 1400),
            '沙四上中期': (1400, 1600),
            '沙四上早期': (1600, 1800)
        },
        '井2': {
            '沙三下': (1050, 1250),
            '沙四上晚期': (1250, 1450),
            '沙四上中期': (1450, 1650),
            '沙四上早期': (1650, 1850)
        },
        '井3': {
            '沙三下': (1100, 1300),
            '沙四上晚期': (1300, 1500),
            '沙四上中期': (1500, 1700),
            '沙四上早期': (1700, 1900)
        }
    }


if __name__ == "__main__":
    # Example usage
    print("Well Data Analysis Tool")
    print("=" * 50)
    
    # Create analyzer instance
    analyzer = WellDataAnalyzer()
    
    # Load sample data
    print("\n1. Loading sample data...")
    sample_data = load_sample_data()
    print(f"Loaded {len(sample_data)} data points from {sample_data['well_name'].nunique()} wells")
    
    # Create sample intervals
    sample_intervals = create_sample_intervals()
    print("\n2. Processing well intervals...")
    
    # Analyze data
    results = analyzer.analyze_well_data(sample_data, sample_intervals)
    
    # Display results
    print("\n3. Analysis Results:")
    print("=" * 50)
    
    for period, df in results.items():
        print(f"\n地层时期: {period}")
        print("-" * 30)
        if not df.empty:
            print(df[['well_name', 'mudstone_thickness', 'stratigraphic_thickness', 
                     'mud_to_layer_ratio', 'avg_TOC']].to_string(index=False))
        else:
            print("No data available for this period")
    
    # Generate and display summary tables
    print("\n4. Summary Tables:")
    print("=" * 50)
    
    summary_tables = analyzer.generate_summary_tables()
    for period, table in summary_tables.items():
        print(f"\n{period}:")
        print("-" * 30)
        if not table.empty:
            print(table.to_string(index=False))
        else:
            print("No data available for this period")