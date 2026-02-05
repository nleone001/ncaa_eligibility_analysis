---
layout: default
title: NCAA Wrestling Eligibility Analysis
---

<div class="container">

# NCAA Wrestling Eligibility Analysis

A data-driven analysis of NCAA Division I Wrestling All-Americans from 2000–2025, focusing on eligibility year patterns.

## Reports

- [**Full Analysis: All-Americans by Eligibility Year**](report.html) — Who makes the podium? How does experience impact success?

## About This Project

This project analyzes 25 years of NCAA Wrestling All-American data to understand patterns in eligibility classifications. All analysis is performed in Python and can be reproduced by running a single script.

### Quick Stats

- **2,000** All-American finishes analyzed
- **1,076** unique wrestlers
- **26** tournament years (2000–2025)

## Reproducibility

To regenerate all charts and tables:

```bash
cd ncaa-eligibility-analysis
pip install -r requirements.txt
python notebooks/analysis.py
```

All outputs are saved to `/charts` and `/tables` directories.

---

<footer>
<p><a href="https://github.com/nleone001/ncaa_eligibility_analysis">View on GitHub</a></p>
</footer>

</div>
