# NCAA Wrestling Eligibility Analysis

A reproducible, data-driven analysis of NCAA Division I Wrestling All-Americans (2000-2025), focusing on eligibility year patterns.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis (generates all charts and tables)
python notebooks/analysis.py
```

## Project Structure

```
ncaa-eligibility-analysis/
├── data/
│   └── raw_data.csv          # Source data
├── notebooks/
│   └── analysis.py           # All analysis code
├── charts/                   # Generated PNG charts
├── tables/                   # Generated markdown tables
├── site/                     # GitHub Pages site
│   ├── _config.yml
│   ├── _layouts/
│   ├── index.md
│   ├── report.md
│   └── styles.css
├── requirements.txt
└── README.md
```

## Key Findings

- **Seniors dominate**: 34.7% of All-Americans are seniors
- **Experience wins titles**: Senior champion rate is 14.6% vs 9.3% for freshmen
- **2,000 All-American finishes** analyzed across 26 years

## Reproducibility

This project is designed for full reproducibility:

1. **Python does all analysis** - No manual calculations or Google Sheets logic
2. **Charts saved to `/charts`** - All figures exported as PNG
3. **Tables exported to `/tables`** - All summary tables as markdown
4. **Single script regeneration** - Run `analysis.py` to update everything

## Data

Source: NCAA Division I Wrestling Championships records, 2000-2025

| Field | Description |
|-------|-------------|
| Year | Tournament year |
| Weight | Weight class |
| Place | All-American placement (1-8) |
| Wrestler | Athlete name |
| School | Institution |
| Eligibility Year | Fr, So, Jr, Sr, SSr |

## View the Report

Visit the [live site](#) or open `site/report.md` locally.

## License

Data analysis for educational purposes. NCAA data sourced from public records.
