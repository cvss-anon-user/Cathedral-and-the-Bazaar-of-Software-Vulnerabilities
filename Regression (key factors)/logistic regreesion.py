# Logistic regression. Note: This artifact does not include data from Company X
# # The file "merged_withVendor_info.csv" combined all necessary information we generated
# # for regression analysis (e.g., hamming distance, CVSS base score, CVSS base metrics).
# # Each CNA organizational type was manually reviewed and labeled.

import pandas as pd
import statsmodels.api as sm

# Load the Excel file
df = pd.read_csv("./merged_withVendor_info.csv")

# Create binary target: 1 if Hamming_Distance > 0, else 0
# ====================== TIP ==========================
# This approach can also use for any CVSS metric:
# Example: df['hamming_label'] = df['PR_Diff'].apply(lambda x: 0 if x == 0 else 1)
# =====================================================
df['hamming_label'] = df['Hamming_Distance'].apply(lambda x: 0 if x == 0 else 1)

# Define CNA predictors
predictors = [
    'Vendor', 'Open Source', 'Researcher',
    'Bug Bounty Provider', 'Hosted Service', 'CERT', 'Consortium'
]

# Drop rows with missing values in predictors or label
# ====================== TIP ==========================
# This approach can also use for any CVSS metric:
# Example: df_clean = df.dropna(subset=predictors + ['PR_Diff'])
# =====================================================
df_clean = df.dropna(subset=predictors + ['Hamming_Distance'])

# Drop constant columns (e.g., all 0s or all 1s)
predictors_filtered = [col for col in predictors if df_clean[col].nunique() > 1]

# Prepare design matrix
X = df_clean[predictors_filtered]
X = sm.add_constant(X)
y = df_clean['hamming_label']

# Fit logistic regression model
model = sm.Logit(y, X).fit()

# Extract summary and add significance
summary = model.summary2().tables[1][['Coef.', 'P>|z|']].copy()

# Add significance stars
def significance_marker(p):
    if p<0.05:
        return "significant"

summary['Significance'] = summary['P>|z|'].apply(significance_marker)

# Display
print(summary)