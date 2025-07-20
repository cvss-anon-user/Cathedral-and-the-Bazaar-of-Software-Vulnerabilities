# PMDC. Note: This artifact does not include data from Company X.
# The file "vulCheck_v31_Cleaned_withShortName.csv" used in this script
# removed CVE descriptions that contain "UNSUPPORTED WHEN ASSIGNED" from the original full dataset,
# and we manually annotate short names for each CNA.


import pandas as pd
import numpy as np
from collections import defaultdict

# === Load the dataset ===
df = pd.read_csv("../Original Dataset/vulCheck_v31_Cleaned_withShortName.csv")
df.columns = df.columns.str.strip()

metrics = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]

# === Initialize results container ===
summary = defaultdict(lambda: {
    "Counts": 0,
    "Compare_Count": 0,
    "inconsistent vector": 0,
    "Hamming_List": [],
    **{f"{m}_Diff": 0 for m in metrics}
})

# === Count CNA total entries (excluding NVD) ===
for name in df["ShortName"].dropna().unique():
    if name != "NVD":
        summary[name]["Counts"] = df[df["ShortName"] == name].shape[0]

# === Compare vectors by CVE-ID ===
for cve_id, group in df.groupby("ID"):
    if "NVD" not in group["ShortName"].values:
        continue

    nvd_row = group[group["ShortName"] == "NVD"].iloc[0]
    nvd_vector_str = nvd_row.get("CVSS_Vector_v31", "")
    if not isinstance(nvd_vector_str, str) or not nvd_vector_str.startswith("CVSS:3.1/"):
        continue

    nvd_vector_parts = nvd_vector_str.replace("CVSS:3.1/", "").split("/")
    nvd_vector = dict(part.split(":") for part in nvd_vector_parts if ":" in part)

    for _, row in group.iterrows():
        cna = row["ShortName"]
        if cna == "NVD":
            continue
        if pd.isna(row["CVSS_Vector_v31"]) or not str(row["CVSS_Vector_v31"]).startswith("CVSS:3.1/"):
            continue

        cna_vector_parts = row["CVSS_Vector_v31"].replace("CVSS:3.1/", "").split("/")
        cna_vector = dict(part.split(":") for part in cna_vector_parts if ":" in part)

        summary[cna]["Compare_Count"] += 1

        hamming = 0
        is_different = False
        for metric in metrics:
            if metric in nvd_vector and metric in cna_vector:
                diff = int(nvd_vector[metric] != cna_vector[metric])
                summary[cna][f"{metric}_Diff"] += diff
                hamming += diff
                if diff:
                    is_different = True

        summary[cna]["Hamming_List"].append(hamming)
        if is_different:
            summary[cna]["inconsistent vector"] += 1

# === Build final summary ===
records = []
for cna, data in summary.items():
    hamming_median = round(np.median(data["Hamming_List"])) if data["Hamming_List"] else 0
    record = {
        "ShortName": cna,
        "Counts": data["Counts"],
        "Compare_Count": data["Compare_Count"],
        "inconsistent vector": data["inconsistent vector"],
        "d (median)": hamming_median
    }
    for metric in metrics:
        diff = data[f"{metric}_Diff"]
        record[f"{metric}_Diff"] = diff
        record[f"{metric}_PMDC"] = round(diff / data["Compare_Count"], 4) if data["Compare_Count"] > 0 else 0
    records.append(record)

# === Save to CSV ===
output_df = pd.DataFrame(records)
# # Uncomment this code below you can save the result
# output_df.to_csv("PMDC_withShortName.csv", index=False)

print("Saved to 'PMDC_withShortName.csv'")
