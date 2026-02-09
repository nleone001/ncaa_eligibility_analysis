---
layout: default
title: Report 03 — Bracket/Year Seed/Placement Stats
---

<div class="container" markdown="1">

# Bracket/Year Seed/Placement Stats

**Analyzing seed performance and bracket unpredictability across 25 years of NCAA Wrestling Championships.**

This report focuses on bracket and year-level statistics related to seeding and placement, examining how wrestlers perform relative to their seeds and identifying trends in bracket unpredictability over time.

## Seed-Placement Differential by Year

The seed-placement differential measures how wrestlers perform relative to their seeds. A positive differential means a wrestler outperformed their seed (e.g., seeded 4th, placed 1st = +3), while a negative differential means they underperformed (e.g., seeded 1st, placed 3rd = -2). For unseeded wrestlers, we assume the highest non-seed value for that year (13 until 2014, 17 until 2019, 33 from 2019 onward).

The sum of all differentials for a given year provides insight into overall bracket unpredictability: higher sums indicate more upsets and unexpected performances, while lower sums suggest more "chalk" (seeds holding true).

![Seed-Placement Differential Sum by Year]({{ site.baseurl }}/charts/seed_placement_differential_by_year.png)

*Sum of all seed-placement differentials for each year (2000-2025). Higher values indicate more bracket unpredictability.*

## Chalk Placements

"Chalk" refers to brackets where seeds hold true—wrestlers finish exactly where they were seeded. This analysis counts year/weight combinations where placement matches seeds perfectly for each match type:

- **Final**: Seeds 1-2 finish in places 1-2
- **3rd place match**: Seeds 3-4 finish in places 3-4
- **5th place match**: Seeds 5-6 finish in places 5-6
- **7th place match**: Seeds 7-8 finish in places 7-8

Hover over a row to see a preview of matches. Click a row to expand and view all year/weight combinations and wrestlers.

{% capture chalk_table %}{% include report_03_chalk_table.md %}{% endcapture %}
{{ chalk_table | markdownify }}

**Takeaway:** The finals are the most predictable match—73 times across 25 years, the top two seeds met in the championship match. Lower placement matches become increasingly unpredictable, with only 3 instances of seeds 7-8 finishing in places 7-8.

## Most Chalk Brackets

To identify the most predictable brackets across all 25 years, we analyze two metrics:

1. **Sum of Differentials**: The sum of all seed-placement differentials for a bracket. A sum of 0 means all 8 seeds placed in the top 8 (though not necessarily in order).
2. **Exact Matches**: Count of wrestlers who finished exactly where they were seeded (seed 1 → place 1, seed 2 → place 2, etc.).

### Distribution of Chalk Metrics

![Sum Differential Distribution]({{ site.baseurl }}/charts/chalk_sum_differential_histogram.png)

*Distribution of seed-placement differential sums across all 250 brackets (25 years × 10 weights). Lower sums indicate more predictable brackets where seeds held true.*

![Exact Matches Distribution]({{ site.baseurl }}/charts/chalk_exact_matches_histogram.png)

*Distribution of exact seed-place matches across all brackets. No bracket achieved perfect chalk (8/8 exact matches). The best was 5/8 exact matches, achieved in only 8 brackets.*

**Key Findings:**
- **8 brackets** achieved a perfect sum of 0 (all 8 seeds placed in top 8)
- **No bracket** achieved perfect chalk (8/8 exact matches)
- **Best performance**: 5/8 exact matches (achieved in 8 brackets)
- **Most common**: 1 exact match per bracket (72 out of 250 brackets)
- **Mean**: 1.6 exact matches per bracket

### Chalk metrics: top results

Tables below show seed-placement sum (rows for Sum 0, 1, 2) and exact seed-place matches (rows for 4/8 and 5/8). Click a row to expand and see the full list of brackets and podium (1st–8th) with wrestler and seed for each.

{% capture chalk_details %}{% include report_03_chalk_details_tables.md %}{% endcapture %}
{{ chalk_details | markdownify }}

## Brackets with Most All-Americans by Eligibility Class

Which brackets had the most All-Americans from each eligibility class? This analysis identifies the year/weight combinations that achieved the maximum count for Freshmen, Sophomores, Juniors, Seniors, and Super Seniors.

Click a row to expand and view the complete wrestler details for each bracket, showing placement, name, and eligibility class.

{% capture max_aa_table %}{% include report_03_max_aa_brackets_table.md %}{% endcapture %}
{{ max_aa_table | markdownify }}

**Takeaway:** Seniors dominate the podium—9 different brackets achieved the maximum of 6 Senior All-Americans. Freshmen are the rarest, with only one bracket (2014 125lbs) achieving the maximum of 5 Freshman All-Americans. Super Seniors, made possible by COVID eligibility extensions, achieved their maximum (6) in 2025 285lbs.

## Seed Distribution by Placement Position

How do seeds correlate with final placement? These histograms show the distribution of seeds for each of the 8 podium positions, revealing which seeds are most likely to achieve each placement.

![Seed Distribution by Placement Position]({{ site.baseurl }}/charts/seed_distribution_by_placement.png)

*Histograms showing seed distribution for each placement position (1st through 8th). Red dashed line indicates mean seed, green dashed line indicates median seed. Higher placements (1st-3rd) are dominated by top seeds, while lower placements (7th-8th) show more unseeded wrestlers.*

**Key Insights:**
- **1st Place**: Mean seed = 2.32, Median = 2. Top seeds dominate championships.
- **2nd Place**: Mean seed = 3.36, Median = 2. Still heavily favored by top seeds.
- **3rd Place**: Mean seed = 4.26, Median = 4. Seeds 3-4 are most common.
- **4th Place**: Mean seed = 5.57, Median = 5. More spread across seeds.
- **5th-6th Place**: Mean seeds around 6-7. Middle seeds are most common.
- **7th-8th Place**: Mean seeds 7.5-9.8. Lower seeds and unseeded wrestlers become more common, with 8th place having the highest mean seed (9.84) and most unseeded wrestlers (61).

[← Back to table of contents]({{ site.baseurl }}/)

</div>
