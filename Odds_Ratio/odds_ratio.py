# Odds Ratio and Group Label. Note: This artifact does not include data from Company X
# The file "vulCheck_v31_Cleaned_withShortName.csv" used in this script
# removed CVE descriptions that contain "UNSUPPORTED WHEN ASSIGNED" from the original full dataset
# and manually annotate short names for each CNA.

import pandas as pd
from tqdm import tqdm

# === Load and Preprocess ===
file_path = "../Original Dataset/vulCheck_v31_Cleaned_withShortName.csv"
df = pd.read_csv(file_path)
df["Description_en"] = df["Description_en"].astype(str).str.strip().str.lower()

# === Filter Description groups with ≥ 4 entries ===
grouped = df.groupby("Description_en")
desc_filtered = grouped.filter(lambda x: len(x) >= 4)

# === Keep only groups where NVD and at least one CNA ShortName have ≥ 2 entries ===
valid_groups = []

for desc, group in desc_filtered.groupby("Description_en"):
    shortname_counts = group["ShortName"].value_counts()

    # NVD must have at least 2 entries
    if shortname_counts.get("NVD", 0) < 2:
        continue

    # At least one CNA (non-NVD) must also have ≥ 2 entries
    cna_counts = shortname_counts[shortname_counts.index != "NVD"]
    if len(cna_counts) == 0:
        continue
    if any(cna_counts >= 2):
        valid_groups.append(group)

    # === Combine valid groups into a single dataframe ===
result_df = pd.concat(valid_groups, ignore_index=True)

# === Use result_df directly ===
df = result_df.copy()
df["Group_Label"] = ""

# === Extract CNA list (excluding NVD) from ShortName ===
all_sources = df["ShortName"].dropna().unique().tolist()
cna_list = [c for c in all_sources if c != "NVD"]

# === Group by Description ===
grouped = df.groupby("Description_en")

# === Initialize result containers ===
results = []
group_counters = {cna: 1 for cna in cna_list}

# === Label assignment and odds ratio computation ===
for cna in tqdm(cna_list, desc="Labeling per CNA"):
    G_C_CNA = G_I_CNA = G_C_NVD = G_I_NVD = 0

    for desc, group in grouped:
        cna_group = group[group["ShortName"] == cna]
        nvd_group = group[group["ShortName"] == "NVD"]

        if len(cna_group) < 2 or len(nvd_group) < 2:
            continue

        # Check consistency
        cna_vectors = cna_group["CVSS_Vector_v31"].dropna().unique()
        nvd_vectors = nvd_group["CVSS_Vector_v31"].dropna().unique()

        is_cna_consistent = len(cna_vectors) == 1
        is_nvd_consistent = len(nvd_vectors) == 1

        # Assign group label
        gid = group_counters[cna]
        cna_label = f"{'G_C' if is_cna_consistent else 'G_I'}_CNA_{cna}_Group{gid}"
        nvd_label = f"{'G_C' if is_nvd_consistent else 'G_I'}_NVD_{cna}_Group{gid}"

        # Update labels in df
        for idx in cna_group.index:
            df.at[idx, "Group_Label"] = (
                df.at[idx, "Group_Label"] + ";" + cna_label
                if df.at[idx, "Group_Label"] else cna_label
            )
        for idx in nvd_group.index:
            df.at[idx, "Group_Label"] = (
                df.at[idx, "Group_Label"] + ";" + nvd_label
                if df.at[idx, "Group_Label"] else nvd_label
            )

        # Count group types
        G_C_CNA += int(is_cna_consistent)
        G_I_CNA += int(not is_cna_consistent)
        G_C_NVD += int(is_nvd_consistent)
        G_I_NVD += int(not is_nvd_consistent)

        group_counters[cna] += 1

    # Compute odds ratio
    odds_cna = G_I_CNA / G_C_CNA if G_C_CNA else (float("inf") if G_I_CNA > 0 else 0.0)
    odds_nvd = G_I_NVD / G_C_NVD if G_C_NVD else (float("inf") if G_I_NVD > 0 else 0.0)
    OR = odds_cna / odds_nvd if odds_nvd else (float("inf") if odds_cna > 0 else 0.0)

    results.append({
        "ShortName": cna,
        "G_I_CNA": G_I_CNA,
        "G_C_CNA": G_C_CNA,
        "G_I_NVD": G_I_NVD,
        "G_C_NVD": G_C_NVD,
        "Odds_Ratio": round(OR, 4)
    })

# #=== Save outputs ===
# # Uncomment this code below you can save the result
# df.to_csv("group_labels_withShortName.csv", index=False)
# pd.DataFrame(results).to_csv("odds_ratio_withShortName.csv", index=False)
#
print("Saved to 'group_labels_withShortName.csv'")
print("Saved to 'odds_ratio_withShortName.csv'")
