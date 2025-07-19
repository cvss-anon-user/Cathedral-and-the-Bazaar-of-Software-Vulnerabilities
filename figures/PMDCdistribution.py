# PMDC for 288 CNAs compared to the NVD -figure 5(b)
# Note: This artifact does not include data from Company X

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.size'] = 15

# Load the Excel file
file_path = '../PMDC/PMDC_withShortName.csv'  # Replace with your actual file
df = pd.read_csv(file_path)

# Print all numeric columns
numeric_cols = df.select_dtypes(include='number').columns
print("Numeric columns available:", list(numeric_cols))

# Choose multiple columns to plot
columns_to_plot = ['AV_PMDC', 'AC_PMDC', 'PR_PMDC','UI_PMDC','S_PMDC','C_PMDC','I_PMDC','A_PMDC']  # Replace with your actual column names

# Plot distributions
markers = ['o', 's', '^', 'D', 'x', 'v', '*', 'P']
interval = 20  # Show marker every N points
metric_short_names = ['AV', 'AC', 'PR', 'UI', 'S', 'C', 'I', 'A']  # For mapping

# Create the plot
plt.figure(figsize=(8, 3))

for i, col in enumerate(columns_to_plot):
    values = sorted(df[col].dropna().values)
    x = range(len(values))
    
    plt.plot(x, values,
             marker=markers[i],
             markevery=interval,
             markersize=5,
             linewidth=1.8,
             markerfacecolor='white',
             markeredgewidth=3, label = metric_short_names[i])

# Final touches
# plt.title("Line Plot of PMDC Values with Distinct Sparse Markers")
plt.xlabel("# of CNAs")
plt.ylabel("Metric (PMDC)")
plt.legend(ncol=2,frameon=False,         # Removes legend border
    labelspacing=0.3,      # Tightens vertical spacing between items
    handletextpad=0.5 )
# plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.990,
bottom=0.148,
left=0.095,
right=0.964,
hspace=0.0,
wspace=0.0)

# plt.tight_layout()
plt.show()
