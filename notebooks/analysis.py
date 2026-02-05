"""
NCAA Wrestling All-Americans Eligibility Analysis
==================================================
Analyzes eligibility year patterns among NCAA D1 Wrestling All-Americans (2000-2024)
"""

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

# Ensure output directories exist
CHARTS_DIR.mkdir(exist_ok=True)
TABLES_DIR.mkdir(exist_ok=True)
SITE_CHARTS_DIR.mkdir(exist_ok=True)

# Plot style configuration for reproducibility
plt.style.use("default")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["font.family"] = "sans-serif"

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
# EXPORT TABLES
# ==============================================================================

print("\n" + "="*60)
print("EXPORTING TABLES")
print("="*60)

# Table 1: Summary by Eligibility Year
summary_data = []
for elig in ELIGIBILITY_ORDER:
    if elig in aa_by_eligibility.index:
        total_aa = int(aa_by_eligibility[elig])
        champs = int(champs_by_eligibility.get(elig, 0))
        pct_of_total = total_aa / len(df) * 100
        summary_data.append({
            "Eligibility Year": elig,
            "All-Americans": total_aa,
            "% of Total": f"{pct_of_total:.1f}%",
            "National Champions": champs
        })

summary_df = pd.DataFrame(summary_data)

# Save as markdown table
md_table = summary_df.to_markdown(index=False)
table_path = TABLES_DIR / "eligibility_summary.md"
with open(table_path, "w") as f:
    f.write("# Eligibility Year Summary\n\n")
    f.write(md_table)
print(f"\nSaved: {table_path}")

# Print for verification
print("\n" + md_table)

# ==============================================================================
# DONE
# ==============================================================================

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print(f"\nOutputs saved to:")
print(f"  Charts: {CHARTS_DIR}")
print(f"  Tables: {TABLES_DIR}")
