"""
Test script for well data analyzer to validate functionality
"""
import pandas as pd
import numpy as np
from well_analyzer import WellDataAnalyzer, load_sample_data, create_sample_intervals

def test_lithology_identification():
    """Test lithology identification functionality"""
    print("Testing lithology identification...")
    analyzer = WellDataAnalyzer()
    
    test_cases = [
        ('泥岩', 'mudstone'),
        ('砂岩', 'sandstone'),
        ('石灰岩', 'other'),
        ('泥质砂岩', 'sandstone'),
        ('砂质泥岩', 'mudstone'),
        ('', 'other'),
        (None, 'other')
    ]
    
    all_passed = True
    for input_text, expected in test_cases:
        result = analyzer.identify_lithology(input_text)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_text}' -> {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    return all_passed

def test_thickness_calculations():
    """Test thickness calculation methods"""
    print("\nTesting thickness calculations...")
    analyzer = WellDataAnalyzer()
    
    # Test stratigraphic thickness
    strat_thickness = analyzer.calculate_stratigraphic_thickness(1000, 1200)
    print(f"  ✓ Stratigraphic thickness (1000-1200): {strat_thickness}m")
    
    # Test mud-to-layer ratio
    mud_ratio = analyzer.calculate_mud_to_layer_ratio(100, 200)
    print(f"  ✓ Mud-to-layer ratio (100/200): {mud_ratio}")
    
    # Test with zero denominator
    mud_ratio_zero = analyzer.calculate_mud_to_layer_ratio(100, 0)
    print(f"  ✓ Mud-to-layer ratio (100/0): {mud_ratio_zero}")
    
    return True

def test_full_analysis():
    """Test full analysis workflow"""
    print("\nTesting full analysis workflow...")
    
    # Create simple test data
    test_data = pd.DataFrame({
        'well_name': ['TestWell'] * 10,
        'depth': range(1000, 1100, 10),
        'lithology': ['泥岩', '砂岩', '泥岩', '砂岩', '泥岩', 
                     '砂岩', '泥岩', '砂岩', '泥岩', '砂岩'],
        'TOC': [2.5] * 10,
        'S1': [1.2] * 10,
        'brittleness_index': [0.5] * 10,
        'Ro': [0.8] * 10,
        'thickness': [10] * 10
    })
    
    test_intervals = {
        'TestWell': {
            '沙三下': (1000, 1090)
        }
    }
    
    analyzer = WellDataAnalyzer()
    results = analyzer.analyze_well_data(test_data, test_intervals)
    
    # Validate results
    if '沙三下' in results and not results['沙三下'].empty:
        result_row = results['沙三下'].iloc[0]
        print(f"  ✓ Analysis completed for TestWell")
        print(f"    - Mudstone thickness: {result_row['mudstone_thickness']}m")
        print(f"    - Stratigraphic thickness: {result_row['stratigraphic_thickness']}m")
        print(f"    - Mud-to-layer ratio: {result_row['mud_to_layer_ratio']:.3f}")
        print(f"    - Average TOC: {result_row['avg_TOC']:.3f}")
        return True
    else:
        print("  ✗ Analysis failed")
        return False

def test_sample_data_analysis():
    """Test analysis with sample data"""
    print("\nTesting sample data analysis...")
    
    analyzer = WellDataAnalyzer()
    sample_data = load_sample_data()
    sample_intervals = create_sample_intervals()
    
    results = analyzer.analyze_well_data(sample_data, sample_intervals)
    
    # Check if all periods have results
    expected_periods = ['沙三下', '沙四上晚期', '沙四上中期', '沙四上早期']
    all_periods_found = True
    
    for period in expected_periods:
        if period in results and not results[period].empty:
            print(f"  ✓ {period}: {len(results[period])} wells analyzed")
        else:
            print(f"  ✗ {period}: No results found")
            all_periods_found = False
    
    # Test summary table generation
    summary_tables = analyzer.generate_summary_tables()
    print(f"  ✓ Generated {len(summary_tables)} summary tables")
    
    return all_periods_found

def run_all_tests():
    """Run all tests"""
    print("Running Well Data Analyzer Tests")
    print("=" * 50)
    
    tests = [
        ("Lithology Identification", test_lithology_identification),
        ("Thickness Calculations", test_thickness_calculations),
        ("Full Analysis Workflow", test_full_analysis),
        ("Sample Data Analysis", test_sample_data_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✓ {test_name}: PASSED")
                passed += 1
            else:
                print(f"\n✗ {test_name}: FAILED")
        except Exception as e:
            print(f"\n✗ {test_name}: ERROR - {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The well data analyzer is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()