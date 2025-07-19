# Step 25: Analyze Core NPI Data and Perform Data Quality Checks

## Overview

This script performs comprehensive analysis and data quality checks on the core NDH NPI tables after data transformation and index creation. It should be run after Step15 (data transformation) and Step20 (index creation).

## Purpose

Provides comprehensive insights into:
- Data quality and completeness
- Processing efficiency and trends
- Change patterns and analysis
- Error identification and resolution
- Performance metrics and monitoring

## What it does

The script performs 20 analytical queries across 7 phases:

### Phase 1: Processing Run Summary (Steps 1-2)
- Latest processing run details and performance metrics
- Processing trends over the last 10 runs
- Change type distribution and percentages

### Phase 2: NPI Distribution Analysis (Steps 3-5)
- Overall NPI distribution by entity type
- Enumeration trends by year since 2005
- Recent update patterns by month
- Deactivation and reactivation statistics

### Phase 3: Individual Record Analysis (Steps 6-8)
- Individual record completeness analysis
- Name component distribution and quality
- NPI-to-Individual relationship metrics
- Sex code distribution and demographics

### Phase 4: Organizational Hierarchy Analysis (Steps 9-11)
- Organizational structure and parent relationships
- Top parent organizations by child count
- Authorized official analysis and distribution
- Subpart percentage and hierarchy depth

### Phase 5: Change Pattern Analysis (Steps 12-14)
- Change type distribution for latest run
- Individual record change patterns
- Parent relationship change analysis
- Trend identification and anomaly detection

### Phase 6: Error Analysis and Data Quality (Steps 15-17)
- Error summary by type and frequency
- Data completeness checks across tables
- Data integrity validation and orphaned records
- Quality score calculations

### Phase 7: Performance and Completeness Metrics (Steps 18-20)
- Source vs processed data comparison
- Relationship coverage analysis
- Processing efficiency metrics and throughput
- Error rates and quality indicators

## Usage

### Dry-run mode (recommended first):
```bash
cd nppes_main/post_import_scripts
python Step25_analyze_npi_data.py
```

### Production mode:
Edit the script and change `is_just_print = False` on line 25, then run:
```bash
python Step25_analyze_npi_data.py
```

## Key Features

- **Comprehensive Coverage**: Analyzes all aspects of the NPI pipeline
- **Data Quality Focus**: Identifies completeness and integrity issues
- **Trend Analysis**: Shows patterns over time and across runs
- **Performance Monitoring**: Tracks processing efficiency
- **Error Detection**: Highlights data quality problems
- **Actionable Insights**: Provides specific recommendations

## Analysis Areas

### Data Quality Metrics
- **Completeness**: Percentage of required fields populated
- **Integrity**: Foreign key consistency and referential integrity
- **Accuracy**: Data format validation and business rule compliance
- **Consistency**: Cross-table data alignment

### Processing Performance
- **Throughput**: NPIs processed per minute
- **Efficiency**: Processing time trends
- **Error Rates**: Percentage of records with issues
- **Change Ratios**: New vs updated vs deactivated NPIs

### Business Intelligence
- **Distribution Analysis**: Individual vs organizational NPIs
- **Hierarchy Insights**: Parent-child relationships
- **Geographic Patterns**: State and regional analysis
- **Temporal Trends**: Changes over time

### Change Management
- **Incremental Processing**: Effectiveness of change detection
- **Update Patterns**: Types and frequency of changes
- **Error Tracking**: Resolution of data quality issues
- **Audit Trail**: Complete change history

## Output Interpretation

### Processing Run Summary
- **Processing Time**: Should be consistent or improving
- **Change Percentages**: Typical monthly updates are 1-3%
- **Error Rates**: Should be < 0.1% for quality data

### Data Quality Indicators
- **Completeness > 95%**: Good data quality
- **Integrity Issues = 0**: No orphaned records
- **Error Count Trends**: Should be stable or decreasing

### Performance Benchmarks
- **Processing Speed**: > 1000 NPIs/minute is good
- **Coverage**: > 99% of source data processed
- **Relationship Links**: > 95% of NPIs have relationships

## Troubleshooting

### High Error Rates
- Check source data quality
- Review parent organization matching logic
- Validate name normalization rules

### Poor Performance
- Verify indexes are created (Step20)
- Check database resource utilization
- Review query execution plans

### Data Completeness Issues
- Investigate source data gaps
- Review transformation logic
- Check field mapping accuracy

## Prerequisites

- Step15 (data transformation) must be completed successfully
- Step20 (index creation) should be completed for optimal performance
- NDH and intake schemas must exist with populated tables

## Dependencies

- plainerflow
- PostgreSQL database connection
- Sufficient database permissions for analysis queries

## Output Files

The script generates comprehensive analysis results including:
- Summary statistics tables
- Trend analysis charts (when visualized)
- Data quality scorecards
- Performance metrics dashboards

## Monitoring and Alerting

Use the results to set up monitoring for:
- Processing time thresholds
- Error rate limits
- Data completeness minimums
- Change pattern anomalies

## Next Steps

Based on analysis results:
1. **Address Data Quality Issues**: Fix identified problems
2. **Optimize Performance**: Tune slow queries or processes
3. **Update Business Rules**: Refine validation logic
4. **Schedule Regular Analysis**: Set up automated monitoring
