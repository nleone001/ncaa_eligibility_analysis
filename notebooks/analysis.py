"""
NCAA Wrestling All-Americans Eligibility Analysis
==================================================
Analyzes eligibility year patterns among NCAA D1 Wrestling All-Americans (2000-2024)
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# Unique wrestlers (each row = one AA finish; Wrestler may appear multiple times)
n_unique_wrestlers = df["Wrestler"].nunique()
print(f"\nUnique wrestlers (all AAs): {n_unique_wrestlers:,}")

# Multi-AA: wrestlers who appear more than once (AAd more than once)
aa_counts_per_wrestler = df.groupby("Wrestler").size()
multi_aa_mask = aa_counts_per_wrestler > 1
multi_aa_wrestlers = aa_counts_per_wrestler[multi_aa_mask]
n_multi_aa = len(multi_aa_wrestlers)
print(f"Multi-AA wrestlers (AAd more than once): {n_multi_aa:,} out of {n_unique_wrestlers:,}")

# Funnel: wrestlers with 2+, 3+, 4+, 5+ AAs (cumulative)
n_2plus = (aa_counts_per_wrestler >= 2).sum()
n_3plus = (aa_counts_per_wrestler >= 3).sum()
n_4plus = (aa_counts_per_wrestler >= 4).sum()
n_5plus = (aa_counts_per_wrestler >= 5).sum()
funnel_counts = [n_unique_wrestlers, n_2plus, n_3plus, n_4plus, n_5plus]

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
ax.set_yticklabels(["1× AA", "2× AA", "3× AA", "4× AA", "5× AA"], fontsize=12)
ax.set_xlim(0, 1)
ax.set_xticks([])
for spine in ["top", "right", "bottom", "left"]:
    ax.spines[spine].set_visible(False)
ax.set_title("Unique wrestlers by multi-AA tier (2000–2025)", fontsize=14, fontweight="bold")
for i, yi in enumerate(y_pos):
    # 5× AA bar is tiny; use black text so the count is readable
    text_color = "black" if i == len(y_pos) - 1 else "white"
    ax.text(x_center, yi, f"  {funnel_counts[i]:,}  ", ha="center", va="center", fontsize=11, fontweight="bold", color=text_color)
plt.tight_layout()
funnel_path = CHARTS_DIR / "multi_aa_funnel.png"
funnel_site_path = SITE_CHARTS_DIR / "multi_aa_funnel.png"
plt.savefig(funnel_path, dpi=150)
plt.savefig(funnel_site_path, dpi=150)
plt.close()
print(f"Saved: {funnel_path}")
print(f"Saved: {funnel_site_path}")

# Eligibility-year combinations by N×AA tier (when AA was earned, by eligibility)
# For each wrestler: (n_aa, sorted tuple of eligibility years in which they AA'd)
elig_order = ELIGIBILITY_ORDER  # ["Fr", "So", "Jr", "Sr", "SSr"]
wrestler_tiers = []
for wrestler in df["Wrestler"].unique():
    w_df = df[df["Wrestler"] == wrestler]
    n_aa = len(w_df)
    eligs = w_df["Eligibility Year"].unique().tolist()
    elig_combo = tuple(sorted(eligs, key=lambda e: elig_order.index(e)))
    wrestler_tiers.append({"wrestler": wrestler, "n_aa": n_aa, "elig_combo": elig_combo})

tiers_df = pd.DataFrame(wrestler_tiers)

# Marker for "AA earned in this eligibility year"
MARKER = "●"
ELIG_COLS = ["Fr", "So", "Jr", "Sr", "SSr"]

def build_combo_table(n_aa_val):
    """Build table rows for one N×AA tier: combinations that exist, sorted by count descending."""
    sub = tiers_df[tiers_df["n_aa"] == n_aa_val]
    if len(sub) == 0:
        return None, 0
    total = len(sub)
    combo_counts = sub.groupby("elig_combo").size().sort_values(ascending=False)
    rows = []
    for elig_combo, count in combo_counts.items():
        pct = count / total * 100
        row = {e: MARKER if e in elig_combo else "" for e in ELIG_COLS}
        row["Count"] = count
        row["%"] = f"{pct:.1f}%"
        rows.append(row)
    return pd.DataFrame(rows), total

# Write combined markdown: one section per tier (1×, 2×, 3×, 4× AA)
combo_md_lines = ["# When AA was earned: combinations by eligibility year\n", "*Sorted by most common to least. ● = AA in that eligibility year.*\n"]
for n in [1, 2, 3, 4]:
    combo_table, total_n = build_combo_table(n)
    if combo_table is None or len(combo_table) == 0:
        continue
    combo_md_lines.append(f"\n## {n}× AA (n = {total_n:,})\n\n")
    # Reorder columns: Fr, So, Jr, Sr, SSr, Count, %
    cols = ELIG_COLS + ["Count", "%"]
    combo_md_lines.append(combo_table[cols].to_markdown(index=False) + "\n")
    print(f"  {n}× AA: {len(combo_table)} combinations (total wrestlers {total_n:,})")

combo_table_path = TABLES_DIR / "eligibility_combos_by_tier.md"
with open(combo_table_path, "w") as f:
    f.write("".join(combo_md_lines))
print(f"Saved: {combo_table_path}")

# Also write to docs/_includes for Jekyll report (Report 02)
includes_dir = ROOT_DIR / "docs" / "_includes"
includes_dir.mkdir(exist_ok=True)
combo_include_path = includes_dir / "report_02_eligibility_combos.md"
with open(combo_include_path, "w") as f:
    f.write("".join(combo_md_lines))
print(f"Saved: {combo_include_path}")

# For each multi-AA wrestler: sort by Year, get Place sequence; "improved every year" = strictly better placement each time (lower place number = better)
def improved_every_year(places):
    """True if placement strictly improved each consecutive year (place values strictly decreasing)."""
    if len(places) < 2:
        return False
    return all(places[i] > places[i + 1] for i in range(len(places) - 1))

progression_rows = []
improved_wrestlers = []

for wrestler in multi_aa_wrestlers.index:
    w_df = df[df["Wrestler"] == wrestler].sort_values("Year")
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
    "n_unique_wrestlers": n_unique_wrestlers,
    "n_multi_aa": n_multi_aa,
    "n_improved_every_year": n_improved,
    "pct_improved_of_multi_aa": round(pct_improved_of_multi, 1),
    "pct_improved_of_all": round(pct_improved_of_all, 1),
    "funnel": {
        "all": n_unique_wrestlers,
        "n_2plus": int(n_2plus),
        "n_3plus": int(n_3plus),
        "n_4plus": int(n_4plus),
        "n_5plus": int(n_5plus),
    },
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
