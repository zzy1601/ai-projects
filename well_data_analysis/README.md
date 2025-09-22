# Well Data Analysis Solution

A comprehensive Python solution for analyzing well data based on statistical and depth information, with capabilities for lithology identification and metric calculations across multiple stratigraphic periods.

## Features

### Core Functionality
- **Lithology Identification**: Automatically identifies mudstone (泥岩) and sandstone (砂岩) from Chinese text descriptions
- **Multi-metric Calculations**: Computes essential petroleum geology metrics
- **Multi-period Analysis**: Handles multiple stratigraphic periods simultaneously
- **Flexible Data Input**: Supports various data formats (Excel, CSV, pandas DataFrame)
- **Professional Output**: Generates formatted tables with both English and Chinese headers

### Calculated Metrics
1. **Mudstone Thickness**: Cumulative thickness for lithology containing '泥岩'
2. **Stratigraphic Thickness**: Difference between bottom depth (底深) and top depth (顶深)  
3. **Mud-to-layer Ratio**: Mudstone thickness divided by stratigraphic thickness
4. **Average Geochemical Properties**: 
   - TOC (Total Organic Carbon)
   - S1 (Free hydrocarbons)
   - Brittleness Index
   - Ro (Vitrinite Reflectance)

### Supported Stratigraphic Periods
- 沙三下 (Sha-3 Lower)
- 沙四上晚期 (Sha-4 Upper Late)
- 沙四上中期 (Sha-4 Upper Middle)
- 沙四上早期 (Sha-4 Upper Early)

## Installation

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Usage

#### 1. Basic Usage with Sample Data
```python
from well_analyzer import WellDataAnalyzer, load_sample_data, create_sample_intervals

# Initialize analyzer
analyzer = WellDataAnalyzer()

# Load sample data
data = load_sample_data()
intervals = create_sample_intervals()

# Perform analysis
results = analyzer.analyze_well_data(data, intervals)

# Generate summary tables
summary_tables = analyzer.generate_summary_tables()

# Export results
analyzer.export_results('results.xlsx', format='excel')
```

#### 2. Custom Data Analysis
```python
import pandas as pd

# Prepare your data
custom_data = pd.DataFrame({
    'well_name': ['Well_1', 'Well_1', 'Well_2'],
    'depth': [1000, 1050, 1000],
    'lithology': ['泥岩', '砂岩', '泥岩'],
    'TOC': [2.5, 1.2, 3.1],
    'S1': [1.5, 0.8, 1.9],
    'brittleness_index': [0.4, 0.7, 0.3],
    'Ro': [0.9, 0.7, 1.1],
    'thickness': [50, 50, 50]  # Optional: thickness column
})

# Define intervals for each well and stratigraphic period
custom_intervals = {
    'Well_1': {
        '沙三下': (1000, 1200),
        '沙四上晚期': (1200, 1400)
    },
    'Well_2': {
        '沙三下': (1000, 1150)
    }
}

# Analyze
analyzer = WellDataAnalyzer()
results = analyzer.analyze_well_data(custom_data, custom_intervals)
```

## Data Format Requirements

### Input Data Structure
Your input DataFrame should contain the following columns:

| Column | Description | Type | Required |
|--------|-------------|------|----------|
| `well_name` | Well identifier | string | Yes |
| `depth` | Depth measurement (m) | float | Yes |
| `lithology` | Lithology description in Chinese | string | Yes |
| `TOC` | Total Organic Carbon | float | Optional |
| `S1` | Free hydrocarbons | float | Optional |
| `brittleness_index` | Brittleness Index (0-1) | float | Optional |
| `Ro` | Vitrinite Reflectance | float | Optional |
| `thickness` | Layer thickness (m) | float | Optional |

### Interval Definition Structure
```python
intervals = {
    'well_name': {
        'stratigraphic_period': (top_depth, bottom_depth),
        # ... more periods
    },
    # ... more wells
}
```

Example:
```python
intervals = {
    '井1': {
        '沙三下': (1000, 1200),
        '沙四上晚期': (1200, 1400),
        '沙四上中期': (1400, 1600),
        '沙四上早期': (1600, 1800)
    }
}
```

## Output Format

### Summary Table Columns (Chinese)
- **井名**: Well Name
- **泥岩厚度**: Mudstone Thickness (m)
- **地层厚度**: Stratigraphic Thickness (m)  
- **泥地比**: Mud-to-layer Ratio
- **平均TOC**: Average TOC
- **平均S1**: Average S1
- **平均脆性指数**: Average Brittleness Index
- **平均Ro**: Average Ro

### Export Formats
- **Excel**: Separate worksheets for each stratigraphic period
- **CSV**: Separate files for each stratigraphic period

## Example Results

```
地层时期: 沙三下
──────────────────────────────────────
井名    泥岩厚度  地层厚度  泥地比    平均TOC
井1      85.0   200.0   0.425   2.234
井2      92.5   200.0   0.463   2.456
井3      78.0   200.0   0.390   2.123
```

## API Reference

### WellDataAnalyzer Class

#### Methods

- `__init__()`: Initialize the analyzer
- `identify_lithology(lithology_text)`: Identify lithology type from text
- `calculate_mudstone_thickness(data, top_depth, bottom_depth)`: Calculate mudstone thickness
- `calculate_stratigraphic_thickness(top_depth, bottom_depth)`: Calculate stratigraphic thickness
- `calculate_mud_to_layer_ratio(mudstone_thickness, stratigraphic_thickness)`: Calculate ratio
- `calculate_average_attributes(data, top_depth, bottom_depth)`: Calculate average attributes
- `analyze_well_data(data, well_intervals)`: Perform complete analysis
- `generate_summary_tables()`: Generate formatted summary tables
- `export_results(output_file, format)`: Export results to file

#### Properties
- `stratigraphic_periods`: List of supported stratigraphic periods
- `results`: Dictionary containing analysis results

## File Structure

```
well_data_analysis/
├── well_analyzer.py              # Main analysis module
├── Well_Data_Analysis_Demo.ipynb # Comprehensive demonstration notebook
└── README.md                     # This documentation file
```

## Error Handling

The solution includes robust error handling for:
- Missing or invalid data
- Empty depth intervals
- Missing attribute columns
- File export errors

## Extending the Solution

### Adding New Stratigraphic Periods
```python
analyzer = WellDataAnalyzer()
analyzer.stratigraphic_periods.extend(['新地层时期1', '新地层时期2'])
```

### Adding New Lithology Types
Modify the `identify_lithology` method to recognize additional lithology patterns.

### Custom Attribute Calculations
Extend the `calculate_average_attributes` method to include additional geochemical or petrophysical properties.

## Contributing

This solution is designed to be easily extensible. When contributing:

1. Follow the existing code structure and naming conventions
2. Include appropriate error handling
3. Add docstrings for new methods
4. Update this README if adding new features

## License

This project is part of the ai-projects repository and follows the same licensing terms.

## Support

For questions or issues, please refer to the demonstration notebook (`Well_Data_Analysis_Demo.ipynb`) which includes comprehensive examples and usage patterns.