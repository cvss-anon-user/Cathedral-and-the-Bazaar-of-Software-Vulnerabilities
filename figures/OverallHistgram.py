# d medium value for 288 CNAs compared to the NVD -figure 5(a)
# Note: This artifact does not include data from Company X

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20

# Load CSV file
df = pd.read_csv('../PMDC/PMDC_withShortName.csv')

column_to_plot = 'd (median)'
data = df[column_to_plot].dropna()

# Define bins as integer boundaries (for bar centers at 0,1,2,...)
min_val = int(data.min())
max_val = int(data.max())
bins = range(min_val, max_val + 2)  # +2 to include the last value as a right edge

# Plot histogram
plt.figure(figsize=(6, 4))
n, bins, patches = plt.hist(data, bins=bins, edgecolor='black', color='skyblue', rwidth=0.6)

# Set xticks to bin centers
tick_positions = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
tick_labels = [int(p) for p in tick_positions]
plt.xticks(tick_positions, tick_labels)

# Axis labels
plt.xlabel('d (median)')
plt.ylabel('# of CNAs')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.990, bottom=0.148, left=0.195, right=0.964, hspace=0.0, wspace=0.0)
plt.show()
