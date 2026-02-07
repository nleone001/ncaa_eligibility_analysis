---
layout: default
title: Report 02 — The Journey (Career Arc)
---

<div class="container" markdown="1">

# The Journey: Progression of the NCAA Elite

## Development and career arc

*What does the path from freshman All-American to senior champion actually look like?*

This report explores multi-time All-Americans, aesthetic progressions (improvement every year), and related career-arc analyses.

## Analysis scope and assumptions

### Observable complete careers

This analysis includes only wrestlers whose careers are **observably complete**—meaning they've exhausted their eligibility or enough time has passed that we can be confident they won't return to competition.

We **include**:

- All wrestlers who competed as Super Seniors (final year of eligibility)
- Wrestlers whose most recent appearance was Sr in 2023 or earlier (had opportunity to use SSr eligibility but didn't)
- Wrestlers whose most recent appearance was Jr in 2022 or earlier (had opportunity for Sr/SSr but didn't return)
- And so on for earlier eligibility years

We **exclude**:

- Wrestlers who last competed as Fr in 2024–2025 (could still AA as So/Jr/Sr/SSr)
- Wrestlers who last competed as So in 2023–2025 (could still AA as Jr/Sr/SSr)
- Wrestlers who last competed as Jr in 2023–2025 (could still AA as Sr/SSr)
- Wrestlers who last competed as Sr in 2024–2025 (could still AA as SSr)

This ensures we're counting complete careers. For example, a wrestler who AA'd as a junior in 2025 might return and become a 4× All-American, but we can't know that yet. By filtering to observable complete careers, our tier counts (1×, 2×, 3×, 4×, 5× AA) represent wrestlers' final career totals.

**Result: {{ site.data.report_02_stats.n_complete_careers }} wrestlers with complete, observable careers.**

## Multi-AA funnel

Of **{{ site.data.report_02_stats.n_unique_wrestlers }}** unique wrestlers with complete careers who have placed at the NCAA tournament (2000–2025), **{{ site.data.report_02_stats.n_multi_aa }}** have All-Americaned more than once. The funnel below shows how many wrestlers have **exactly** 1×, 2×, 3×, 4×, or 5× AAs (same counts as the tables below).

![Funnel: unique wrestlers by multi-AA tier (1× through 5× AA)]({{ site.baseurl }}/charts/multi_aa_funnel.png)

*Exactly 1×, 2×, 3×, 4×, 5× AA. Total {{ site.data.report_02_stats.n_unique_wrestlers }} unique wrestlers (complete careers only).*

- **1× AA:** {{ site.data.report_02_stats.funnel.n_1plus }} wrestlers
- **2× AA:** {{ site.data.report_02_stats.funnel.n_2plus }} wrestlers
- **3× AA:** {{ site.data.report_02_stats.funnel.n_3plus }} wrestlers
- **4× AA:** {{ site.data.report_02_stats.funnel.n_4plus }} wrestlers
- **5× AA:** {{ site.data.report_02_stats.funnel.n_5plus }} wrestlers

Roughly half of all wrestlers who ever AA'd did it more than once; while around 10% achieved the elite goal of four All-American finishes. Only a small group of 7 wrestlers achieved an accomplishment likely never to be repeated of earning a fifth All-American finish thanks to the COVID 2020 eligibility extension.

## When All-American was earned (by eligibility)

For each tier (1×, 2×, 3×, 4× AA), the tables below show the **combinations of eligibility years** in which wrestlers earned their All-American finishes. Only combinations that appear in the data are listed; each table is sorted from most common to least. ● = AA in that eligibility year.

{% capture report_02_combos %}{% include report_02_eligibility_combos.md %}{% endcapture %}
{{ report_02_combos | markdownify }}

## When National Championships were won (by eligibility)

Same idea for **national champions** (place = 1): for each tier (1× NC, 2× NC, etc.), the tables show the combinations of eligibility years in which wrestlers won titles. Sorted by most common to least. ● = NC in that eligibility year.

{% capture report_02_nc_combos %}{% include report_02_nc_eligibility_combos.md %}{% endcapture %}
{{ report_02_nc_combos | markdownify }}

## Multi-weight All-Americans

Wrestlers who have earned an All-American finish (place 1–8) in **more than one weight class** are a distinct subset of the elite: they moved weights at some point and still placed at NCAAs.

Of **{{ site.data.report_02_stats.n_unique_wrestlers }}** unique wrestlers with complete careers who have placed at the NCAA tournament (2000–2025), **{{ site.data.report_02_stats.n_multi_weight_aa }}** have All-Americaned in at least two different weight classes.

*Additional sections (aesthetic progressions, defending champions, last-chance seniors, Super Senior performance) will be added as the analysis is completed.*

[← Back to table of contents]({{ site.baseurl }}/)

</div>
