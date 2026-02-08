"""
NCAA Wrestling All-Americans Eligibility Analysis
==================================================
Analyzes eligibility year patterns among NCAA D1 Wrestling All-Americans (2000-2024)
"""

import html as html_module
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Paths
ROOT_DIR = Path(__file__).parent.parent
DATA_PATH = ROOT_DIR / "data" / "raw_data.csv"
CHARTS_DIR = ROOT_DIR / "charts"
TABLES_DIR = ROOT_DIR / "tables"
SITE_CHARTS_DIR = ROOT_DIR / "docs" / "charts"  # For GitHub Pages
REPORT_DATA_DIR = ROOT_DIR / "docs" / "_data"   # Jekyll data for report.md

# Ensure output directories exist
CHARTS_DIR.mkdir(exist_ok=True)
TABLES_DIR.mkdir(exist_ok=True)
SITE_CHARTS_DIR.mkdir(exist_ok=True)
REPORT_DATA_DIR.mkdir(exist_ok=True)

# Plot style configuration for reproducibility
plt.style.use("default")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Avenir", "Helvetica Neue", "Helvetica", "Arial"]
plt.rcParams["font.weight"] = "light"
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["axes.titleweight"] = "medium"

# Eligibility year order (for consistent plotting)
ELIGIBILITY_ORDER = ["Fr", "So", "Jr", "Sr", "SSr"]
ELIGIBILITY_COLORS = {
    "Fr": "#4CAF50",   # Green
    "So": "#2196F3",   # Blue  
    "Jr": "#FF9800",   # Orange
    "Sr": "#9C27B0",   # Purple
    "SSr": "#F44336",  # Red
}

# ==============================================================================
# LOAD DATA
# ==============================================================================

print("Loading data...")
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df):,} records")

# ==============================================================================
# CLEAN DATA
# ==============================================================================

print("\nCleaning data...")

# Standardize eligibility year (fix casing and whitespace issues)
df["Eligibility Year"] = df["Eligibility Year"].str.strip().str.title()
# Handle edge cases: "Ssr" -> "SSr" (super senior)
df["Eligibility Year"] = df["Eligibility Year"].replace({"Ssr": "SSr"})

# Type conversions
df["Year"] = df["Year"].astype(int)
df["Weight"] = df["Weight"].astype(int)
df["Place"] = df["Place"].astype(int)
df["Wrestler"] = df["Wrestler"].astype(str)
df["School"] = df["School"].astype(str)
df["Placement-Seed Delta"] = df["Placement-Seed Delta"].astype(int)
df["Eligibility Year"] = df["Eligibility Year"].astype(str)
df["Progression Eligible"] = df["Progression Eligible"].astype(bool)
df["AAs"] = df["AAs"].astype(int)

# ==============================================================================
# VALIDATION
# ==============================================================================

print("\nRunning validation checks...")

# Check year range
year_min, year_max = df["Year"].min(), df["Year"].max()
print(f"  Year range: {year_min}-{year_max}")
assert year_min >= 1999, f"Unexpected minimum year: {year_min}"
assert year_max <= 2025, f"Unexpected maximum year: {year_max}"

# Check place values (All-Americans are places 1-8)
valid_places = set(range(1, 9))
actual_places = set(df["Place"].unique())
assert actual_places.issubset(valid_places), f"Invalid places found: {actual_places - valid_places}"
print(f"  Places: {sorted(actual_places)}")

# Check eligibility years
valid_eligibility = set(ELIGIBILITY_ORDER)
actual_eligibility = set(df["Eligibility Year"].unique())
invalid_eligibility = actual_eligibility - valid_eligibility
if invalid_eligibility:
    print(f"  WARNING: Unknown eligibility values: {invalid_eligibility}")
    # Filter to known values for analysis
    df = df[df["Eligibility Year"].isin(valid_eligibility)]
    print(f"  Filtered to {len(df):,} records with valid eligibility")
else:
    print(f"  Eligibility years: {sorted(actual_eligibility)}")

# Check for null values
null_counts = df.isnull().sum()
if null_counts.any():
    print(f"  WARNING: Null values found:\n{null_counts[null_counts > 0]}")
else:
    print("  No null values")

# Summary statistics
print(f"\nData summary:")
print(f"  Total All-Americans: {len(df):,}")
print(f"  Unique wrestlers: {df['Wrestler'].nunique():,}")
print(f"  Year span: {year_max - year_min + 1} years ({year_min}-{year_max})")

# Eligibility breakdown
print(f"\nEligibility Year distribution:")
print(df["Eligibility Year"].value_counts().sort_index())

# ==============================================================================
# ANALYSIS: Eligibility Year Distribution
# ==============================================================================

print("\n" + "="*60)
print("ANALYSIS: Eligibility Year Distribution")
print("="*60)

# --- All-Americans by Eligibility Year ---
aa_by_eligibility = df["Eligibility Year"].value_counts()
aa_by_eligibility = aa_by_eligibility.reindex(ELIGIBILITY_ORDER).dropna()

print("\nAll-Americans by Eligibility Year:")
print(aa_by_eligibility)

# --- National Champions (Place == 1) by Eligibility Year ---
champions = df[df["Place"] == 1]
champs_by_eligibility = champions["Eligibility Year"].value_counts()
champs_by_eligibility = champs_by_eligibility.reindex(ELIGIBILITY_ORDER).dropna()

print("\nNational Champions by Eligibility Year:")
print(champs_by_eligibility)

# ==============================================================================
# CHART 1: National Champions by Eligibility Year
# ==============================================================================

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    champs_by_eligibility.index,
    champs_by_eligibility.values,
    color=[ELIGIBILITY_COLORS.get(e, "#888888") for e in champs_by_eligibility.index],
    edgecolor="white",
    linewidth=1.5
)

# Add value labels on bars
for bar, val in zip(bars, champs_by_eligibility.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 2,
        str(int(val)),
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

ax.set_xlabel("Eligibility Year", fontsize=12)
ax.set_ylabel("Number of National Champions", fontsize=12)
ax.set_title(f"NCAA Wrestling National Champions by Eligibility Year\n({year_min}-{year_max})", 
             fontsize=14, fontweight="bold")
ax.set_ylim(0, champs_by_eligibility.max() * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
chart_path = CHARTS_DIR / "champions_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "champions_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"\nSaved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# CHART 2: All All-Americans by Eligibility Year
# ==============================================================================

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    aa_by_eligibility.index,
    aa_by_eligibility.values,
    color=[ELIGIBILITY_COLORS.get(e, "#888888") for e in aa_by_eligibility.index],
    edgecolor="white",
    linewidth=1.5
)

# Add value labels on bars
for bar, val in zip(bars, aa_by_eligibility.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 5,
        str(int(val)),
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold"
    )

ax.set_xlabel("Eligibility Year", fontsize=12)
ax.set_ylabel("Number of All-Americans", fontsize=12)
ax.set_title(f"NCAA Wrestling All-Americans by Eligibility Year\n({year_min}-{year_max})", 
             fontsize=14, fontweight="bold")
ax.set_ylim(0, aa_by_eligibility.max() * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
chart_path = CHARTS_DIR / "all_americans_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "all_americans_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"Saved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# CHART 3: All-Americans Trend (Primary) - Smoothed Lines with Direct Labels
# ==============================================================================

# Pivot: count of AAs by year and eligibility
aa_by_year_elig = df.pivot_table(
    index="Year", 
    columns="Eligibility Year", 
    aggfunc="size", 
    fill_value=0
)

# Reorder columns (exclude SSr - too few data points)
plot_order = [e for e in ["Fr", "So", "Jr", "Sr"] if e in aa_by_year_elig.columns]
aa_counts = aa_by_year_elig[plot_order]

# 3-year rolling mean + light Gaussian smoothing for extra smoothness
from scipy.ndimage import gaussian_filter1d
aa_rolled = aa_counts.rolling(window=3, center=True, min_periods=1).mean()

# Eligibility labels for direct annotation
ELIG_LABELS = {"Fr": "Freshman", "So": "Sophomore", "Jr": "Junior", "Sr": "Senior"}

fig, ax = plt.subplots(figsize=(10, 6))

for elig in plot_order:
    years = aa_rolled.index.values
    rolled = aa_rolled[elig].values
    # Apply light Gaussian smoothing on top
    smoothed = gaussian_filter1d(rolled, sigma=1.2)
    
    # Plot smoothed trend line only
    ax.plot(
        years, 
        smoothed,
        color=ELIGIBILITY_COLORS.get(elig, "#888888"),
        linewidth=3,
    )
    
    # Direct label at end of line
    ax.annotate(
        ELIG_LABELS[elig],
        xy=(years[-1], smoothed[-1]),
        xytext=(8, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=11,
        fontweight="medium",
        color=ELIGIBILITY_COLORS.get(elig, "#888888")
    )

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of All-Americans", fontsize=12)
ax.set_title("All-Americans by Eligibility Class Over Time\n(3-year smoothed trend)", 
             fontsize=14, fontweight="bold")
ax.set_ylim(0, 45)
ax.set_xlim(aa_rolled.index.min(), aa_rolled.index.max() + 3)  # Extra space for labels
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
chart_path = CHARTS_DIR / "aa_trend_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "aa_trend_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"Saved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# CHART 4: All-Americans Variability (Secondary) - Small Multiples Bar Charts
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
axes = axes.flatten()

for idx, elig in enumerate(plot_order):
    ax = axes[idx]
    years = aa_counts.index.values
    counts = aa_counts[elig].values
    
    # Bar chart for raw yearly data
    ax.bar(
        years, 
        counts,
        color=ELIGIBILITY_COLORS.get(elig, "#888888"),
        alpha=0.6,
        width=0.8
    )
    
    ax.set_title(ELIG_LABELS[elig], fontsize=12, fontweight="medium",
                 color=ELIGIBILITY_COLORS.get(elig, "#888888"))
    ax.set_ylim(0, 45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

# Common labels
fig.supxlabel("Year", fontsize=12)
fig.supylabel("Number of All-Americans", fontsize=12)
fig.suptitle("All-Americans by Year: Yearly Counts by Class", fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
chart_path = CHARTS_DIR / "aa_variability_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "aa_variability_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"Saved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# CHART 5: National Champions Trend (Primary) - Smoothed Lines with Direct Labels
# ==============================================================================

# Pivot: count of NCs by year and eligibility
nc_by_year_elig = champions.pivot_table(
    index="Year", 
    columns="Eligibility Year", 
    aggfunc="size", 
    fill_value=0
)

# Reorder columns (exclude SSr)
plot_order_nc = [e for e in ["Fr", "So", "Jr", "Sr"] if e in nc_by_year_elig.columns]
nc_counts = nc_by_year_elig[plot_order_nc]

# 3-year rolling mean + light Gaussian smoothing
nc_rolled = nc_counts.rolling(window=3, center=True, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(10, 6))

for elig in plot_order_nc:
    years = nc_rolled.index.values
    rolled = nc_rolled[elig].values
    # Apply light Gaussian smoothing on top
    smoothed = gaussian_filter1d(rolled, sigma=1.2)
    
    # Plot smoothed trend line only
    ax.plot(
        years, 
        smoothed,
        color=ELIGIBILITY_COLORS.get(elig, "#888888"),
        linewidth=3,
    )
    
    # Direct label at end of line
    ax.annotate(
        ELIG_LABELS[elig],
        xy=(years[-1], smoothed[-1]),
        xytext=(8, 0),
        textcoords="offset points",
        va="center",
        ha="left",
        fontsize=11,
        fontweight="medium",
        color=ELIGIBILITY_COLORS.get(elig, "#888888")
    )

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Number of National Champions", fontsize=12)
ax.set_title("National Champions by Eligibility Class Over Time\n(3-year smoothed trend)", 
             fontsize=14, fontweight="bold")
ax.set_ylim(0, 8)
ax.set_xlim(nc_rolled.index.min(), nc_rolled.index.max() + 3)  # Extra space for labels
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
chart_path = CHARTS_DIR / "nc_trend_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "nc_trend_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"Saved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# CHART 6: National Champions Variability (Secondary) - Small Multiples Bar Charts
# ==============================================================================

fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
axes = axes.flatten()

for idx, elig in enumerate(plot_order_nc):
    ax = axes[idx]
    years = nc_counts.index.values
    counts = nc_counts[elig].values
    
    # Bar chart for raw yearly data
    ax.bar(
        years, 
        counts,
        color=ELIGIBILITY_COLORS.get(elig, "#888888"),
        alpha=0.6,
        width=0.8
    )
    
    ax.set_title(ELIG_LABELS[elig], fontsize=12, fontweight="medium",
                 color=ELIGIBILITY_COLORS.get(elig, "#888888"))
    ax.set_ylim(0, 10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

# Common labels
fig.supxlabel("Year", fontsize=12)
fig.supylabel("Number of National Champions", fontsize=12)
fig.suptitle("National Champions by Year: Yearly Counts by Class", fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
chart_path = CHARTS_DIR / "nc_variability_by_eligibility.png"
site_chart_path = SITE_CHARTS_DIR / "nc_variability_by_eligibility.png"
plt.savefig(chart_path, dpi=150)
plt.savefig(site_chart_path, dpi=150)
plt.close()
print(f"Saved: {chart_path}")
print(f"Saved: {site_chart_path}")

# ==============================================================================
# REPORT 2: Aesthetic progressions (multi-AA and improvement every year)
# ==============================================================================

print("\n" + "="*60)
print("REPORT 2: Multi-AA and aesthetic progressions")
print("="*60)

# Filter: Include only wrestlers whose full career falls in the dataset window (2000-2025).
# (1) Career complete: exclude those who could still AA in a non-SSr year; include SSr, Sr (any), Jr ≤2022, So ≤2021, Fr ≤2020.
# (2) Career in window: each AA (Eligibility Year, Year) must satisfy year bounds so the whole career is observable:
#     Fr:  year-1>=1999 and year+3<=2025  -> 2000<=year<=2022
#     So:  year-2>=1999 and year+2<=2025  -> 2001<=year<=2023
#     Jr:  year-3>=1999 and year+1<=2025  -> 2002<=year<=2024
#     Sr:  year-4>=1999 and year+0<=2025  -> 2003<=year<=2025
#     SSr: year-5>=1999 and year+0<=2025  -> 2004<=year<=2025 (not used in timeline viz)
CAREER_WINDOW = (1999, 2025)
ELIG_YEAR_BOUNDS = {
    "Fr":  (CAREER_WINDOW[0] + 1, CAREER_WINDOW[1] - 3),   # 2000..2022
    "So":  (CAREER_WINDOW[0] + 2, CAREER_WINDOW[1] - 2),   # 2001..2023
    "Jr":  (CAREER_WINDOW[0] + 3, CAREER_WINDOW[1] - 1),   # 2002..2024
    "Sr":  (CAREER_WINDOW[0] + 4, CAREER_WINDOW[1]),       # 2003..2025
    "SSr": (CAREER_WINDOW[0] + 5, CAREER_WINDOW[1]),       # 2004..2025
}


def career_fully_in_window(wrestler_df):
    """True if every AA (Eligibility Year, Year) for this wrestler is within the allowed year bounds."""
    for _, row in wrestler_df.iterrows():
        elig = row["Eligibility Year"]
        year = row["Year"]
        lo, hi = ELIG_YEAR_BOUNDS.get(elig, (0, 0))
        if not (lo <= year <= hi):
            return False
    return True


wrestler_latest = (
    df.loc[df.groupby("Wrestler")["Year"].idxmax()][["Wrestler", "Eligibility Year", "Year"]]
    .rename(columns={"Eligibility Year": "Latest_Eligibility", "Year": "Latest_Year"})
)


def career_is_complete(row):
    """True if wrestler's career is observably complete. We do not exclude based on possible SSr return."""
    elig = row["Latest_Eligibility"]
    year = row["Latest_Year"]
    if elig == "SSr":
        return True
    if elig == "Sr":
        return True  # Include all Sr; do not exclude for possible SSr return
    if elig == "Jr" and year <= 2022:
        return True
    if elig == "So" and year <= 2021:
        return True
    if elig == "Fr" and year <= 2020:
        return True
    return False


wrestler_latest["Career_Complete"] = wrestler_latest.apply(career_is_complete, axis=1)
valid_wrestlers = wrestler_latest[wrestler_latest["Career_Complete"]]["Wrestler"].tolist()
# Require full career in window: every (Eligibility Year, Year) must be in bounds (excludes e.g. Cael Sanderson: So 2000 < 2001)
valid_wrestlers = [w for w in valid_wrestlers if career_fully_in_window(df[df["Wrestler"] == w])]
df_filtered = df[df["Wrestler"].isin(valid_wrestlers)].copy()
n_complete_careers = len(valid_wrestlers)
print(f"\nWrestlers with complete observable careers (full career in window): {n_complete_careers:,}")

# Career window timeline: allowed AA year ranges by eligibility class (for report); SSr excluded
timeline_elig = [e for e in ELIGIBILITY_ORDER if e != "SSr"]
n_timeline_rows = len(timeline_elig)
row_spacing = 0.4  # tighter vertical spacing between bars
y_positions = np.arange(n_timeline_rows) * row_spacing
row_height = 0.72 * row_spacing
fig, ax = plt.subplots(figsize=(12, 5))
x_min, x_max = 1998, 2027
ax.set_xlim(x_min, x_max)
ax.set_ylim(-0.35, (n_timeline_rows - 1) * row_spacing + 0.35)
bar_color = "#475569"
bar_text_color = "#f8fafc"
for i, elig in enumerate(timeline_elig):
    y = y_positions[i]
    lo, hi = ELIG_YEAR_BOUNDS[elig]
    rect = mpatches.Rectangle(
        (lo, y - row_height / 2), hi - lo, row_height,
        facecolor=bar_color, edgecolor=bar_color, linewidth=1.2, alpha=0.85
    )
    ax.add_patch(rect)
    ax.text(lo, y, f"  {lo}", ha="left", va="center", fontsize=16, fontweight="bold", color=bar_text_color)
    ax.text(hi, y, f"{hi}  ", ha="right", va="center", fontsize=16, fontweight="bold", color=bar_text_color)
ax.set_yticks(y_positions)
ax.set_yticklabels(timeline_elig, fontsize=16)
ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
ax.set_xticklabels(["2000", "2005", "2010", "2015", "2020", "2025"], fontsize=15)
ax.axvspan(1998, 2000, alpha=0.12, color="gray", zorder=0)
ax.axvspan(2025, 2027, alpha=0.12, color="gray", zorder=0)
mid_y = (n_timeline_rows - 1) * row_spacing / 2
ax.text(1999, mid_y, "before dataset", fontsize=18, fontweight="bold", color="#475569", ha="center", va="center", rotation=90)
ax.text(2026, mid_y, "future data", fontsize=18, fontweight="bold", color="#475569", ha="center", va="center", rotation=90)
ax.set_xlabel("Year", fontsize=15)
ax.grid(True, axis="y", color="#f1f5f9", linewidth=0.5)
ax.set_axisbelow(True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Eligible AA year ranges by class (complete career window)", fontsize=19, fontweight="bold")
fig.text(0.5, -0.02, "Wrestlers must have all AA appearances within these windows to be included in analysis.", ha="center", fontsize=14, color="#64748b", style="italic")
plt.tight_layout(rect=[0, 0.04, 1, 1])
career_timeline_path = CHARTS_DIR / "career_window_timeline.png"
career_timeline_site_path = SITE_CHARTS_DIR / "career_window_timeline.png"
plt.savefig(career_timeline_path, dpi=150)
plt.savefig(career_timeline_site_path, dpi=150)
plt.close()
print(f"Saved: {career_timeline_path}")
print(f"Saved: {career_timeline_site_path}")

# Use df_filtered for all multi-AA analysis (funnel, tiers, multi-weight, progression).
# Unique wrestlers (each row = one AA finish; Wrestler may appear multiple times)
n_unique_wrestlers = df_filtered["Wrestler"].nunique()
print(f"Unique wrestlers (complete careers only): {n_unique_wrestlers:,}")

# Multi-AA: wrestlers who appear more than once (AAd more than once)
aa_counts_per_wrestler = df_filtered.groupby("Wrestler").size()
multi_aa_mask = aa_counts_per_wrestler > 1
multi_aa_wrestlers = aa_counts_per_wrestler[multi_aa_mask]
n_multi_aa = len(multi_aa_wrestlers)
print(f"Multi-AA wrestlers (AAd more than once): {n_multi_aa:,} out of {n_unique_wrestlers:,}")

# Funnel: wrestlers with exactly 1×, 2×, 3×, 4×, 5× AAs (matches table counts)
n_1x = (aa_counts_per_wrestler == 1).sum()
n_2x = (aa_counts_per_wrestler == 2).sum()
n_3x = (aa_counts_per_wrestler == 3).sum()
n_4x = (aa_counts_per_wrestler == 4).sum()
n_5x = (aa_counts_per_wrestler >= 5).sum()
funnel_counts = [n_1x, n_2x, n_3x, n_4x, n_5x]

# Funnel diagram: horizontal bars (width ∝ count), stacked top to bottom
fig, ax = plt.subplots(figsize=(9, 6))
y_pos = np.arange(len(funnel_counts))[::-1]  # 4, 3, 2, 1, 0 so "All" at top
max_w = max(funnel_counts)
x_center = 0.5
bar_half_scale = 0.42
lefts = [x_center - (w / max_w) * bar_half_scale for w in funnel_counts]
bar_widths = [(w / max_w) * 2 * bar_half_scale for w in funnel_counts]
colors = ["#1a365d", "#2c5282", "#3182ce", "#4299e1", "#63b3ed"]  # dark to light blue
bars = ax.barh(y_pos, bar_widths, left=lefts, height=0.72, color=colors, edgecolor="white", linewidth=2)
ax.set_yticks(y_pos)
ax.set_yticklabels(["1× AA", "2× AA", "3× AA", "4× AA", "5× AA"], fontsize=16)
ax.set_xlim(0, 1)
ax.set_xticks([])
for spine in ["top", "right", "bottom", "left"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Unique wrestlers by AA honor counts (2000–2025)", fontsize=18, fontweight="bold")
for i, yi in enumerate(y_pos):
    # 5× AA bar is tiny; use black text so the count is readable
    text_color = "black" if i == len(y_pos) - 1 else "white"
    ax.text(x_center, yi, f"  {funnel_counts[i]:,}  ", ha="center", va="center", fontsize=15, fontweight="bold", color=text_color)
plt.tight_layout()
funnel_path = CHARTS_DIR / "multi_aa_funnel.png"
funnel_site_path = SITE_CHARTS_DIR / "multi_aa_funnel.png"
plt.savefig(funnel_path, dpi=150)
plt.savefig(funnel_site_path, dpi=150)
plt.close()
print(f"Saved: {funnel_path}")
print(f"Saved: {funnel_site_path}")

# Multi-weight AAs: wrestlers who placed (AA) in more than one weight class
weights_per_wrestler = df_filtered.groupby("Wrestler")["Weight"].nunique()
multi_weight_mask = weights_per_wrestler >= 2
n_multi_weight_aa = multi_weight_mask.sum()
print(f"\nMulti-weight AAs (placed 1–8 in more than one weight class): {n_multi_weight_aa:,} wrestlers out of {n_unique_wrestlers:,}")

# Count of AAs at exactly 2, 3, 4 unique weight classes (e.g. Kyle Dake = 4 weight classes)
n_weight_2 = (weights_per_wrestler == 2).sum()
n_weight_3 = (weights_per_wrestler == 3).sum()
n_weight_4 = (weights_per_wrestler == 4).sum()
multi_weight_by_n = {"2": int(n_weight_2), "3": int(n_weight_3), "4": int(n_weight_4)}
wrestlers_4_weights = weights_per_wrestler[weights_per_wrestler == 4].index.tolist()
print(f"  Exactly 2 weight classes: {n_weight_2:,}")
print(f"  Exactly 3 weight classes: {n_weight_3:,}")
print(f"  Exactly 4 weight classes: {n_weight_4:,} (e.g. Kyle Dake)")

# For wrestlers who AAd at 2+ weights: did they move up or down? Did place improve?
# Build transitions: each consecutive AA pair when weight changed.
# Order by ascending Year and ascending eligibility (Fr -> So -> Jr -> Sr -> SSr) so we follow career progression.
elig_sort_key = {e: i for i, e in enumerate(ELIGIBILITY_ORDER)}
multi_weight_wrestlers = weights_per_wrestler[multi_weight_mask].index.tolist()
transitions = []
for wrestler in multi_weight_wrestlers:
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler].copy()
    w_df["_order"] = w_df["Year"] * 10 + w_df["Eligibility Year"].map(elig_sort_key)
    w_df = w_df.sort_values(["_order", "Year", "Eligibility Year"])
    rows = w_df[["Year", "Weight", "Place", "Eligibility Year"]].values.tolist()
    for i in range(len(rows) - 1):
        year1, w1, place1, elig1 = rows[i]
        year2, w2, place2, elig2 = rows[i + 1]
        if w1 != w2:  # weight changed
            direction = "up" if w2 > w1 else "down"
            place_change = "improved" if place2 < place1 else ("worse" if place2 > place1 else "same")
            transitions.append({
                "wrestler": wrestler,
                "from_weight": int(w1),
                "to_weight": int(w2),
                "from_place": int(place1),
                "to_place": int(place2),
                "direction": direction,
                "place_change": place_change,
            })
transitions_df = pd.DataFrame(transitions)

# Aggregate: move up vs down, and place improvement by direction
if len(transitions_df) > 0:
    up_df = transitions_df[transitions_df["direction"] == "up"]
    down_df = transitions_df[transitions_df["direction"] == "down"]
    weight_move_stats = {
        "n_transitions": len(transitions_df),
        "moves_up": int(len(up_df)),
        "moves_down": int(len(down_df)),
        "up_improved": int((up_df["place_change"] == "improved").sum()),
        "up_worse": int((up_df["place_change"] == "worse").sum()),
        "up_same": int((up_df["place_change"] == "same").sum()),
        "down_improved": int((down_df["place_change"] == "improved").sum()),
        "down_worse": int((down_df["place_change"] == "worse").sum()),
        "down_same": int((down_df["place_change"] == "same").sum()),
    }
    pct_up_improved = 100 * weight_move_stats["up_improved"] / len(up_df) if len(up_df) > 0 else 0
    pct_up_worse = 100 * weight_move_stats["up_worse"] / len(up_df) if len(up_df) > 0 else 0
    pct_down_improved = 100 * weight_move_stats["down_improved"] / len(down_df) if len(down_df) > 0 else 0
    pct_down_worse = 100 * weight_move_stats["down_worse"] / len(down_df) if len(down_df) > 0 else 0
    print(f"\nWeight-change transitions: {len(transitions_df)} transitions (when wrestler changed weight)")
    print(f"  Moving UP: {len(up_df)} — improved: {weight_move_stats['up_improved']} ({pct_up_improved:.1f}%), worse: {weight_move_stats['up_worse']} ({pct_up_worse:.1f}%), same: {weight_move_stats['up_same']}")
    print(f"  Moving DOWN: {len(down_df)} — improved: {weight_move_stats['down_improved']} ({pct_down_improved:.1f}%), worse: {weight_move_stats['down_worse']} ({pct_down_worse:.1f}%), same: {weight_move_stats['down_same']}")
    weight_move_stats["pct_up_improved"] = round(pct_up_improved, 1)
    weight_move_stats["pct_up_worse"] = round(pct_up_worse, 1)
    weight_move_stats["pct_up_same"] = round(100 * weight_move_stats["up_same"] / len(up_df), 1) if len(up_df) > 0 else 0
    weight_move_stats["pct_down_improved"] = round(pct_down_improved, 1)
    weight_move_stats["pct_down_worse"] = round(pct_down_worse, 1)
    weight_move_stats["pct_down_same"] = round(100 * weight_move_stats["down_same"] / len(down_df), 1) if len(down_df) > 0 else 0
else:
    weight_move_stats = {}

# Flow diagram: Multi-weight AAs -> Moving up/down -> Improved/Worse/Same
# Colors: green (improved), grey (same), red (worse)
FLOW_GREEN = "#22c55e"
FLOW_RED = "#ef4444"
FLOW_GREY = "#94a3b8"
FLOW_UP = "#3b82f6"
FLOW_DOWN = "#8b5cf6"
FLOW_LEFT = "#64748b"

if len(transitions_df) > 0:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title and subtitle (outside chart)
    fig.suptitle("Weight-change transitions and placement outcomes", fontsize=14, fontweight="bold", y=0.98)
    fig.text(0.5, 0.93, "152 transitions from 137 multi-weight All-Americans", ha="center", fontsize=10, color="#64748b")

    # Column 1 (left): Multi-weight AA transitions
    left_w, left_h = 1.8, 1.2
    rect = mpatches.FancyBboxPatch((1.5 - left_w/2, 5 - left_h/2), left_w, left_h, boxstyle="round,pad=0.02",
                                    facecolor=FLOW_LEFT, edgecolor="#64748b", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(1.5, 5, f"Multi-weight AA\ntransitions\n{weight_move_stats['n_transitions']}", ha="center", va="center", fontsize=11, color="white")

    # Column 2: Moving up / Moving down (with % like outcome boxes)
    n_trans = weight_move_stats["n_transitions"]
    mid_w, mid_h = 2, 1
    for cx, cy, label, count, color in [
        (4.5, 6.5, "Moving up", weight_move_stats["moves_up"], FLOW_UP),
        (4.5, 3.5, "Moving down", weight_move_stats["moves_down"], FLOW_DOWN),
    ]:
        pct = round(100 * count / n_trans, 1) if n_trans else 0
        rect = mpatches.FancyBboxPatch((cx - mid_w/2, cy - mid_h/2), mid_w, mid_h, boxstyle="round,pad=0.02",
                                        facecolor=color, edgecolor="#64748b", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cx, cy, f"{label}\n{count} ({pct}%)", ha="center", va="center", fontsize=11, color="white")

    # Column 3: Outcome boxes — Worse centered on source; Improved/Same with spacing (reduced so up/down sets don't touch)
    out_w, out_h = 1.8, 0.75
    spacing = 0.9  # vertical gap between outcome boxes (middle stays centered on source)
    up_center, down_center = 6.5, 3.5  # match middle column box centers
    outcome_specs = [
        (7.5, up_center + spacing, f"Improved\n{weight_move_stats['up_improved']} ({weight_move_stats['pct_up_improved']}%)", FLOW_GREEN),
        (7.5, up_center, f"Worse\n{weight_move_stats['up_worse']} ({weight_move_stats['pct_up_worse']}%)", FLOW_RED),
        (7.5, up_center - spacing, f"Same\n{weight_move_stats['up_same']} ({weight_move_stats['pct_up_same']}%)", FLOW_GREY),
        (7.5, down_center + spacing, f"Improved\n{weight_move_stats['down_improved']} ({weight_move_stats['pct_down_improved']}%)", FLOW_GREEN),
        (7.5, down_center, f"Worse\n{weight_move_stats['down_worse']} ({weight_move_stats['pct_down_worse']}%)", FLOW_RED),
        (7.5, down_center - spacing, f"Same\n{weight_move_stats['down_same']} ({weight_move_stats['pct_down_same']}%)", FLOW_GREY),
    ]
    for x, y, label, color in outcome_specs:
        rect = mpatches.FancyBboxPatch((x - out_w/2, y - out_h/2), out_w, out_h, boxstyle="round,pad=0.02",
                                        facecolor=color, edgecolor="none", linewidth=0)
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=11, color="white")

    # Uniform thin connectors (single color)
    left_right = 1.5 + left_w / 2  # left box right edge
    mid_left = 4.5 - mid_w / 2
    mid_right = 4.5 + mid_w / 2
    right_left = 7.5 - out_w / 2
    connector_color = FLOW_LEFT
    connector_lw = 1.2

    # Connectors: left -> middle
    ax.plot([left_right, mid_left], [5, 6.5], color=connector_color, lw=connector_lw)
    ax.plot([left_right, mid_left], [5, 3.5], color=connector_color, lw=connector_lw)

    # Connectors: middle -> right (Worse at center; Improved above, Same below)
    up_outcomes = [(up_center + spacing, weight_move_stats["up_improved"]), (up_center, weight_move_stats["up_worse"]), (up_center - spacing, weight_move_stats["up_same"])]
    down_outcomes = [(down_center + spacing, weight_move_stats["down_improved"]), (down_center, weight_move_stats["down_worse"]), (down_center - spacing, weight_move_stats["down_same"])]
    for mid_y, outcomes in [(6.5, up_outcomes), (3.5, down_outcomes)]:
        for oy, count in outcomes:
            ax.plot([mid_right, right_left], [mid_y, oy], color=connector_color, lw=connector_lw)
    plt.tight_layout()
    flow_path = CHARTS_DIR / "weight_change_flow.png"
    flow_site_path = SITE_CHARTS_DIR / "weight_change_flow.png"
    plt.savefig(flow_path, dpi=150)
    plt.savefig(flow_site_path, dpi=150)
    plt.close()
    print(f"Saved: {flow_path}")
    print(f"Saved: {flow_site_path}")

# Eligibility-year combinations by N×AA tier (when AA was earned, by eligibility)
# For each wrestler: (n_aa, sorted tuple of eligibility years in which they AA'd)
elig_order = ELIGIBILITY_ORDER  # ["Fr", "So", "Jr", "Sr", "SSr"]
wrestler_tiers = []
for wrestler in df_filtered["Wrestler"].unique():
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler]
    n_aa = len(w_df)
    eligs = w_df["Eligibility Year"].unique().tolist()
    elig_combo = tuple(sorted(eligs, key=lambda e: elig_order.index(e)))
    wrestler_tiers.append({"wrestler": wrestler, "n_aa": n_aa, "elig_combo": elig_combo})

tiers_df = pd.DataFrame(wrestler_tiers)

# Placement-by-eligibility strings for combo table tooltips/expand: "Name (Fr-So-Jr-Sr)" with place or DNP
def wrestler_placement_string_combo(wrestler, w_df):
    w_df = w_df.sort_values(["_order", "Year", "Eligibility Year"])
    elig_to_place = {}
    for _, row in w_df.iterrows():
        elig_to_place[row["Eligibility Year"]] = int(row["Place"])
    order = ["Fr", "So", "Jr", "Sr"]
    if "SSr" in elig_to_place:
        order.append("SSr")
    parts = [str(elig_to_place.get(e, "DNP")) for e in order]
    return f"{wrestler} ({'-'.join(parts)})"

wrestler_placement_str_combo = {}
for wrestler in df_filtered["Wrestler"].unique():
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler].copy()
    w_df["_order"] = w_df["Year"] * 10 + w_df["Eligibility Year"].map(elig_sort_key)
    wrestler_placement_str_combo[wrestler] = wrestler_placement_string_combo(wrestler, w_df)

COMBO_LIST_DELIM = " | "

# Marker for "AA earned in this eligibility year"
MARKER = "●"
ELIG_COLS = ["Fr", "So", "Jr", "Sr", "SSr"]

def build_combo_table(n_aa_val):
    """Build table rows for one N×AA tier: combinations that exist, sorted by count descending.
    Only include wrestlers whose number of distinct eligibility years equals n_aa (excludes data quirks).
    Each row includes a 'Wrestlers' column (comma-separated names, HTML-escaped) for tooltips/expand."""
    sub = tiers_df[(tiers_df["n_aa"] == n_aa_val) & (tiers_df["elig_combo"].apply(len) == n_aa_val)]
    if len(sub) == 0:
        return None, 0
    total = len(sub)
    combo_counts = sub.groupby("elig_combo").size().sort_values(ascending=False)
    rows = []
    for elig_combo, count in combo_counts.items():
        pct = count / total * 100
        names = sub[sub["elig_combo"] == elig_combo]["wrestler"].tolist()
        wrestlers_attr = html_module.escape(", ".join(sorted(names)))
        row = {e: MARKER if e in elig_combo else "" for e in ELIG_COLS}
        row["Count"] = count
        row["%"] = f"{pct:.1f}%"
        row["Wrestlers"] = wrestlers_attr
        rows.append(row)
    return pd.DataFrame(rows), total


def combo_df_to_html(combo_table, cols, table_class_extra="", wrestlers_col=None, placement_lookup=None):
    """Render combo DataFrame as HTML table with classed cells for styling (vertical borders, shaded cells).
    If wrestlers_col is set and combo_table has that column, each <tr> gets data-wrestlers and data-count.
    If placement_lookup is provided, each <tr> also gets data-wrestlers-places (Name (Fr-So-Jr-Sr))."""
    lines = [f'<table class="eligibility-combo-table {table_class_extra}">', "<thead><tr>"]
    for c in cols:
        lines.append(f"<th>{c}</th>")
    lines.append("</tr></thead><tbody>")
    has_wrestlers = wrestlers_col and wrestlers_col in combo_table.columns
    for idx, row in combo_table.iterrows():
        tr_attrs = ""
        if has_wrestlers and row.get(wrestlers_col):
            tr_attrs = f' data-wrestlers="{row[wrestlers_col]}" data-count="{row["Count"]}"'
            if placement_lookup:
                names = [s.strip() for s in html_module.unescape(row[wrestlers_col]).split(",")]
                places_str = COMBO_LIST_DELIM.join(placement_lookup.get(n, n) for n in names)
                tr_attrs += f' data-wrestlers-places="{html_module.escape(places_str)}"'
        lines.append(f"<tr{tr_attrs}>")
        for c in cols:
            val = row[c]
            if c in ELIG_COLS:
                cell_class = "combo-yes" if val == MARKER else "combo-no"
                lines.append(f'<td class="{cell_class}">{val}</td>')
            else:
                lines.append(f"<td>{val}</td>")
        lines.append("</tr>")
    lines.append("</tbody></table>")
    return "\n".join(lines)


def combo_df_to_html_nc(combo_table, cols, table_class_extra="", wrestlers_col="Wrestlers", placement_lookup=None):
    """Same as combo_df_to_html but NC tables use combo-yes-nc for gold shaded cells.
    If combo_table has a wrestlers_col, each <tr> gets data-wrestlers and data-count for tooltips.
    If placement_lookup is provided, each <tr> also gets data-wrestlers-places (Name (Fr-So-Jr-Sr))."""
    lines = [f'<table class="eligibility-combo-table eligibility-combo-nc {table_class_extra}">', "<thead><tr>"]
    for c in cols:
        lines.append(f"<th>{c}</th>")
    lines.append("</tr></thead><tbody>")
    has_wrestlers = wrestlers_col in combo_table.columns
    for idx, row in combo_table.iterrows():
        tr_attrs = ""
        if has_wrestlers and row[wrestlers_col]:
            tr_attrs = f' data-wrestlers="{row[wrestlers_col]}" data-count="{row["Count"]}"'
            if placement_lookup:
                names = [s.strip() for s in html_module.unescape(row[wrestlers_col]).split(",")]
                places_str = COMBO_LIST_DELIM.join(placement_lookup.get(n, n) for n in names)
                tr_attrs += f' data-wrestlers-places="{html_module.escape(places_str)}"'
        lines.append(f"<tr{tr_attrs}>")
        for c in cols:
            val = row[c]
            if c in ELIG_COLS:
                cell_class = "combo-yes-nc" if val == MARKER else "combo-no"
                lines.append(f'<td class="{cell_class}">{val}</td>')
            else:
                lines.append(f"<td>{val}</td>")
        lines.append("</tr>")
    lines.append("</tbody></table>")
    return "\n".join(lines)


cols = ELIG_COLS + ["Count", "%"]

# Write combined markdown (for tables/ repo reference) and HTML (for docs/_includes)
combo_md_lines = ["# When AA was earned: combinations by eligibility year\n", "*Sorted by most common to least. ● = AA in that eligibility year.*\n"]
combo_html_lines = [
    "<h1>When All-American was earned:</h1>",
    "<p>When do wrestlers actually earn their All-American finishes? The tables below show the combinations of eligibility years for each tier (1×, 2×, 3×, 4×, 5× AA). Each table is sorted from most common to least common pattern. ● = AA in that eligibility year. Hover to view wrestlers list for each row. Click a row to view wrestlers list for that row.</p>",
]
for n in [1, 2, 3, 4, 5]:
    combo_table, total_n = build_combo_table(n)
    if combo_table is None or len(combo_table) == 0:
        continue
    combo_md_lines.append(f"\n## {n}× AA (n = {total_n:,})\n\n")
    combo_md_lines.append(combo_table[cols].to_markdown(index=False) + "\n")
    combo_html_lines.append(f"\n<h2 class=\"combo-tier-header\">{n}× AAs ({total_n:,})</h2>\n")
    combo_html_lines.append(combo_df_to_html(combo_table, cols, "eligibility-combo-aa", wrestlers_col="Wrestlers", placement_lookup=wrestler_placement_str_combo) + "\n")
    if n == 5:
        five_x_sub = tiers_df[(tiers_df["n_aa"] == 5) & (tiers_df["elig_combo"].apply(len) == 5)]
        five_x_names = sorted(five_x_sub["wrestler"].tolist())
        five_x_list_text = ", ".join(five_x_names)
        combo_html_lines.append(f'<p class="five-x-aa-list"><strong>Likely to never be repeated 5xAAs:</strong> {five_x_list_text}</p>\n')
    print(f"  {n}× AA: {len(combo_table)} combinations (total wrestlers {total_n:,})")
# Funnel and tables both use exact counts (1×, 2×, 3×, 4×, 5×)
n_exactly_4 = (aa_counts_per_wrestler == 4).sum()
print(f"  (4× AA = {n_exactly_4:,}; funnel matches table)")

combo_table_path = TABLES_DIR / "eligibility_combos_by_tier.md"
with open(combo_table_path, "w") as f:
    f.write("".join(combo_md_lines))
print(f"Saved: {combo_table_path}")

# Also write to docs/_includes for Jekyll report (Report 02) — HTML for styling
includes_dir = ROOT_DIR / "docs" / "_includes"
includes_dir.mkdir(exist_ok=True)
combo_include_path = includes_dir / "report_02_eligibility_combos.md"
with open(combo_include_path, "w") as f:
    f.write("".join(combo_html_lines))
print(f"Saved: {combo_include_path}")

# National Champions (place == 1): same eligibility-combo tables (1× NC, 2× NC, etc.)
champions_df = df_filtered[df_filtered["Place"] == 1]
nc_tiers = []
for wrestler in champions_df["Wrestler"].unique():
    w_df = champions_df[champions_df["Wrestler"] == wrestler]
    n_nc = len(w_df)
    eligs = w_df["Eligibility Year"].unique().tolist()
    elig_combo = tuple(sorted(eligs, key=lambda e: elig_order.index(e)))
    nc_tiers.append({"wrestler": wrestler, "n_nc": n_nc, "elig_combo": elig_combo})

nc_tiers_df = pd.DataFrame(nc_tiers)

def build_nc_combo_table(n_nc_val):
    """Build table rows for one N×NC tier: combinations that exist, sorted by count descending.
    Only include wrestlers whose number of distinct eligibility years equals n_nc.
    Each row includes a 'Wrestlers' column (comma-separated names, HTML-escaped) for tooltips."""
    sub = nc_tiers_df[(nc_tiers_df["n_nc"] == n_nc_val) & (nc_tiers_df["elig_combo"].apply(len) == n_nc_val)]
    if len(sub) == 0:
        return None, 0
    total = len(sub)
    combo_counts = sub.groupby("elig_combo").size().sort_values(ascending=False)
    rows = []
    for elig_combo, count in combo_counts.items():
        pct = count / total * 100
        names = sub[sub["elig_combo"] == elig_combo]["wrestler"].tolist()
        wrestlers_attr = html_module.escape(", ".join(names))
        row = {e: MARKER if e in elig_combo else "" for e in ELIG_COLS}
        row["Count"] = count
        row["%"] = f"{pct:.1f}%"
        row["Wrestlers"] = wrestlers_attr
        rows.append(row)
    return pd.DataFrame(rows), total

nc_cols = ELIG_COLS + ["Count", "%"]
nc_combo_md_lines = ["# When NC was won: combinations by eligibility year\n", "*National champions only (place = 1). Sorted by most common to least. ● = NC in that eligibility year.*\n"]
nc_combo_html_lines = ["<h1>When NC was won: combinations by eligibility year</h1>", "<p><em>National champions only (place = 1). Sorted by most common to least. Gold shaded cells = NC in that eligibility year.</em></p>"]
for n in [1, 2, 3, 4, 5]:
    nc_table, total_n = build_nc_combo_table(n)
    if nc_table is None or len(nc_table) == 0:
        continue
    nc_combo_md_lines.append(f"\n## {n}× NC (n = {total_n:,})\n\n")
    nc_combo_md_lines.append(nc_table[nc_cols].to_markdown(index=False) + "\n")
    nc_combo_html_lines.append(f"\n<h2 class=\"combo-tier-header\">{n}× Champs ({total_n:,})</h2>\n")
    nc_combo_html_lines.append(combo_df_to_html_nc(nc_table, nc_cols, wrestlers_col="Wrestlers", placement_lookup=wrestler_placement_str_combo) + "\n")
    print(f"  {n}× NC: {len(nc_table)} combinations (total wrestlers {total_n:,})")

nc_combo_table_path = TABLES_DIR / "nc_eligibility_combos_by_tier.md"
with open(nc_combo_table_path, "w") as f:
    f.write("".join(nc_combo_md_lines))
print(f"Saved: {nc_combo_table_path}")

# Tooltip + click-to-expand for ALL combo tables (NC and AA)
nc_combo_html_lines.append("""
<script>
(function() {
  var tip = null;
  var expandContainer = null;
  var allRows = null;

  function ensureTooltipStyles() {
    if (document.getElementById('wrestler-tooltip-styles')) return;
    var style = document.createElement('style');
    style.id = 'wrestler-tooltip-styles';
    style.textContent = '.wrestler-tooltip{position:fixed;background:#fff;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12);padding:12px;font-size:0.85rem;line-height:1.5;max-height:400px;max-width:500px;overflow-y:auto;overflow-x:hidden;z-index:1000;pointer-events:none;border:1px solid #e2e8f0;white-space:normal}.wrestler-tooltip .wrestler-tooltip-title{font-weight:600;margin-bottom:6px;color:#1a1a1a}.wrestler-tooltip .wrestler-tooltip-list{margin:0;padding-left:1.2em}';
    document.head.appendChild(style);
  }

  var COMBO_DELIM = ' | ';
  function showTip(el, x, y) {
    var listStr = el.getAttribute('data-wrestlers-places') || el.getAttribute('data-wrestlers');
    var n = el.getAttribute('data-count');
    if (!listStr || !tip) return;
    var title = tip.querySelector('.wrestler-tooltip-title');
    var list = tip.querySelector('.wrestler-tooltip-list');
    title.textContent = n + ' Wrestlers';
    var items = listStr.indexOf(COMBO_DELIM) !== -1 ? listStr.split(COMBO_DELIM) : listStr.split(/,\\s*/);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    tip.style.left = (x + 16) + 'px';
    tip.style.top = (y - 10) + 'px';
    tip.style.display = 'block';
  }
  function hideTip() { if (tip) tip.style.display = 'none'; }

  function showExpand(tr) {
    var listStr = tr.getAttribute('data-wrestlers-places') || tr.getAttribute('data-wrestlers');
    var n = tr.getAttribute('data-count');
    if (!listStr || !expandContainer) return;
    allRows.forEach(function(r) { r.classList.remove('combo-row-selected'); });
    tr.classList.add('combo-row-selected');
    var title = expandContainer.querySelector('.combo-expand-title');
    var list = expandContainer.querySelector('.combo-expand-list');
    title.textContent = n + ' Wrestlers';
    var items = listStr.indexOf(COMBO_DELIM) !== -1 ? listStr.split(COMBO_DELIM) : listStr.split(/,\\s*/);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    var table = tr.closest('table');
    if (table.nextSibling !== expandContainer) {
      if (expandContainer.parentNode) expandContainer.parentNode.removeChild(expandContainer);
      table.parentNode.insertBefore(expandContainer, table.nextSibling);
    }
    expandContainer.classList.add('is-visible');
  }
  function hideExpand() {
    if (expandContainer) expandContainer.classList.remove('is-visible');
    if (allRows) allRows.forEach(function(r) { r.classList.remove('combo-row-selected'); });
  }

  document.addEventListener('DOMContentLoaded', function() {
    ensureTooltipStyles();
    tip = document.createElement('div');
    tip.className = 'wrestler-tooltip';
    tip.innerHTML = '<div class="wrestler-tooltip-title"></div><ul class="wrestler-tooltip-list"></ul>';
    tip.style.display = 'none';
    document.body.appendChild(tip);

    expandContainer = document.createElement('div');
    expandContainer.id = 'combo-expand-container';
    expandContainer.className = 'combo-expand-container';
    expandContainer.innerHTML = '<div class="combo-expand-title"></div><ul class="combo-expand-list"></ul>';

    allRows = document.querySelectorAll('.eligibility-combo-table tbody tr[data-wrestlers]');
    allRows.forEach(function(tr) {
      tr.addEventListener('mouseenter', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mousemove', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mouseleave', hideTip);
      tr.addEventListener('click', function() {
        if (tr.classList.contains('combo-row-selected')) {
          hideExpand();
        } else {
          showExpand(tr);
        }
      });
    });
  });
})();
</script>
""")

nc_combo_include_path = includes_dir / "report_02_nc_eligibility_combos.md"
with open(nc_combo_include_path, "w") as f:
    f.write("".join(nc_combo_html_lines))
print(f"Saved: {nc_combo_include_path}")

# For each multi-AA wrestler: sort by Year, get Place sequence; "improved every year" = strictly better placement each time (lower place number = better)
def improved_every_year(places):
    """True if placement strictly improved each consecutive year (place values strictly decreasing)."""
    if len(places) < 2:
        return False
    return all(places[i] > places[i + 1] for i in range(len(places) - 1))

progression_rows = []
improved_wrestlers = []

for wrestler in multi_aa_wrestlers.index:
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler].sort_values("Year")
    places = w_df["Place"].tolist()
    years = w_df["Year"].tolist()
    eligs = w_df["Eligibility Year"].tolist()
    if improved_every_year(places):
        improved_wrestlers.append(wrestler)
        progression_str = "-".join(str(p) for p in places)
        year_str = "-".join(str(y) for y in years)
        n_appearances = len(places)
        progression_rows.append({
            "Wrestler": wrestler,
            "Progression": progression_str,
            "Years": year_str,
            "Eligibility sequence": "-".join(eligs),
            "AA count": n_appearances,
        })

n_improved = len(improved_wrestlers)
pct_improved_of_multi = (n_improved / n_multi_aa * 100) if n_multi_aa else 0
pct_improved_of_all = (n_improved / n_unique_wrestlers * 100) if n_unique_wrestlers else 0

print(f"Multi-AA wrestlers who improved every year (strictly better place each time): {n_improved:,}")
print(f"  → {pct_improved_of_multi:.1f}% of multi-AA wrestlers")
print(f"  → {pct_improved_of_all:.1f}% of all unique wrestlers")

# Build progression table (for export and narrative)
progression_df = pd.DataFrame(progression_rows)
if len(progression_df) > 0:
    progression_df = progression_df.sort_values("Progression")  # e.g. 2-1, 3-2-1, 4-3-2-1
    print(f"\nProgression sequences (improved every year):")
    print(progression_df[["Wrestler", "Progression", "Years", "AA count"]].to_string(index=False))
else:
    print("\nNo wrestlers with strictly improving placement every year.")

# ==============================================================================
# PROGRESSION ARCHETYPES (counts for Report 02)
# ==============================================================================
# Classify each wrestler with complete career into progression archetypes.
# Wrestlers can match multiple archetypes. Uses same eligibility exclusion: df_filtered only.

def classify_archetype(places):
    """
    places: list of int, ordered chronologically (e.g., [4, 3, 2, 1])
    Returns: list of archetype names that apply (1-6 only; Last Chance handled separately).
    """
    archetypes = []

    # 1. Continued Progression: 3+ AA, strictly improving each year
    if len(places) >= 3 and all(places[i] > places[i + 1] for i in range(len(places) - 1)):
        archetypes.append("Continued Progression")

    # 2. Plateau Breaker: 3+ AA, 2+ consecutive same placement then improvement
    if len(places) >= 3:
        for i in range(len(places) - 2):
            if places[i] == places[i + 1] and places[i + 2] < places[i]:
                archetypes.append("Plateau Breaker")
                break

    # 3. Regression Survivor: 3+ AA, drops 3+ places then returns to within 1 of previous best
    if len(places) >= 3:
        for i in range(len(places) - 2):
            drop = places[i + 1] - places[i]
            if drop >= 3:  # dropped 3+ places
                best_before = min(places[: i + 1])
                for j in range(i + 2, len(places)):
                    if places[j] <= best_before + 1:
                        archetypes.append("Regression Survivor")
                        break
                else:
                    continue
                break

    # 4. Consistent Elite: 3+ AA, never won (all > 1), all placements 2-4
    if len(places) >= 3 and all(p > 1 for p in places) and all(p <= 4 for p in places):
        archetypes.append("Consistent Elite")

    # 5. Early Peak: 3+ AA, best placement in first half, final >= best+2
    if len(places) >= 3:
        best_place = min(places)
        best_index = places.index(best_place)
        midpoint = len(places) // 2
        if best_index < midpoint and places[-1] >= best_place + 2:
            archetypes.append("Early Peak")

    # 6. Finish on a Win: 3+ AA, all odd placements (1,3,5,7)
    if len(places) >= 3 and all(p % 2 == 1 for p in places):
        archetypes.append("Finish on a Win")

    return archetypes


# Build per-wrestler place sequences (chronological: Year then eligibility order)
# Store counts by number of AAs (3×, 4×, 5×); all six placement archetypes require 3+ AA. 5+ AAs grouped as 5×.
elig_sort_key = {e: i for i, e in enumerate(ELIGIBILITY_ORDER)}
AA_BUCKETS = ("3", "4", "5")

def make_by_aa():
    return {b: 0 for b in AA_BUCKETS}

archetype_counts = {
    "Continued Progression": {"by_aa": make_by_aa()},   # 3+ AA only → 3,4,5
    "Plateau Breaker": {"by_aa": make_by_aa()},
    "Regression Survivor": {"by_aa": make_by_aa()},
    "Consistent Elite": {"by_aa": make_by_aa()},
    "Early Peak": {"by_aa": make_by_aa()},
    "Finish on a Win": {"by_aa": make_by_aa()},       # 3+ AA → 3,4,5
    "Last Chance": {
        "Senior Last Chance": {"by_aa": {"1": 0}},
        "COVID Last Chance": {"by_aa": {"1": 0}},
        "Championship Last Chance": {"by_aa": {"1": 0}},
    },
}
# Wrestler names per archetype per bucket (for tooltip and expand in report)
ARCHETYPE_NAMES = ["Continued Progression", "Plateau Breaker", "Regression Survivor", "Consistent Elite", "Early Peak", "Finish on a Win"]
archetype_wrestlers = {name: {b: [] for b in AA_BUCKETS} for name in ARCHETYPE_NAMES}
last_chance_wrestlers = {"Senior Last Chance": [], "COVID Last Chance": [], "Championship Last Chance": []}

for wrestler in df_filtered["Wrestler"].unique():
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler].copy()
    w_df["_order"] = w_df["Year"] * 10 + w_df["Eligibility Year"].map(elig_sort_key)
    w_df = w_df.sort_values(["_order", "Year", "Eligibility Year"])
    places = w_df["Place"].tolist()
    eligs = w_df["Eligibility Year"].tolist()
    years = w_df["Year"].tolist()
    n_aa = len(places)
    n_aa_key = str(min(n_aa, 5))  # 5+ → "5"

    # Archetypes 1-6 (from place sequence)
    for name in classify_archetype(places):
        if n_aa_key in archetype_counts[name]["by_aa"]:
            archetype_counts[name]["by_aa"][n_aa_key] += 1
            archetype_wrestlers[name][n_aa_key].append(wrestler)

    # 7. Last Chance (1× AA only) — collect wrestler names for tooltip/expand
    if n_aa == 1:
        elig = eligs[0]
        year = int(years[0])
        place = int(places[0])
        if elig in ("Sr", "SSr"):
            archetype_counts["Last Chance"]["Senior Last Chance"]["by_aa"]["1"] += 1
            last_chance_wrestlers["Senior Last Chance"].append(wrestler)
        if elig == "SSr" and year >= 2021:
            archetype_counts["Last Chance"]["COVID Last Chance"]["by_aa"]["1"] += 1
            last_chance_wrestlers["COVID Last Chance"].append(wrestler)
        if place == 1 and elig in ("Sr", "SSr"):
            archetype_counts["Last Chance"]["Championship Last Chance"]["by_aa"]["1"] += 1
            last_chance_wrestlers["Championship Last Chance"].append(wrestler)

# Add totals and ensure JSON-serializable (int)
for name in ["Continued Progression", "Plateau Breaker", "Regression Survivor", "Consistent Elite", "Early Peak", "Finish on a Win"]:
    by_aa = archetype_counts[name]["by_aa"]
    archetype_counts[name]["total"] = sum(by_aa.values())
    archetype_counts[name]["by_aa"] = {k: int(v) for k, v in by_aa.items()}
for sub in ["Senior Last Chance", "COVID Last Chance", "Championship Last Chance"]:
    by_aa = archetype_counts["Last Chance"][sub]["by_aa"]
    archetype_counts["Last Chance"][sub]["total"] = sum(by_aa.values())
    archetype_counts["Last Chance"][sub]["by_aa"] = {k: int(v) for k, v in by_aa.items()}

print("\nProgression archetype counts (complete careers only), by # of AAs (3×, 4×, 5×):")
for name in ["Continued Progression", "Plateau Breaker", "Regression Survivor", "Consistent Elite", "Early Peak", "Finish on a Win"]:
    total = archetype_counts[name]["total"]
    by_aa = archetype_counts[name]["by_aa"]
    print(f"  {name}: {total:,} total — 3×: {by_aa['3']}, 4×: {by_aa['4']}, 5×: {by_aa['5']}")
print("  Last Chance (1× only):")
print(f"    Senior Last Chance: {archetype_counts['Last Chance']['Senior Last Chance']['total']:,}")
print(f"    COVID Last Chance: {archetype_counts['Last Chance']['COVID Last Chance']['total']:,}")
print(f"    Championship Last Chance: {archetype_counts['Last Chance']['Championship Last Chance']['total']:,}")

# Build placement-by-eligibility string for each wrestler: "Name (Fr-So-Jr-Sr)" or "Name (Fr-So-Jr-Sr-SSr)"
# Use DNP for years with no AA; include SSr only if wrestler has SSr in data.
def wrestler_placement_string(wrestler, w_df):
    w_df = w_df.sort_values(["_order", "Year", "Eligibility Year"])
    elig_to_place = {}
    for _, row in w_df.iterrows():
        elig_to_place[row["Eligibility Year"]] = int(row["Place"])
    order = ["Fr", "So", "Jr", "Sr"]
    if "SSr" in elig_to_place:
        order.append("SSr")
    parts = [str(elig_to_place.get(e, "DNP")) for e in order]
    return f"{wrestler} ({'-'.join(parts)})"

# Precompute placement strings for all wrestlers in df_filtered (need _order on each w_df)
wrestler_placement_str = {}
for wrestler in df_filtered["Wrestler"].unique():
    w_df = df_filtered[df_filtered["Wrestler"] == wrestler].copy()
    w_df["_order"] = w_df["Year"] * 10 + w_df["Eligibility Year"].map(elig_sort_key)
    wrestler_placement_str[wrestler] = wrestler_placement_string(wrestler, w_df)

# Delimiter for list of "Name (a-b-c-d)" in data attribute (split in JS)
ARCHETYPE_LIST_DELIM = " | "

# Archetypes table HTML for Report 02: tooltip on count cells, click row to expand 3×/4×/5× lists
ARCHETYPE_DESCRIPTIONS = {
    "Continued Progression": "3+ AA; each consecutive AA shows improvement (place[i+1] &lt; place[i])",
    "Plateau Breaker": "3+ AA; 2+ consecutive years same placement, then improvement",
    "Regression Survivor": "3+ AA; drops 3+ places then returns to within 1 of previous best",
    "Consistent Elite": "3+ AA; never won (no 1st); all placements 2–4",
    "Early Peak": "3+ AA; best placement in first half of career; final placement ≥ best + 2",
    "Finish on a Win": "3+ AA; all placements odd (1, 3, 5, 7)—won final match every year",
}
archetype_table_lines = [
    '<table class="archetype-table">',
    "<thead><tr><th>Archetype</th><th>Description</th><th>Total</th><th>3× AA</th><th>4× AA</th><th>5× AA</th></tr></thead>",
    "<tbody>",
]
for name in ARCHETYPE_NAMES:
    total = archetype_counts[name]["total"]
    by_aa = archetype_counts[name]["by_aa"]
    desc = ARCHETYPE_DESCRIPTIONS[name]
    # Each 3×/4×/5× cell: data-wrestlers (names), data-wrestlers-places (Name (Fr-So-Jr-Sr)), data-count
    w3 = archetype_wrestlers[name]["3"]
    w4 = archetype_wrestlers[name]["4"]
    w5 = archetype_wrestlers[name]["5"]
    places3 = ARCHETYPE_LIST_DELIM.join([wrestler_placement_str[w] for w in sorted(w3)]) if w3 else ""
    places4 = ARCHETYPE_LIST_DELIM.join([wrestler_placement_str[w] for w in sorted(w4)]) if w4 else ""
    places5 = ARCHETYPE_LIST_DELIM.join([wrestler_placement_str[w] for w in sorted(w5)]) if w5 else ""
    attr3 = f' data-wrestlers="{html_module.escape(", ".join(sorted(w3)))}" data-wrestlers-places="{html_module.escape(places3)}" data-count="{by_aa["3"]}"' if w3 else ""
    attr4 = f' data-wrestlers="{html_module.escape(", ".join(sorted(w4)))}" data-wrestlers-places="{html_module.escape(places4)}" data-count="{by_aa["4"]}"' if w4 else ""
    attr5 = f' data-wrestlers="{html_module.escape(", ".join(sorted(w5)))}" data-wrestlers-places="{html_module.escape(places5)}" data-count="{by_aa["5"]}"' if w5 else ""
    row_attrs = f' data-wrestlers-3="{html_module.escape(", ".join(sorted(w3)))}" data-wrestlers-places-3="{html_module.escape(places3)}" data-count-3="{by_aa["3"]}"'
    row_attrs += f' data-wrestlers-4="{html_module.escape(", ".join(sorted(w4)))}" data-wrestlers-places-4="{html_module.escape(places4)}" data-count-4="{by_aa["4"]}"'
    row_attrs += f' data-wrestlers-5="{html_module.escape(", ".join(sorted(w5)))}" data-wrestlers-places-5="{html_module.escape(places5)}" data-count-5="{by_aa["5"]}"'
    archetype_table_lines.append(f"<tr{row_attrs}>")
    archetype_table_lines.append(f"<td><strong>{html_module.escape(name)}</strong></td>")
    archetype_table_lines.append(f"<td>{desc}</td>")
    archetype_table_lines.append(f"<td>{total}</td>")
    archetype_table_lines.append(f'<td class="archetype-cell"{attr3}>{by_aa["3"]}</td>')
    archetype_table_lines.append(f'<td class="archetype-cell"{attr4}>{by_aa["4"]}</td>')
    archetype_table_lines.append(f'<td class="archetype-cell"{attr5}>{by_aa["5"]}</td>')
    archetype_table_lines.append("</tr>")
archetype_table_lines.append("</tbody></table>")

archetype_script = """
<script>
(function() {
  var tip = null;
  var expandContainer = null;
  var expandedRow = null;

  function ensureTooltipStyles() {
    if (document.getElementById('wrestler-tooltip-styles')) return;
    var style = document.createElement('style');
    style.id = 'wrestler-tooltip-styles';
    style.textContent = '.wrestler-tooltip{position:fixed;background:#fff;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12);padding:12px;font-size:0.85rem;line-height:1.5;max-height:400px;max-width:500px;overflow-y:auto;overflow-x:hidden;z-index:1000;pointer-events:none;border:1px solid #e2e8f0;white-space:normal}.wrestler-tooltip .wrestler-tooltip-title{font-weight:600;margin-bottom:6px;color:#1a1a1a}.wrestler-tooltip .wrestler-tooltip-list{margin:0;padding-left:1.2em}';
    document.head.appendChild(style);
  }
  var PLACES_DELIM = ' | ';
  function getDisplayList(el, attrPlaces, attrNames) {
    var places = el.getAttribute(attrPlaces);
    if (places) return places.split(PLACES_DELIM);
    var names = el.getAttribute(attrNames);
    return names ? names.split(/,\\s*/) : [];
  }
  function showTip(el, x, y) {
    var listStr = el.getAttribute('data-wrestlers-places') || el.getAttribute('data-wrestlers');
    var n = el.getAttribute('data-count');
    if (!listStr || !tip) return;
    var title = tip.querySelector('.wrestler-tooltip-title');
    var list = tip.querySelector('.wrestler-tooltip-list');
    title.textContent = n + ' Wrestlers';
    var items = listStr.indexOf(PLACES_DELIM) !== -1 ? listStr.split(PLACES_DELIM) : listStr.split(/,\\s*/);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    tip.style.left = (x + 16) + 'px';
    tip.style.top = (y - 10) + 'px';
    tip.style.display = 'block';
  }
  function hideTip() { if (tip) tip.style.display = 'none'; }

  function showExpand(tr) {
    var list3 = getDisplayList(tr, 'data-wrestlers-places-3', 'data-wrestlers-3');
    var list4 = getDisplayList(tr, 'data-wrestlers-places-4', 'data-wrestlers-4');
    var list5 = getDisplayList(tr, 'data-wrestlers-places-5', 'data-wrestlers-5');
    var n3 = tr.getAttribute('data-count-3') || '0';
    var n4 = tr.getAttribute('data-count-4') || '0';
    var n5 = tr.getAttribute('data-count-5') || '0';
    if (!expandContainer) return;
    document.querySelectorAll('.archetype-table tbody tr').forEach(function(r) { r.classList.remove('archetype-row-selected'); });
    tr.classList.add('archetype-row-selected');
    var html = '<div class="archetype-expand-section"><strong>3× AA (' + n3 + ')</strong><ul class="archetype-expand-list">' + list3.map(function(n){ return '<li>' + n + '</li>'; }).join('') + '</ul></div>';
    html += '<div class="archetype-expand-section"><strong>4× AA (' + n4 + ')</strong><ul class="archetype-expand-list">' + list4.map(function(n){ return '<li>' + n + '</li>'; }).join('') + '</ul></div>';
    html += '<div class="archetype-expand-section"><strong>5× AA (' + n5 + ')</strong><ul class="archetype-expand-list">' + list5.map(function(n){ return '<li>' + n + '</li>'; }).join('') + '</ul></div>';
    expandContainer.querySelector('.archetype-expand-body').innerHTML = html;
    var table = tr.closest('table');
    if (table.nextSibling !== expandContainer) {
      if (expandContainer.parentNode) expandContainer.parentNode.removeChild(expandContainer);
      table.parentNode.insertBefore(expandContainer, table.nextSibling);
    }
    expandContainer.classList.add('is-visible');
    expandedRow = tr;
  }
  function hideExpand() {
    if (expandContainer) expandContainer.classList.remove('is-visible');
    document.querySelectorAll('.archetype-table tbody tr').forEach(function(r) { r.classList.remove('archetype-row-selected'); });
    expandedRow = null;
  }

  document.addEventListener('DOMContentLoaded', function() {
    ensureTooltipStyles();
    tip = document.createElement('div');
    tip.className = 'wrestler-tooltip';
    tip.innerHTML = '<div class="wrestler-tooltip-title"></div><ul class="wrestler-tooltip-list"></ul>';
    tip.style.display = 'none';
    document.body.appendChild(tip);

    expandContainer = document.createElement('div');
    expandContainer.id = 'archetype-expand-container';
    expandContainer.className = 'archetype-expand-container';
    expandContainer.innerHTML = '<div class="archetype-expand-body"></div>';

    var cells = document.querySelectorAll('.archetype-table .archetype-cell[data-wrestlers]');
    cells.forEach(function(td) {
      td.addEventListener('mouseenter', function(e) { showTip(td, e.clientX, e.clientY); });
      td.addEventListener('mousemove', function(e) { showTip(td, e.clientX, e.clientY); });
      td.addEventListener('mouseleave', hideTip);
    });
    var rows = document.querySelectorAll('.archetype-table tbody tr');
    rows.forEach(function(tr) {
      tr.style.cursor = 'pointer';
      tr.addEventListener('click', function() {
        if (tr.classList.contains('archetype-row-selected')) hideExpand();
        else showExpand(tr);
      });
    });
  });
})();
</script>
"""

archetype_include_path = includes_dir / "report_02_archetypes_table.md"
with open(archetype_include_path, "w") as f:
    f.write("\n".join(archetype_table_lines) + "\n" + archetype_script)
print(f"Saved: {archetype_include_path}")

# Last Chance table: hover and click on whole row for tooltip/expand (same placement format)
LAST_CHANCE_CRITERIA = {
    "Senior Last Chance": "1× AA; AA earned as Sr or SSr",
    "COVID Last Chance": "1× AA; earned as SSr in 2021 or later (COVID extension)",
    "Championship Last Chance": "1× NC (place = 1); NC earned as Sr or SSr",
}
last_chance_table_lines = [
    '<table class="last-chance-table">',
    "<thead><tr><th>Sub-type</th><th>Criteria</th><th>Count</th></tr></thead>",
    "<tbody>",
]
for sub in ["Senior Last Chance", "COVID Last Chance", "Championship Last Chance"]:
    wrestlers = last_chance_wrestlers[sub]
    total = len(wrestlers)
    places_str = ARCHETYPE_LIST_DELIM.join([wrestler_placement_str[w] for w in sorted(wrestlers)]) if wrestlers else ""
    names_str = ", ".join(sorted(wrestlers)) if wrestlers else ""
    row_attrs = ""
    if wrestlers:
        row_attrs = f' data-wrestlers="{html_module.escape(names_str)}" data-wrestlers-places="{html_module.escape(places_str)}" data-count="{total}"'
    last_chance_table_lines.append(f"<tr{row_attrs}>")
    last_chance_table_lines.append(f"<td><strong>{html_module.escape(sub)}</strong></td>")
    last_chance_table_lines.append(f"<td>{LAST_CHANCE_CRITERIA[sub]}</td>")
    last_chance_table_lines.append(f"<td>{total}</td>")
    last_chance_table_lines.append("</tr>")
last_chance_table_lines.append("</tbody></table>")

last_chance_script = """
<script>
(function() {
  var PLACES_DELIM = ' | ';
  var tip = document.querySelector('.wrestler-tooltip');
  var lcExpandContainer = null;

  function ensureTip() {
    if (tip) return;
    var style = document.getElementById('wrestler-tooltip-styles');
    if (!style) {
      style = document.createElement('style');
      style.id = 'wrestler-tooltip-styles';
      style.textContent = '.wrestler-tooltip{position:fixed;background:#fff;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.12);padding:12px;font-size:0.85rem;line-height:1.5;max-height:400px;max-width:500px;overflow-y:auto;overflow-x:hidden;z-index:1000;pointer-events:none;border:1px solid #e2e8f0;white-space:normal}.wrestler-tooltip .wrestler-tooltip-title{font-weight:600;margin-bottom:6px;color:#1a1a1a}.wrestler-tooltip .wrestler-tooltip-list{margin:0;padding-left:1.2em}';
      document.head.appendChild(style);
    }
    tip = document.createElement('div');
    tip.className = 'wrestler-tooltip';
    tip.innerHTML = '<div class="wrestler-tooltip-title"></div><ul class="wrestler-tooltip-list"></ul>';
    tip.style.display = 'none';
    document.body.appendChild(tip);
  }
  function showTip(tr, x, y) {
    var listStr = tr.getAttribute('data-wrestlers-places') || tr.getAttribute('data-wrestlers');
    var n = tr.getAttribute('data-count');
    if (!listStr || !tip) return;
    var title = tip.querySelector('.wrestler-tooltip-title');
    var list = tip.querySelector('.wrestler-tooltip-list');
    title.textContent = n + ' Wrestlers';
    var items = listStr.indexOf(PLACES_DELIM) !== -1 ? listStr.split(PLACES_DELIM) : listStr.split(/,\\s*/);
    list.innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    tip.style.left = (x + 16) + 'px';
    tip.style.top = (y - 10) + 'px';
    tip.style.display = 'block';
  }
  function hideTip() { if (tip) tip.style.display = 'none'; }
  function showLcExpand(tr) {
    var listStr = tr.getAttribute('data-wrestlers-places') || tr.getAttribute('data-wrestlers');
    var n = tr.getAttribute('data-count');
    if (!lcExpandContainer) return;
    document.querySelectorAll('.last-chance-table tbody tr[data-wrestlers]').forEach(function(r) { r.classList.remove('lc-row-selected'); });
    tr.classList.add('lc-row-selected');
    var items = listStr && listStr.indexOf(PLACES_DELIM) !== -1 ? listStr.split(PLACES_DELIM) : (listStr ? listStr.split(/,\\s*/) : []);
    lcExpandContainer.querySelector('.lc-expand-title').textContent = n + ' Wrestlers';
    lcExpandContainer.querySelector('.lc-expand-list').innerHTML = items.map(function(item){ return '<li>' + item + '</li>'; }).join('');
    var table = tr.closest('table');
    if (table.nextSibling !== lcExpandContainer) {
      if (lcExpandContainer.parentNode) lcExpandContainer.parentNode.removeChild(lcExpandContainer);
      table.parentNode.insertBefore(lcExpandContainer, table.nextSibling);
    }
    lcExpandContainer.classList.add('is-visible');
  }
  function hideLcExpand() {
    if (lcExpandContainer) lcExpandContainer.classList.remove('is-visible');
    document.querySelectorAll('.last-chance-table tbody tr[data-wrestlers]').forEach(function(r) { r.classList.remove('lc-row-selected'); });
  }
  document.addEventListener('DOMContentLoaded', function() {
    ensureTip();
    lcExpandContainer = document.createElement('div');
    lcExpandContainer.className = 'last-chance-expand-container';
    lcExpandContainer.innerHTML = '<div class="lc-expand-title"></div><ul class="lc-expand-list"></ul>';
    var rows = document.querySelectorAll('.last-chance-table tbody tr[data-wrestlers]');
    rows.forEach(function(tr) {
      tr.style.cursor = 'pointer';
      tr.addEventListener('mouseenter', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mousemove', function(e) { showTip(tr, e.clientX, e.clientY); });
      tr.addEventListener('mouseleave', hideTip);
      tr.addEventListener('click', function() {
        if (tr.classList.contains('lc-row-selected')) hideLcExpand();
        else showLcExpand(tr);
      });
    });
  });
})();
</script>
"""

last_chance_include_path = includes_dir / "report_02_last_chance_table.md"
with open(last_chance_include_path, "w") as f:
    f.write("\n".join(last_chance_table_lines) + "\n" + last_chance_script)
print(f"Saved: {last_chance_include_path}")

# ==============================================================================
# EXPORT TABLES
# ==============================================================================

print("\n" + "="*60)
print("EXPORTING TABLES")
print("="*60)

# Table 1: Summary by Eligibility Year
total_champs = len(champions)
summary_data = []
for elig in ELIGIBILITY_ORDER:
    if elig in aa_by_eligibility.index:
        total_aa = int(aa_by_eligibility[elig])
        champs = int(champs_by_eligibility.get(elig, 0))
        pct_of_aas = total_aa / len(df) * 100
        pct_of_ncs = champs / total_champs * 100 if total_champs > 0 else 0
        summary_data.append({
            "Eligibility Year": elig,
            "All-Americans": total_aa,
            "% of AAs": f"{pct_of_aas:.1f}%",
            "National Champions": champs,
            "% of NCs": f"{pct_of_ncs:.1f}%"
        })

summary_df = pd.DataFrame(summary_data)

# Save as markdown table
md_table = summary_df.to_markdown(index=False)
table_path = TABLES_DIR / "eligibility_summary.md"
with open(table_path, "w") as f:
    f.write("# Eligibility Year Summary\n\n")
    f.write(md_table)
print(f"\nSaved: {table_path}")

# Report 2: Multi-AA and aesthetic progression table + stats (incl. funnel tiers)
report_02_stats = {
    "n_complete_careers": n_complete_careers,
    "n_unique_wrestlers": n_unique_wrestlers,
    "n_multi_aa": n_multi_aa,
    "n_multi_weight_aa": int(n_multi_weight_aa),
    "n_improved_every_year": n_improved,
    "pct_improved_of_multi_aa": round(pct_improved_of_multi, 1),
    "pct_improved_of_all": round(pct_improved_of_all, 1),
    "funnel": {
        "all": n_unique_wrestlers,
        "n_1plus": int(n_1x),
        "n_2plus": int(n_2x),
        "n_3plus": int(n_3x),
        "n_4plus": int(n_4x),
        "n_5plus": int(n_5x),
    },
    "five_x_aa_wrestlers": sorted(aa_counts_per_wrestler[aa_counts_per_wrestler >= 5].index.tolist()),
    "multi_weight_by_n": multi_weight_by_n,
    "weight_move_stats": weight_move_stats,
    "wrestlers_4_weights": wrestlers_4_weights,
    "archetypes": archetype_counts,
}
report_02_path = REPORT_DATA_DIR / "report_02_stats.json"
with open(report_02_path, "w") as f:
    json.dump(report_02_stats, f, indent=2)
print(f"Saved: {report_02_path}")

if len(progression_df) > 0:
    prog_md = progression_df.to_markdown(index=False)
    prog_table_path = TABLES_DIR / "multi_aa_progression.md"
    with open(prog_table_path, "w") as f:
        f.write("# Multi-AA wrestlers who improved every year\n\n")
        f.write(f"*{n_improved} wrestlers out of {n_multi_aa} multi-AA wrestlers ({pct_improved_of_multi:.1f}%) had a strictly better placement each consecutive year.*\n\n")
        f.write(prog_md)
    print(f"Saved: {prog_table_path}")

# Print for verification
print("\n" + md_table)

# ==============================================================================
# REPORT STATS (for docs/report.md via Jekyll site.data.report_stats)
# ==============================================================================

ELIGIBILITY_LABELS = {
    "Fr": "Freshmen",
    "So": "Sophomores",
    "Jr": "Juniors",
    "Sr": "Seniors",
    "SSr": "Super Seniors",
}

total_aa = len(df)
report_stats = {
    "year_min": year_min,
    "year_max": year_max,
    "year_range": f"{year_min}–{year_max}",
    "nc": {},
    "aa": {},
}
for elig in ELIGIBILITY_ORDER:
    nc_count = int(champs_by_eligibility.get(elig, 0))
    aa_count = int(aa_by_eligibility.get(elig, 0))
    report_stats["nc"][elig] = {
        "count": nc_count,
        "pct": f"{nc_count / total_champs * 100:.1f}" if total_champs else "0",
        "label": ELIGIBILITY_LABELS[elig],
    }
    report_stats["aa"][elig] = {
        "count": aa_count,
        "pct": f"{aa_count / total_aa * 100:.1f}" if total_aa else "0",
        "label": ELIGIBILITY_LABELS[elig],
    }

report_stats_path = REPORT_DATA_DIR / "report_stats.json"
with open(report_stats_path, "w") as f:
    json.dump(report_stats, f, indent=2)
print(f"\nSaved: {report_stats_path}")

# ==============================================================================
# DONE
# ==============================================================================

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print(f"\nOutputs saved to:")
print(f"  Charts: {CHARTS_DIR}")
print(f"  Tables: {TABLES_DIR}")
print(f"  Report data (Jekyll): {REPORT_DATA_DIR}")
