---
layout: default
title: Report 02 — The Journey (Career Arc)
---

<div class="container" markdown="1">

# Report 02: The Journey

## Development and career arc

*What does the path from freshman All-American to senior champion actually look like?*

This report explores multi-time All-Americans, aesthetic progressions (improvement every year), and related career-arc analyses. We start with the funnel: how many of the 1,076 unique wrestlers who have ever AA'd went on to do it again—and again?

## Multi-AA funnel

Of **{{ site.data.report_02_stats.n_unique_wrestlers }}** unique wrestlers who have placed at the NCAA tournament (2000–2025), **{{ site.data.report_02_stats.n_multi_aa }}** have All-Americaned more than once. The funnel below shows how many reached each tier (2×, 3×, 4×, or 5× AA).

![Funnel: unique wrestlers by multi-AA tier (All → 2× → 3× → 4× → 5× AA)]({{ site.baseurl }}/charts/multi_aa_funnel.png)

*Unique wrestlers by multi-AA tier. Top: all 1,076; then wrestlers with 2+ AAs (548), 3+ (266), 4+ (103), 5+ (7).*

- **All wrestlers:** {{ site.data.report_02_stats.n_unique_wrestlers }} unique wrestlers (at least one AA)
- **2× AA:** {{ site.data.report_02_stats.funnel.n_2plus }} wrestlers
- **3× AA:** {{ site.data.report_02_stats.funnel.n_3plus }} wrestlers
- **4× AA:** {{ site.data.report_02_stats.funnel.n_4plus }} wrestlers
- **5× AA:** {{ site.data.report_02_stats.funnel.n_5plus }} wrestlers

Roughly half of all wrestlers who ever AA'd did it more than once; while around 10% achieved the elite goal of four All-American finishes. Only a small group of 7 wrestlers achieved an accomplishment likely never to be repeated of earning a fifth All-American finish thanks to the COVID 2020 eligibility extension.

## When AA was earned (by eligibility)

For each tier (1×, 2×, 3×, 4× AA), the tables below show the **combinations of eligibility years** in which wrestlers earned their All-American finishes. Only combinations that appear in the data are listed; each table is sorted from most common to least. ● = AA in that eligibility year.

{% capture report_02_combos %}{% include report_02_eligibility_combos.md %}{% endcapture %}
{{ report_02_combos | markdownify }}

## When NC was won (by eligibility)

Same idea for **national champions** (place = 1): for each tier (1× NC, 2× NC, etc.), the tables show the combinations of eligibility years in which wrestlers won titles. Sorted by most common to least. ● = NC in that eligibility year.

{% capture report_02_nc_combos %}{% include report_02_nc_eligibility_combos.md %}{% endcapture %}
{{ report_02_nc_combos | markdownify }}

*Additional sections (aesthetic progressions, multi-weight success, defending champions, last-chance seniors, Super Senior performance) will be added as the analysis is completed.*

[← Back to table of contents]({{ site.baseurl }}/)

</div>
