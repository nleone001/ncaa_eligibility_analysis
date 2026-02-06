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

## Analysis Ideas

- **Total National Champs and AAs by eligibility**
- **Trend over time of NC and AAs by eligibliity**
- **Multi-AA weight changes** % repeat AA after moving up/down
- **Returning champs (<Sr) losing title % by class**
- **Brackets/Years with most 1-2 finals**
- **Most "Chalk" brackets and years** 
- **invidual years/brackets with most Fr -> Sr AAs**
- **oldest and youngest bracket/year**
- **Average placing age over time** Exodus / barbarians @ gate
- **Most Unseeded AAs per year/bracket** pre 2019
- **highest seed placing for each podium position** pre 2019
- **wrestlers with aesthetic improvement (3-4 year progression)** Eric Larkin 4-3-2-1
- **overperforming/underperforming schools/individuals by seed and placement**
- **last chance wrestlers - wrestlers who AAd on their last year of eligibility**
- **covid beneficiaries - AAs in SSr year**
- **General AAs and NC by school - total and over time**
- **progression of Fr/So AAs by school**
- **Standout class of 2010 (so 2008, jr 2009, sr 2010)**


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
