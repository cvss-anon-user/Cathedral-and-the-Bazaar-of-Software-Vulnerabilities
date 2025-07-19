# Linear regression CVSS(CNA)-CVSS(NVD). Note: This artifact does not include data from Company X
# The file "merged_withVendor_info.csv" combined all necessary information we generated
# for regression analysis (e.g., hamming distance, CVSS base score, CVSS base metrics).
# Each CNA organizational type was manually reviewed and annotated.

import pandas as pd
import statsmodels.api as sm

# === Load filtered conflict data ===
file_path = "./merged_withVendor_info.csv"
df = pd.read_csv(file_path)

# === Filter to conflict cases ===
df_conflict = df[
    (df["Hamming_Distance"] != 0) &
    (df["CVSS_BaseScore"] != df["CVSS_NVD_BaseScore"])
]

# === Define predictors and outcome ===
predictors = ['Vendor', 'Open Source', 'Researcher', 'Bug Bounty Provider', 'Hosted Service', 'CERT', 'Consortium']
df_conflict[predictors] = df_conflict[predictors].fillna(0)

# === Construct X and y ===
X = sm.add_constant(df_conflict[predictors])
y = df_conflict["CVSS_BaseScore"] - df_conflict["CVSS_NVD_BaseScore"]

# === Run regression ===
model = sm.OLS(y, X).fit()

# === Print coefficients and p-values ===
print("Regression Results: Y = CVSS(CNA) - CVSS(NVD)\n")
print("{:<15} {:>12} {:>15}".format("Variable", "Coefficient", "P-value"))
print("-" * 45)

for var in model.params.index:
    coef = model.params[var]
    pval = model.pvalues[var]
    # Format p-value in scientific notation if small
    if pval < 0.0001:
        pval_str = f"{pval:.1e}"
    else:
        pval_str = f"{pval:.4f}"
    print(f"{var:<15} {coef:>12.4f} {pval_str:>15}")
