---
layout: default
title: Surviving March Matness: An Analysis of NCAA Wrestling Tournament Chaos
---

<div class="container" markdown="1">

# Surviving March Matness: An Analysis of NCAA Wrestling Tournament Chaos

**Analyzing seed performance and bracket unpredictability across 25 years of NCAA Wrestling Championships.**

This report focuses on bracket and year-level statistics related to seeding and placement, examining how wrestlers perform relative to their seeds and identifying the exceptional times that a tournament went according to plan.

## Executive Summary

- **Finals are the most predictable:** The top two seeds met in the championship match 73 times across 25 years (29% of all finals), while seeds 7-8 finishing in places 7-8 occurred only 3 times
- **No perfect chalk brackets:** Across 250 weight class brackets (25 years × 10 weights), no bracket achieved perfect chalk (8/8 seeds finishing exactly where seeded), with the best performance being 5/8 exact matches in only 8 brackets
- **Top seeds dominate championships:** First-place finishers had a mean seed of 2.32, with the #1 and #2 seeds accounting for the vast majority of champions
- **Efforts to reduce chaos:** Seeding has changed twice since 2000: expanding from 12 to 16 seeded wrestlers in 2014 and lal wrestlers seeded starting in 2019. 

## Seed-Placement Differential by Year

The seed-placement differential measures how wrestlers perform relative to their seeds. A positive differential means a wrestler outperformed their seed (e.g., seeded 4th, placed 1st = +3), while a negative differential means they underperformed (e.g., seeded 1st, placed 3rd = -2). For unseeded wrestlers, we assume the highest non-seed value for that year (13 until 2014, 17 until 2019).

The sum of all differentials for a given year provides insight into overall bracket unpredictability: higher sums indicate more upsets and unexpected performances, while lower sums suggest more "chalk" (seeds holding true).

![Seed-Placement Differential Sum by Year]({{ site.baseurl }}/charts/seed_placement_differential_by_year.png)

*Sum of all seed-placement differentials for each year (2000-2025). Higher values indicate more bracket unpredictability.*

**Year-by-year trends:** The most chaotic tournaments occurred in 2021 (differential sum: 227) and 2015 (204), years marked by numerous upsets and unseeded wrestlers making deep runs. In contrast, 2008 (69), 2019 (90), and 2003 (95) saw the most chalk results, with top seeds generally performing as expected. There does not appear to be any linear trend to each season's performance relative to seed. The championship tournament chaos, often termed "March Matness", remains an unpredictable end to the NCAA wrestling season.

## Seed Distribution by Placement Position

Before examining specific chalk outcomes, it's essential to understand the baseline relationship between seeds and placements. How often do certain seeds achieve each placement position? These histograms reveal the fundamental patterns that define tournament predictability.

![Seed Distribution by Placement Position]({{ site.baseurl }}/charts/seed_distribution_by_placement.png)

*Histograms showing seed distribution for each placement position (1st through 8th). Red dashed line indicates mean seed, green dashed line indicates median seed. Higher placements (1st-3rd) are dominated by top seeds, while lower placements (7th-8th) show more unseeded wrestlers.*

**Key Insights:**
- **1st Place**: Mean seed = 2.32, Median = 2. Top seeds dominate championships, with the #1 and #2 seeds accounting for the overwhelming majority of champions. Only rarely do seeds outside the top 4 win titles, with the highest ever seed to win the championship being 13-seed Cody Brewer winning the 2015 133 weight class.
- **2nd Place**: Mean seed = 3.36, Median = 2. Still heavily favored by top seeds, though slightly more variability than first place.
- **3rd Place**: Mean seed = 4.26, Median = 4. Seeds 3-4 are most common, aligning closely with expectations for third-place finishers.
- **4th Place**: Mean seed = 5.57, Median = 5. More spread across seeds, with notable representation from seeds 3-7.
- **5th-6th Place**: Mean seeds around 6-7. Middle seeds are most common, with increasing frequency of unseeded wrestlers beginning to appear.
- **7th-8th Place**: Mean seeds 7.5-9.8. Lower seeds and unseeded wrestlers become increasingly common, with 8th place having the highest mean seed (9.84) and the most unseeded wrestlers (61 across all brackets).

**Implications for chalk analysis:** This distribution helps explain why lower placement matches rarely go chalk—by 7th-8th place, unseeded wrestlers and lower seeds dominate the field, making exact seed-to-placement matches statistically unlikely. The tight clustering of top seeds in championship and runner-up positions, however, creates favorable conditions for finals to go chalk.

## Chalk Placements

Building on the seed distribution patterns above, we now examine how often placement matches produce "chalk" outcomes—where wrestlers finish exactly where they were seeded. This analysis counts year/weight combinations where placement matches seeds perfectly for each match type:

- **Final**: Seeds 1-2 finish in places 1-2
- **3rd place match**: Seeds 3-4 finish in places 3-4
- **5th place match**: Seeds 5-6 finish in places 5-6
- **7th place match**: Seeds 7-8 finish in places 7-8

Hover over a row to see a preview of matches. Click a row to expand and view all year/weight combinations and wrestlers.

{% capture chalk_table %}{% include report_03_chalk_table.md %}{% endcapture %}
{{ chalk_table | markdownify }}

**Takeaway:** The finals are the most predictable match—73 times across 25 years (29% of all finals), the top two seeds met in the championship match. This aligns with the seed distribution data showing #1 and #2 seeds dominating the top two placements. Lower placement matches become increasingly unpredictable, with only 20 instances of seeds 3-4 finishing in places 3-4 (8%), and just 3 instances of seeds 7-8 finishing in places 7-8 (1.2%). 

## Most Chalk Brackets

Having examined individual match types, we now turn to complete brackets. To identify the brackets were seeds proved to be the most accurate across all 25 years, we analyze two complementary metrics:

1. **Sum of Differentials**: The sum of all seed-placement differentials for a bracket. A sum of 0 means all 8 seeds placed in the top 8 (though not necessarily in the correct order).
2. **Exact Matches**: Count of wrestlers who finished exactly where they were seeded (seed 1 → place 1, seed 2 → place 2, etc.).

**Why both metrics matter:** Sum of differentials measures overall bracket integrity (did the top-8 seeded wrestlers make All-American?), while exact matches measure precision (did they finish in their exact predicted spots?). A bracket can have a low differential sum with few exact matches if seeds shuffle within the top 8, or high exact matches with a moderate sum if unseeded wrestlers place while some seeds miss.

### Distribution of Chalk Metrics

![Sum Differential Distribution]({{ site.baseurl }}/charts/chalk_sum_differential_histogram.png)

*Distribution of seed-placement differential sums across all 250 brackets (25 years × 10 weights). Lower sums indicate more predictable brackets where seeds held true.*

![Exact Matches Distribution]({{ site.baseurl }}/charts/chalk_exact_matches_histogram.png)

*Distribution of exact seed-place matches across all brackets. No bracket achieved perfect chalk (8/8 exact matches). The best was 5/8 exact matches, achieved in only 8 brackets.*

**Key Findings:**
- **8 brackets** achieved a perfect sum of 0 (all 8 seeds placed in top 8)
- **No bracket** achieved perfect chalk (8/8 exact matches)
- **Best performance**: 5/8 exact matches (achieved in 8 brackets)
- **Most common**: 1 exact match per bracket (72 out of 250 brackets, or 29%). 
- **Mean**: 1.6 exact matches per bracket
- **Zero exact matches**: 55 brackets (22%) had no wrestlers finish exactly where seeded

### Chalk metrics: top results

Tables below show seed-placement sum (rows for Sum 0, 1, 2) and exact seed-place matches (rows for 4/8 and 5/8). Click a row to expand and see the full list of brackets and podium (1st–8th) with wrestler and seed for each.

{% capture chalk_details %}{% include report_03_chalk_details_tables.md %}{% endcapture %}
{{ chalk_details | markdownify }}

**Notable example of All 8 seeds finishing as AA:** 
1. 2000 149 weight class: Chalk finals (1. Tony Davis, 2. Adam Tirapelle) and 7th/8th (7. Mike Zadick, 8. Quinn Foster)
2. 2003 133 weight class: Top 4 seeds chalk (1. Logan Stieber, 2. Tony Ramos, 3. Tyler Graff, 4. AJ Schopp)
3. 2014 174 weight class: 5 chalk seeds (1. Chris Perry, 2. Andrew Howe, 5. Matt Brown, 7. Tyler Wilps, 8. Bryce Hammond)

## Brackets with Most All-Americans by Eligibility Class

While not directly a measure of chalk, the eligibility class composition of All-Americans provides insight into bracket dynamics. 

One example we are examing is a weight class exodus: a large group of seniors toeing the line for a final time before clearing the way for a new class the following year. 

Another is the barbarians at the gate: a young group of freshman taking hold of the podium. 

Click a row to expand and view the complete wrestler details for each bracket, showing placement, name, and eligibility class.

{% capture max_aa_table %}{% include report_03_max_aa_brackets_table.md %}{% endcapture %}
{{ max_aa_table | markdownify }}

**Takeaway:** There have been many examples(9) of a weight class exodus: 6 of the 8 All-Americans being in their final year. Only once has a group of freshman taken the majority of podium positions: 2014 125lbs. 

## Conclusion

This comprehensive analysis of 25 years of NCAA Wrestling Championships reveals that true chalk—where seeds finish exactly as predicted—is remarkably rare. Despite 250 bracket opportunities, no weight class has ever achieved perfect chalk (8/8 exact matches), with even the best brackets managing only 5/8 exact matches. The most common result is a single exact match per bracket, occurring in 29% of cases.

**What makes a bracket predictable?** Several factors emerge:
- **Top-seed dominance**: Championships are dominated by #1 and #2 seeds (mean seed 2.32), making finals the most likely chalk match (29% occurrence rate)
- **Progressive unpredictability**: As placement descends, chalk becomes exponentially rarer—3rd place matches go chalk 8% of the time, 7th place matches just 1.2%
- **Unseeded wildcards**: Lower placements (7th-8th) feature numerous unseeded wrestlers, making exact seed matches statistically improbable

**Practical implications:** For fans, bettors, and analysts, these findings underscore the inherent uncertainty of March Matness. Even in the most favorable conditions (top-seeded finalists, senior-heavy brackets), exact seed-to-placement alignment is the exception, not the rule. The smart approach is to expect the top seeds to populate the top placements, but in shuffled order—perfect chalk remains wrestling's white whale.

[← Back to table of contents]({{ site.baseurl }}/)

</div>