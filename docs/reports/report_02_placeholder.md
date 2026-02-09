---
layout: default
title: Report 02 — The Journey (Career Arc)
---

<div class="container" markdown="1">

# The Journey: Progression of the NCAA Elite
## The Elite Few

Coleman Scott (Oklahoma State, 2005-2008): 8-5-2-1
Frank Molinaro (Penn State, 2009-2012): 8-5-2-1

Two wrestlers, years apart, identical progressions. Four years, four steps up the podium, each finishing their career on top. This is the path wrestling culture celebrates: the blue-collar grind, the steady improvement, the earned reward.

But how common is this path, really?

Before we can talk about the journey from freshman All-American to senior champion, we need to acknowledge how rare it is to have any journey at all.

## The path to Multiple All-American Honors

In the 2000-2025 dataset of 2000 All-Americans, we see 1,076 unique wrestlers earning All-American honors. For some of these wrestlers, though, we do not have the full picture of their career. This AA career analysis will only include wrestlers whose careers are complete and fall entirely within the 2000-2025 window. See appendix for detailed criteria. 

![Eligible AA year ranges by class (complete career window)]({{ site.baseurl }}/charts/career_window_timeline.png)

*Wrestlers must have all AA appearances within these windows to be included in analysis.*

## Multi-AA funnel

Of **{{ site.data.report_02_stats.n_complete_careers }}**  unique wrestlers with complete careers who placed at the NCAA tournament (2000–2025), only **{{ site.data.report_02_stats.n_multi_aa }}** have All-Americaned more than once - these are the wrestlers whose journeys we can truly examine.

![Funnel: unique wrestlers by multi-AA tier (1× through 5× AA)]({{ site.baseurl }}/charts/multi_aa_funnel.png)

*Exactly 1×, 2×, 3×, 4×, 5× AA. Total {{ site.data.report_02_stats.n_unique_wrestlers }} unique wrestlers (complete careers only).*

- **1× AA:** {{ site.data.report_02_stats.funnel.n_1plus }} wrestlers
- **2× AA:** {{ site.data.report_02_stats.funnel.n_2plus }} wrestlers
- **3× AA:** {{ site.data.report_02_stats.funnel.n_3plus }} wrestlers
- **4× AA:** {{ site.data.report_02_stats.funnel.n_4plus }} wrestlers
- **5× AA:** {{ site.data.report_02_stats.funnel.n_5plus }} wrestlers

Roughly half of all wrestlers who ever AA'd did it more than once. Only about 11% achieved the elite goal of four All-American finishes. And just seven wrestlers achieved what may never be repeated: a fifth All-American finish, made possible only by the COVID eligibility extension.


{% capture report_02_combos %}{% include report_02_eligibility_combos.md %}{% endcapture %}
{{ report_02_combos | markdownify }}

**Key patterns:**
- **1× AA:** Nearly half (50%) earn their lone All-American finish as seniors—the "last chance" breakthrough
- **2× AA:** Junior-Senior dominates (53%), but there's significant variety in when wrestlers earn their first AA
- **3x AA:** Sophomore-Junior-Senior represents the majority, again showing that many careers require a freshman year of experience and development to break through and sustain AA finishes


{% capture report_02_nc_combos %}{% include report_02_nc_eligibility_combos.md %}{% endcapture %}
{{ report_02_nc_combos | markdownify }}

**Key patterns:**
- **1× Champion:** Most single-time champions win as seniors (58%) or juniors (26%)
- **2x Champion:** Less than 10% of two-time champions won as a Freshman, again reinforcing that sustained success at the top usually comes later in a wrestler's career
- **3x Champion:** Most three-time champions win after their freshman year. Spencer Lee is the only three-time champion who failed to repeat in his senior year.
- **4× Champion:** Seven wrestlers have achieved four titles. Within our dataset: Kyle Dake, Logan Stieber, Yianni Diakomihalis, Aaron Brooks, and Carter Starocci (who also won a fifth). Pat Smith (1990-1994) and Cael Sanderson (1999-2002) accomplished this feat outside our analysis window.
- **5x Champion:** Only Carter Starocci has achieved this historic feat, thanks to the COVID eligibility extension. This will never be repeated with the current college eligibility rules.  

## Progression Archetypes

Now that we've seen when wrestlers earn their All-American finishes, let's examine how they progress—or don't—across those finishes. 

We classify wrestlers with **complete, observable careers** into progression archetypes based on their AA placement sequences. We are only considering wrestlers with **3+ AAs** to get the full picture of their careers. Counts below are broken out by 3×, 4×, and 5× AA. Hover to view wrestlers list for each row. Click a row to view wrestlers list for that row.

{% capture report_02_archetypes %}{% include report_02_archetypes_table.md %}{% endcapture %}
{{ report_02_archetypes }}

## Last Chance All-Americans

Wrestlers who All-Americaned exactly once, in their last year of eligibility. Hover to view wrestlers list for each row. Click a row to view wrestlers list for that row.

{% capture report_02_last_chance %}{% include report_02_last_chance_table.md %}{% endcapture %}
{{ report_02_last_chance }}

## Multi-weight All-Americans


Moving up or down a weight class is risky: new competition, different body composition, potential loss of competitive advantage. Yet some wrestlers navigate these transitions and still manage to reach the podium.

Wrestlers who have earned AA honors in more than one weight class are a distinct subset of the elite: they moved weights at some point and still placed at NCAAs.

Of **{{ site.data.report_02_stats.n_unique_wrestlers }}** unique wrestlers with complete careers who placed at the NCAA tournament (2000–2025), **{{ site.data.report_02_stats.n_multi_weight_aa }}** have earned AA in at least two different weight classes.

### Count of AAs at n unique weight classes

Most multi-weight All-Americans competed at exactly two weight classes. The rare feat of placing at four different weights was accomplished by only one wrestler in the dataset: **Kyle Dake, Mr. 444**, who famously won national titles at 141, 149, 157, and 165 (2009–2013).

| Unique weight classes | Wrestlers |
|:---------------------:|:---------:|
| 2 | {{ site.data.report_02_stats.multi_weight_by_n.2 }} |
| 3 | {{ site.data.report_02_stats.multi_weight_by_n.3 }} |
| 4 | {{ site.data.report_02_stats.multi_weight_by_n.4 }} |

### Weight-change direction and placement impact

For wrestlers who AAd at two or more weights, we examine each transition - a consecutive pair of AA finishes (ordered by ascending year and eligibility: Fr → So → Jr → Sr → SSr) where the wrestler changed weight. For example, Fr at 125 lbs → So at 133 lbs counts as one transition. There are **{{ site.data.report_02_stats.weight_move_stats.n_transitions }}** such transitions in the data.

{% include report_02_weight_flow.html %}

*Hover over any box to see wrestlers in that segment. Same layout as static diagram below.*

<details>
<summary>Static version (PNG)</summary>

![Weight-change flow: Multi-weight AA transitions → Moving up/down → Improved (green) / Worse (red) / Same (grey)]({{ site.baseurl }}/charts/weight_change_flow.png)

</details>

*Flow diagram: all weight-change transitions on the left; branches to moving up or down (with counts); then to improved (green), worse (red), or same placement (grey).*

**Findings:**

**The conventional wisdom is that moving up a weight class to bigger, stronger competition could lead to worse results. The data tells a different story:**

- **Weight changes are almost always upward.** {{ site.data.report_02_stats.weight_move_stats.moves_up }} of {{ site.data.report_02_stats.weight_move_stats.n_transitions }} transitions ({{ site.data.report_02_stats.weight_move_stats.moves_up | times: 100 | divided_by: site.data.report_02_stats.weight_move_stats.n_transitions }}%) involve moving to a higher weight class, showing natural growth over a college career.

- **Moving up correlates with improvement, not decline.** Among wrestlers who moved up, {{ site.data.report_02_stats.weight_move_stats.pct_up_improved }}% improved their placement, {{ site.data.report_02_stats.weight_move_stats.pct_up_worse }}% placed worse, and {{ site.data.report_02_stats.weight_move_stats.pct_up_same }}% stayed the same. For elite wrestlers, moving up in weight and facing bigger competition doesn't prevent success.

- **Moving down shows even higher improvement rates.** Only {{ site.data.report_02_stats.weight_move_stats.moves_down }} transitions involve cutting to a lower weight, but {{ site.data.report_02_stats.weight_move_stats.down_improved }} of those ({{ site.data.report_02_stats.weight_move_stats.pct_down_improved }}%) resulted in improved placement. Small sample, but the pattern suggests elite wrestlers who cut weight may be finding their optimal competitive class.

**Takeaway:** Weight changes don't derail elite careers, whether moving up with natural growth or cutting down to find an edge, multi-weight All-Americans show that adaptability is part of sustained excellence.

---

## Appendix: Methodology and Analysis Scope

### Complete Career Criteria

This analysis includes only wrestlers whose careers are **observably complete**—meaning they've exhausted their eligibility or enough time has passed that we can be confident they won't return to competition.

#### We include:

- All wrestlers who competed as Super Seniors (final year of eligibility)
- Wrestlers whose most recent appearance was Sr (any year); we do not exclude based on a possible SSr return
- Wrestlers whose most recent appearance was Jr in 2022 or earlier (had opportunity for Sr/SSr but didn't return)
- And so on for earlier eligibility years

#### We exclude:

- Wrestlers who last competed as Fr in 2024–2025 (could still AA as So/Jr/Sr/SSr)
- Wrestlers who last competed as So in 2023–2025 (could still AA as Jr/Sr/SSr)
- Wrestlers who last competed as Jr in 2023–2025 (could still AA as Sr/SSr)

We do not exclude wrestlers who last competed as Sr (e.g., in 2024–2025) based on a possible return as SSr, as many wrestlers are opting to not take their final year and move on to post-collegiate endeavors. We count their career as complete through their senior year. 

### Full Career in Dataset Window

We also require that a wrestler's entire career falls within the dataset window (2000–2025). For each AA finish (each row in our data), the year must be in the allowed range for that eligibility class:

- Fr AA year in 2000–2022
- So in 2001–2023
- Jr in 2002–2024
- Sr in 2003–2025
- SSr in 2004–2025

If any appearance falls outside these bounds, we exclude the wrestler. For example, a So in 2000 implies Fr was 1999, before the window, so that wrestler is excluded.

Wrestlers must have all AA appearances within these windows to be included in analysis.

### What This Approach Captures (and Doesn't)

This methodology ensures we're counting complete careers that are fully observable. Our tier counts (1×, 2×, 3×, 4×, 5× AA) represent wrestlers' final career totals.

**What we can see:** The progression patterns of wrestlers who reached the NCAA podium multiple times—how they improved, plateaued, or regressed across their All-American finishes.

**What we cannot see:** The journey to the first All-American finish. For most wrestlers, this is the hardest climb—the years spent as a non-starter, backup, national qualifier, or Round of 12 competitor before finally breaking through to the podium. These pre-AA years, while often the most dramatic part of a wrestler's development arc, are not captured in our dataset.

For example, Robbie Waller (Oklahoma, 2000-2003) came one win short of All-American honors as both a freshman and sophomore before finally placing 6th as a junior and winning the championship as a senior. Mike Macchiavello (NC State, 2014-2018) had a losing record as a freshman and sophomore, took a redshirt year, then came one win short as a junior before winning the title as a senior. These inspiring progressions are largely invisible in our data - we only see their AA finishes, not the years of grinding that preceded them.

This analysis therefore tells the story of the elite few who made it to the podium enough times to show a progression, not the full journey of every wrestler who eventually earned All-American honors.

[← Back to table of contents]({{ site.baseurl }}/)

</div>
