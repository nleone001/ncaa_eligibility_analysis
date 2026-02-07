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
- Wrestlers whose most recent appearance was Sr (any year); we do not exclude based on a possible SSr return
- Wrestlers whose most recent appearance was Jr in 2022 or earlier (had opportunity for Sr/SSr but didn't return)
- And so on for earlier eligibility years

We **exclude**:

- Wrestlers who last competed as Fr in 2024–2025 (could still AA as So/Jr/Sr/SSr)
- Wrestlers who last competed as So in 2023–2025 (could still AA as Jr/Sr/SSr)
- Wrestlers who last competed as Jr in 2023–2025 (could still AA as Sr/SSr)

We do *not* exclude wrestlers who last competed as Sr (e.g. in 2024–2025) based on a possible return as SSr; we count their career as complete through their senior year.

**Full career in window.** We also require that a wrestler's *entire* career falls within the dataset window (2000–2025). For each AA (each row), the year must be in the allowed range for that eligibility class: Fr AA year in 2000–2021 (Fr year − 1 ≥ 1999, Fr year + 4 ≤ 2025), So in 2001–2022, Jr in 2002–2023, Sr in 2003–2024, SSr in 2004–2025. If any appearance falls outside these bounds, we exclude the wrestler—e.g. a So in 2000 implies Fr was 1999, before the window, so that wrestler is excluded.

![Eligible AA year ranges by class (complete career window)]({{ site.baseurl }}/charts/career_window_timeline.png)

*Wrestlers must have all AA appearances within these windows to be included in analysis.*

This ensures we're counting complete careers that are fully observable. Our tier counts (1×, 2×, 3×, 4×, 5× AA) represent wrestlers' final career totals.

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

For each tier (1×, 2×, 3×, 4×, 5× AA), the tables below show the **combinations of eligibility years** in which wrestlers earned their All-American finishes. Only combinations that appear in the data are listed; each table is sorted from most common to least. ● = AA in that eligibility year.

{% capture report_02_combos %}{% include report_02_eligibility_combos.md %}{% endcapture %}
{{ report_02_combos | markdownify }}

## When National Championships were won (by eligibility)

Same idea for **national champions** (place = 1): for each tier (1× NC, 2× NC, etc.), the tables show the combinations of eligibility years in which wrestlers won titles. Sorted by most common to least. ● = NC in that eligibility year.

{% capture report_02_nc_combos %}{% include report_02_nc_eligibility_combos.md %}{% endcapture %}
{{ report_02_nc_combos | markdownify }}

## Multi-weight All-Americans

Wrestlers who have earned an All-American finish (place 1–8) in **more than one weight class** are a distinct subset of the elite: they moved weights at some point and still placed at NCAAs.

Of **{{ site.data.report_02_stats.n_unique_wrestlers }}** unique wrestlers with complete careers who have placed at the NCAA tournament (2000–2025), **{{ site.data.report_02_stats.n_multi_weight_aa }}** have All-Americaned in at least two different weight classes.

### Count of AAs at n unique weight classes

Most multi-weight All-Americans competed at exactly two weight classes. The rare feat of placing at four different weights was accomplished by only one wrestler in the dataset: **Kyle Dake**, who famously won national titles at 141, 149, 157, and 165 (2009–2013).

| Unique weight classes | Wrestlers |
|:----------------------|----------:|
| 2 | {{ site.data.report_02_stats.multi_weight_by_n.2 }} |
| 3 | {{ site.data.report_02_stats.multi_weight_by_n.3 }} |
| 4 | {{ site.data.report_02_stats.multi_weight_by_n.4 }} |

### Weight-change direction and placement impact

For wrestlers who AAd at two or more weights, we examine each *transition*—a consecutive pair of AA finishes in different years where the wrestler changed weight. There are **{{ site.data.report_02_stats.weight_move_stats.n_transitions }}** such transitions in the data.

| Direction | Transitions | Place improved | Place worse | Same place |
|:----------|------------:|---------------:|------------:|-----------:|
| **Moving up** | {{ site.data.report_02_stats.weight_move_stats.moves_up }} | {{ site.data.report_02_stats.weight_move_stats.up_improved }} ({{ site.data.report_02_stats.weight_move_stats.pct_up_improved }}%) | {{ site.data.report_02_stats.weight_move_stats.up_worse }} ({{ site.data.report_02_stats.weight_move_stats.pct_up_worse }}%) | {{ site.data.report_02_stats.weight_move_stats.up_same }} |
| **Moving down** | {{ site.data.report_02_stats.weight_move_stats.moves_down }} | {{ site.data.report_02_stats.weight_move_stats.down_improved }} ({{ site.data.report_02_stats.weight_move_stats.pct_down_improved }}%) | {{ site.data.report_02_stats.weight_move_stats.down_worse }} ({{ site.data.report_02_stats.weight_move_stats.pct_down_worse }}%) | {{ site.data.report_02_stats.weight_move_stats.down_same }} |

**Findings:**

- **Weight changes are almost always upward.** The vast majority of transitions ({{ site.data.report_02_stats.weight_move_stats.moves_up }} out of {{ site.data.report_02_stats.weight_move_stats.n_transitions }}) involve moving to a higher weight class, reflecting natural growth over a career.
- **Moving up: more improvement than regression.** Among wrestlers who moved up, about 57% improved their placement, ~23% placed worse, and ~20% placed the same. So moving up tends to be associated with improvement, not decline.
- **Moving down: small sample, but high improvement rate.** Only 15 transitions involve moving down in weight. Of those, 11 improved and 2 placed worse. The small sample makes it hard to draw a strong trend, but there is no evidence that moving down leads to worse outcomes—if anything, the improvement rate is higher. Wrestlers who move down may be finding a better fit at a lower weight.

[← Back to table of contents]({{ site.baseurl }}/)

</div>
