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
├── docs/                     # Current GitHub Pages site (live)
│   ├── _config.yml
│   ├── _layouts/
│   ├── index.md
│   ├── report.md             # Main report (unchanged)
│   └── styles.css
├── site/                     # Multi-report site (TOC + reports/)
│   ├── index.md              # Landing / table of contents
│   ├── styles.css
│   └── reports/
│       ├── report_01_overview.md
│       └── report_02_placeholder.md
├── requirements.txt
└── README.md
```

The live site is currently served from `docs/`. The `site/` directory holds the new structure (landing page with table of contents and multiple report pages) for when you switch publishing to it.

## Analysis Ideas

- 1. **Total National Champs and AAs by eligibility**
- 2. **Trend over time of NC and AAs by eligibliity**
- 3. **Multi-AA weight changes** % repeat AA after moving up/down
- 4. **Returning champs (<Sr) losing title % by class**
- 5. **Brackets/Years with most 1-2 finals**
- 6. **Most "Chalk" brackets and years** 
- 7. **invidual years/brackets with most Fr -> Sr AAs**
- 8. **oldest and youngest bracket/year**
- 9. **Average placing age over time** Exodus / barbarians @ gate
- 10. **Most Unseeded AAs per year/bracket** pre 2019
- 11. **highest seed placing for each podium position** pre 2019
- 12. **wrestlers with aesthetic improvement (3-4 year progression)** Eric Larkin 4-3-2-1
- 13. **overperforming/underperforming schools/individuals by seed and placement**
- 14. **last chance wrestlers - wrestlers who AAd on their last year of eligibility**
- 15. **covid beneficiaries - AAs in SSr year**
- 16. **General AAs and NC by school - total and over time**
- 17. **progression of Fr/So AAs by school**
- 18. **Standout class of 2010 (so 2008, jr 2009, sr 2010)**


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

The report pages pull stats from `docs/_data/report_stats.json` and `docs/_data/report_02_stats.json`, written when you run the analysis. To see reports with numbers rendered, use the live site or build the Jekyll site from `docs/` (e.g. `jekyll build` or GitHub Pages).

## View the Report

Visit the [live site](#) or open `docs/report.md` locally (Liquid will only render when the site is built).

## License

Data analysis for educational purposes. NCAA data sourced from public records.
