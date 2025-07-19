#  Distribution of Entry-level disagreememt 𝑑 values (figure 4(a))
# Note: This artifact does not include data from Company X

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load data
summary_df = pd.read_csv("../PMDC/PMDC_withShortName.csv")
hamming_df = pd.read_csv("../d metric/Hamming_Distance_AllCNA.csv")

# Clean column names
summary_df.columns = summary_df.columns.str.strip()
hamming_df.columns = hamming_df.columns.str.strip()

# Get top 20 CNA names by count
summary_df["Counts"] = pd.to_numeric(summary_df["Counts"], errors="coerce")
top20 = summary_df.sort_values(by="Counts", ascending=False).head(20)
cna_list = top20["ShortName"].tolist()

# Filter relevant data
filtered_df = hamming_df[hamming_df["ShortName"].isin(cna_list)]

# Compute median Hamming distance per CNA
medians = filtered_df.groupby("ShortName")["Hamming_Distance"].median().reindex(cna_list)

# Add MedianGroup column for coloring
filtered_df["MedianGroup"] = filtered_df["ShortName"].map(
    lambda name: int(round(medians[name])) if pd.notna(medians[name]) else -1
)

# Define palette based on median groups
palette_named = {
    0: "#66c2a5",
    1: "#FFD92F",
    2: "#fb8072",
    3: "#8da0cb"
}

# Create violin plot using hue for fill color
plt.figure(figsize=(14, 5))
sns.violinplot(
    data=filtered_df,
    x="ShortName",
    y="Hamming_Distance",
    hue="MedianGroup",
    palette=palette_named,
    order=cna_list,
    dodge=False,
    inner="box"
)

plt.ylabel("d-Disagreement Metric", fontsize=18)
plt.xlabel("")
plt.xticks(rotation=30, ha='right', fontsize=18)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Custom legend
legend_labels = {
    0: "Median = 0",
    1: "Median = 1",
    2: "Median = 2",
    3: "Median = 3"
}
legend_patches = [mpatches.Patch(color=palette_named[k], label=legend_labels[k]) for k in legend_labels]
plt.legend(
    handles=legend_patches,
    loc='upper center',
    bbox_to_anchor=(0.629, 1.185),
    ncol=4,
    frameon=True,
    fontsize=16
)

plt.tight_layout()
plt.show()