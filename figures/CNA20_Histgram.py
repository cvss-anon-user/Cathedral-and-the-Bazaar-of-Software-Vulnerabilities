# number of CVEs assigned by top 20 CNAs (figure 3)

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.rcParams['font.size'] = 20

# === Load data ===
file_path = "../PMDC/PMDC_withShortName.csv"
df = pd.read_csv(file_path)

# === Data cleaning ===
df["Counts"] = pd.to_numeric(df["Counts"], errors="coerce")
df["ShortName"] = df["ShortName"].astype(str)
df = df.dropna(subset=["Counts", "ShortName"])

top_20 = df.sort_values(by="Counts", ascending=False).head(20).reset_index(drop=True)

# === Prepare plot ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7))
upper_ylim = (4000, 17000)
lower_ylim = (0, 2200)

colors = ['lightsteelblue'] * len(top_20)

bars1 = ax1.bar(top_20['ShortName'], top_20['Counts'], color=colors)
bars2 = ax2.bar(top_20['ShortName'], top_20['Counts'], color=colors)

ax1.set_ylim(upper_ylim)
ax2.set_ylim(lower_ylim)

ax1.spines['bottom'].set_visible(False)
ax1.set_xticks([])
ax2.spines['top'].set_visible(False)

# === Add axis break lines ===
d = .015
kwargs = dict(color='k', clip_on=False)
ax1.plot((-d, +d), (-d, +d), transform=ax1.transAxes, **kwargs)
ax1.plot((1 - d, 1 + d), (-d, +d), transform=ax1.transAxes, **kwargs)
ax2.plot((-d, +d), (1 - d, 1 + d), transform=ax2.transAxes, **kwargs)
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), transform=ax2.transAxes, **kwargs)

# === Add value labels ===
for bar in bars1:
    if bar.get_height() > 2500:
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                 str(int(bar.get_height())), ha='center', va='bottom', rotation=90, fontsize=17)

for bar in bars2:
    if bar.get_height() < 2500:
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 str(int(bar.get_height())), ha='center', va='bottom', rotation=90, fontsize=17)

# === Set x-axis labels ===
ax2.set_xticklabels(top_20['ShortName'], rotation=40, ha='right')

# === Axis and label settings ===
ax1.tick_params(axis='y')
ax2.tick_params(axis='y')
ax1.set_ylabel("# of CVEs")

plt.tight_layout()
plt.show()