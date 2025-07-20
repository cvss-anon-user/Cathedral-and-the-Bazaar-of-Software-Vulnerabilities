# Data Clean. 
import pandas as pd
import re

# Note: Due to VulnCheck's licensing restrictions, we cannot redistribute the original 'vulCheck_v31.csv' file.
# Please replace this path with your own preprocessed dataset if needed.
# However, you may directly use the file 'vulCheck_v31_Cleaned_withShortName.csv',
# which is a cleaned version derived from the original data using our preprocessing script,
# and has been manually annotated with CNA organizational types.

file_path = "./vulCheck_v31.csv"
df = pd.read_csv(file_path)

# **UNSUPPORTED WHEN ASSIGNED, allow with or without space
pattern = r"^\*\*\s*UNSUPPORTED WHEN ASSIGNED"

# Cleaning
cleaned_df = df[~df['Description_en'].astype(str).str.match(pattern, na=False)].copy()
cleaned_path = "vulCheck_v31_Cleaned.csv"

# Generate clean data file
# # Uncomment this code below you can save the result
# cleaned_df.to_csv(cleaned_path, index=False)
print(f"🧹 Original rows: {len(df)}, After cleaning: {len(cleaned_df)}")
print(f"✅ Cleaned file saved to:\n{cleaned_path}")

# non-NVD
non_nvd_df = cleaned_df[cleaned_df["WeaknessSource"] != "nvd@nist.gov"]
num_non_nvd_rows = len(non_nvd_df)
num_unique_cnas = non_nvd_df["WeaknessSource"].nunique()

# NVD
nvd_df = cleaned_df[cleaned_df["WeaknessSource"] == "nvd@nist.gov"]
num_nvd_rows = len(nvd_df)

print(f"Number of rows where CNAs ≠ 'NVD': {num_non_nvd_rows}")
print(f"Number of rows where CNAs == 'NVD': {num_nvd_rows}")


