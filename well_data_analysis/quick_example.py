#!/usr/bin/env python3
"""
Quick example script for well data analysis

This script demonstrates the basic usage of the well data analyzer with minimal code.
"""

from well_analyzer import WellDataAnalyzer, load_sample_data, create_sample_intervals

def main():
    """Quick example of well data analysis"""
    print("🔍 Well Data Analysis - Quick Example")
    print("=" * 50)
    
    # Step 1: Initialize analyzer
    analyzer = WellDataAnalyzer()
    print("✓ Analyzer initialized")
    
    # Step 2: Load sample data
    data = load_sample_data()
    intervals = create_sample_intervals()
    print(f"✓ Sample data loaded: {len(data)} records from {data['well_name'].nunique()} wells")
    
    # Step 3: Perform analysis
    results = analyzer.analyze_well_data(data, intervals)
    print(f"✓ Analysis completed for {len(results)} stratigraphic periods")
    
    # Step 4: Display summary
    print("\n📊 Analysis Summary:")
    print("-" * 40)
    
    for period, df in results.items():
        if not df.empty:
            avg_mud_thickness = df['mudstone_thickness'].mean()
            avg_mud_ratio = df['mud_to_layer_ratio'].mean()
            avg_toc = df['avg_TOC'].mean()
            
            print(f"{period}:")
            print(f"  • Average mudstone thickness: {avg_mud_thickness:.1f}m")
            print(f"  • Average mud-to-layer ratio: {avg_mud_ratio:.3f}")
            print(f"  • Average TOC: {avg_toc:.3f}")
            print()
    
    # Step 5: Generate formatted tables
    summary_tables = analyzer.generate_summary_tables()
    print("✓ Summary tables generated")
    
    # Display one example table
    if '沙三下' in summary_tables and not summary_tables['沙三下'].empty:
        print("\n📋 Example Summary Table (沙三下):")
        print("-" * 60)
        print(summary_tables['沙三下'].to_string(index=False))
    
    print("\n🎉 Analysis completed successfully!")
    print("\n💡 Tip: Check the Jupyter notebook 'Well_Data_Analysis_Demo.ipynb' for a comprehensive tutorial.")

if __name__ == "__main__":
    main()