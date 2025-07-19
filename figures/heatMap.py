#  Per-Metric Disagreement Coefficient (figure 4(b))
# Note: This artifact does not include data from Company X

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Load summary data
summary_df = pd.read_csv("../PMDC/PMDC_withShortName.csv")
summary_df.columns = summary_df.columns.str.strip()
summary_df["Counts"] = pd.to_numeric(summary_df["Counts"], errors="coerce")

# Select top 20 CNA names by count
top20 = summary_df.sort_values(by="Counts", ascending=False).head(20)
cna_list = top20["ShortName"].tolist()

# Metrics to include in heatmap
metric_order = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]

# Extract PMDC values for each metric and CNA
heatmap_data = top20.set_index("ShortName")[[f"{m}_PMDC" for m in metric_order]].T
heatmap_data.columns = cna_list
heatmap_data.index = metric_order

# Plot
fig, ax = plt.subplots(figsize=(14, 4))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="1%", pad=0.1)

sns.heatmap(
    heatmap_data,
    ax=ax,
    cbar_ax=cax,
    annot=True,
    fmt=".2f",
    annot_kws={"size": 14},
    cmap="YlOrRd",
    linewidths=0.5
)

ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xticklabels(cna_list, rotation=30, ha="right", fontsize=15)
ax.set_yticklabels(metric_order, rotation=0, fontsize=15)
cax.tick_params(labelsize=14)

plt.tight_layout()
plt.show()