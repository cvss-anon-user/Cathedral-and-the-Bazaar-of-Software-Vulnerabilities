#  The growth of CNAs (figure 1(a))
# Note: This artifact does not include data from Company X

# Re-import required libraries after environment reset
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20
plt.rcParams['font.weight'] = 'normal'

# Load the dataset again
df = pd.read_csv("../Original Dataset/vulCheck_v31_Cleaned_withShortName.csv")

# Extract year from CVE ID
df['Year'] = df['ID'].str.extract(r'CVE-(\d{4})').astype(int)

# Filter out NVD entries
non_nvd_df = df[df['ShortName'] != 'NVD']

# Count unique CNAs per year that published CVEs
cna_counts_per_year = non_nvd_df.groupby('Year')['ShortName'].nunique().reset_index(name='Unique CNAs')
cna_counts_per_year = cna_counts_per_year[cna_counts_per_year['Year'] <= 2024]

# Create a zoom-in inset showing the range from 2000 to 2015
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# Main figure
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(cna_counts_per_year['Year'], cna_counts_per_year['Unique CNAs'], marker='o', color='teal', label='# of CNAs')
# ax.set_title("Number of Non-NVD CNAs Publishing CVEs per Year", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("# of CNAs")
# ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')

# Inset axes for zoom-in from 2000 to 2015
axins = inset_axes(ax, width="40%", height="40%", loc='center left', borderpad=2)
axins.plot(cna_counts_per_year['Year'], cna_counts_per_year['Unique CNAs'], marker='o', color='teal')
axins.set_xlim(2000, 2015)
axins.set_ylim(0, cna_counts_per_year[cna_counts_per_year['Year'].between(2000, 2015)]['Unique CNAs'].max() + 2)
axins.grid(True, linestyle='--', alpha=0.5)
axins.set_xticks([])
# axins.set_xticks([2000, 2005, 2010, 2015])

# Add lines connecting inset to main plot
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="gray", lw=1)

plt.show()