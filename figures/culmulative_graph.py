# Severity levels 1(b)
# Note: This artifact does not include data from Company X

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
plt.rcParams['font.size'] = 20

# === Load data ===
file_path = "./Summary_withShortName.csv"
df = pd.read_csv(file_path)


# === Clean and sort ===
df = df.dropna(subset=["Compare_Count", "NVD_Higher", "CNA_Higher", "Equal_Severity", "CNA_Critical", "NVD_Critical"])
df_sorted = df.sort_values(by="Compare_Count", ascending=False).head(50).reset_index(drop=True)

# === Prepare layers ===
x = np.arange(1, len(df_sorted) + 1)
cna_layer = df_sorted["CNA_Higher"].values
nvd_layer = df_sorted["NVD_Higher"].values
equal_layer = df_sorted["Equal_Severity"].values
cna_critical = df_sorted["CNA_Critical"].values
nvd_critical = df_sorted["NVD_Critical"].values

nvd_top = cna_layer + nvd_layer
equal_top = nvd_top + equal_layer

# === Main plot ===
fig, ax = plt.subplots(figsize=(8, 6))

# Fill main areas
ax.fill_between(x, 0, cna_layer, color='#2ca02c', alpha=0.6, label='CNA Higher')
ax.fill_between(x, cna_layer, nvd_top, color='orange', alpha=0.6, label='NVD Higher')
ax.fill_between(x, nvd_top, equal_top, color='#d3d3d3', alpha=0.6, label='Same level')

# Fill critical areas (darker)
ax.fill_between(x, 0, cna_critical, color='#1a661a', alpha=0.8, label='CNA Critical')
ax.fill_between(x, cna_layer, cna_layer + nvd_critical, color='#cc5500', alpha=0.8, label='NVD Critical')

# Area outlines
ax.plot(x, cna_layer, color='#2ca02c', linewidth=1)
ax.plot(x, nvd_top, color='#ff7f0e', linewidth=1)
ax.plot(x, equal_top, color='darkgrey', linewidth=1)

# Axes setup
ax.set_xlim(0.5, len(x) + 0.5)
ax.set_xlabel("CNAs Ranked by # of Common CVE Entries")
ax.set_ylabel("Number of CVE Entries")
ax.tick_params(axis='both')
ax.legend(loc='upper right', ncol = 2)
# ax.grid(alpha=0.3)

# === Inset Zoom ===
zoom_range = (x >= 20) & (x <= 50)
x_zoom = x[zoom_range]

axins = inset_axes(ax, width="40%", height="40%", loc='lower right', borderpad=3)

# Fill zoom areas
axins.fill_between(x_zoom, 0, cna_layer[zoom_range], color='#2ca02c', alpha=0.6)
axins.fill_between(x_zoom, cna_layer[zoom_range], nvd_top[zoom_range], color='orange', alpha=0.6)
axins.fill_between(x_zoom, nvd_top[zoom_range], equal_top[zoom_range], color='#d3d3d3', alpha=0.6)

# Fill critical zones in zoom
axins.fill_between(x_zoom, 0, cna_critical[zoom_range], color='#1a661a', alpha=0.8)
axins.fill_between(x_zoom, cna_layer[zoom_range], cna_layer[zoom_range] + nvd_critical[zoom_range], color='#cc5500', alpha=0.8)

# Outline
axins.plot(x_zoom, cna_layer[zoom_range], color='#2ca02c', linewidth=1)
axins.plot(x_zoom, nvd_top[zoom_range], color='#ff7f0e', linewidth=1)
axins.plot(x_zoom, equal_top[zoom_range], color='darkgrey', linewidth=1)

# Config
axins.set_xlim(20, 50)
axins.set_ylim(0, equal_top[zoom_range].max() + 100)
axins.set_xticks([])
axins.set_yticks([])
for spine in axins.spines.values():
    spine.set_visible(True)


mark_inset(ax, axins, loc1=2, loc2=1, fc="none", ec="gray", lw=1.5)

plt.tight_layout()
plt.show()