# Hamming Distance. Note: This artifact does not include data from Company X.
# The file "vulCheck_v31_Cleaned_withShortName.csv" used in this script
# removed CVE descriptions that contain "UNSUPPORTED WHEN ASSIGNED" from the original full dataset,
# and we manually annotate short names for each CNA.

import pandas as pd
import re

# === Load data (already includes ShortName) ===
file_path = "../Original Dataset/vulCheck_v31_Cleaned_withShortName.csv"
df = pd.read_csv(file_path)

nvd_source = "NVD"
metrics = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
records = []

# === Compare each CVE group ===
for cve_id, group in df.groupby("ID"):
    if nvd_source not in group["ShortName"].values:
        continue

    # Get NVD vector
    nvd_row = group[group["ShortName"] == nvd_source].iloc[0]
    nvd_vector_str = nvd_row.get("CVSS_Vector_v31", "")
    if not isinstance(nvd_vector_str, str) or not nvd_vector_str.startswith("CVSS:3.1/"):
        continue

    nvd_vector_parts = nvd_vector_str.replace("CVSS:3.1/", "").split("/")
    nvd_vector = dict(part.split(":") for part in nvd_vector_parts if ":" in part)

    # Compare with all non-NVD CNAs
    cna_group = group[group["ShortName"] != nvd_source]

    for _, row in cna_group.iterrows():
        cna = row["ShortName"]

        cna_vector_str = row.get("CVSS_Vector_v31", "")
        if not isinstance(cna_vector_str, str) or not cna_vector_str.startswith("CVSS:3.1/"):
            continue

        cna_vector_parts = cna_vector_str.replace("CVSS:3.1/", "").split("/")
        cna_vector = dict(part.split(":") for part in cna_vector_parts if ":" in part)

        result = {
            "ID": cve_id,
            "ShortName": cna,
        }

        hamming = 0
        for metric in metrics:
            if metric in nvd_vector and metric in cna_vector:
                diff = int(nvd_vector[metric] != cna_vector[metric])
                result[f"{metric}_Diff"] = diff
                hamming += diff
            else:
                result[f"{metric}_Diff"] = None  # One side is missing this metric

        result["Hamming_Distance"] = hamming
        records.append(result)

# === Save all CNA comparison results ===
hamming_df = pd.DataFrame(records)
# # Uncomment this code below you can save the result
# hamming_df.to_csv("Hamming_Distance_AllCNA.csv", index=False)
print("Saved to 'Hamming_Distance_AllCNA.csv'")

# === Calculate median Hamming distance per CNA ShortName ===
median_df = hamming_df.groupby("ShortName")["Hamming_Distance"].median().reset_index()
hamming_median = round(np.median(data["Hamming_List"])) if data["Hamming_List"] else 0
# # Uncomment this code below you can save the result
# median_df.to_csv("Median_d_withShortName.csv", index=False)
print("Saved to 'Median_d_withShortName.csv'")


