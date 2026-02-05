---
layout: default
title: NCAA Wrestling Eligibility Analysis
---

<div class="container">

# NCAA Wrestling All-Americans: An Eligibility Year Analysis

<p class="meta">Data spans 2000–2025 | 2,000 All-American finishes analyzed</p>

<p class="lead">Who makes the podium at the NCAA Wrestling Championships? This analysis examines 25 years of All-American data to understand how eligibility year impacts success at the highest level of collegiate wrestling.</p>

## Key Findings

**Experience matters.** Seniors and juniors account for nearly two-thirds of all All-American finishes, with seniors alone representing 34.7% of the total. Freshmen, despite the attention they receive, make up just 11.8% of All-Americans.

**The champion rate increases with experience.** While freshmen who make All-American have a 9.3% chance of winning a national title, that rate climbs steadily: 10.6% for sophomores, 12.9% for juniors, and 14.6% for seniors.

## National Champions by Eligibility Year

The distribution of national champions tells a clear story: experience correlates strongly with winning titles.

<figure>
<img src="{{ site.baseurl }}/charts/champions_by_eligibility.png" alt="Bar chart showing national champions by eligibility year">
<figcaption>National champions by eligibility year, 2000–2025. Seniors have won more titles than any other class.</figcaption>
</figure>

Over this 25-year period:
- **101 seniors** won national titles (40.4% of all champions)
- **78 juniors** won national titles (31.2%)
- **45 sophomores** won national titles (18.0%)
- **22 freshmen** won national titles (8.8%)
- **4 super seniors** won national titles (1.6%)

## All-Americans by Eligibility Year

The broader All-American picture shows a similar pattern, with upper classmen dominating the podium.

<figure>
<img src="{{ site.baseurl }}/charts/all_americans_by_eligibility.png" alt="Bar chart showing all All-Americans by eligibility year">
<figcaption>All-American finishes (places 1–8) by eligibility year, 2000–2025.</figcaption>
</figure>

## Summary Table

| Eligibility Year | All-Americans | % of Total | National Champions | Champion Rate |
|:-----------------|:-------------:|:----------:|:------------------:|:-------------:|
| Freshman         | 237           | 11.8%      | 22                 | 9.3%          |
| Sophomore        | 423           | 21.1%      | 45                 | 10.6%         |
| Junior           | 603           | 30.1%      | 78                 | 12.9%         |
| Senior           | 694           | 34.7%      | 101                | 14.6%         |
| Super Senior     | 43            | 2.1%       | 4                  | 9.3%          |

## Methodology

This analysis includes all NCAA Division I Wrestling All-American finishes (places 1–8) from 2000 through 2025. Eligibility year classifications are as recorded in official NCAA records.

**Data cleaning notes:**
- Eligibility years were standardized (e.g., lowercase corrections, whitespace trimming)
- Super seniors (SSr) represent athletes using additional eligibility, including COVID-era extensions

---

<footer>
<p>Analysis generated from <code>notebooks/analysis.py</code>. Data source: NCAA Wrestling Championships records.</p>
<p>Rerun the analysis script to regenerate all charts and tables from the source data.</p>
</footer>

</div>
