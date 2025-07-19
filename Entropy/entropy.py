# Entropy. Note: This artifact does not include data from Company X
# The file "group_labels_withShortName.csv" used in this script
# is generated from the "../Original Dataset/odds_ratio.py"

import pandas as pd
import numpy as np
from collections import Counter
from scipy.stats import entropy

# === Load labeled data ===
file_path = "../Odds_Ratio/group_labels_withShortName.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# === Clean string fields ===
df["Group_Label"] = df["Group_Label"].astype(str).str.strip()
df["ShortName"] = df["ShortName"].astype(str).str.strip()
df["CVSS_Vector_v31"] = df["CVSS_Vector_v31"].astype(str).str.strip()

# === Drop empty Group_Label ===
df = df[df['Group_Label'].notna() & (df['Group_Label'] != '')].copy()

# === Step 1: Explode Group_Label to handle multiple labels per row ===
df["Group_Label"] = df["Group_Label"].str.split(";")
df_exploded = df.explode("Group_Label")
df_exploded = df_exploded[df_exploded["Group_Label"].notna()]

# === Step 2: Extract CNA names from Group_Label ===
cna_names = sorted(list(set(
    label.split("_CNA_")[1].split("_Group")[0]
    for label in df_exploded["Group_Label"].unique() if "_CNA_" in label
)))

# === Step 3: Compute entropy for each CNA and its associated NVD groups ===
entropy_results = []

for cna in cna_names:
    cna_prefix = f"_CNA_{cna}_Group"
    nvd_prefix = f"_NVD_{cna}_Group"

    # --- CNA Group Entropy ---
    cna_df = df_exploded[(df_exploded["ShortName"] == cna) & (df_exploded["Group_Label"].str.contains(cna_prefix))]
    cna_grouped = cna_df.groupby("Group_Label")

    entropies_cna = []
    for _, group in cna_grouped:
        vectors = group["CVSS_Vector_v31"].dropna().tolist()
        if len(vectors) > 1:
            probs = np.array(list(Counter(vectors).values())) / len(vectors)
            entropies_cna.append(entropy(probs, base=2))

    # --- NVD Group Entropy ---
    nvd_df = df_exploded[(df_exploded["ShortName"] == "NVD") & (df_exploded["Group_Label"].str.contains(nvd_prefix))]
    nvd_grouped = nvd_df.groupby("Group_Label")

    entropies_nvd = []
    for _, group in nvd_grouped:
        vectors = group["CVSS_Vector_v31"].dropna().tolist()
        if len(vectors) > 1:
            probs = np.array(list(Counter(vectors).values())) / len(vectors)
            entropies_nvd.append(entropy(probs, base=2))

    entropy_results.append({
        "ShortName": cna,
        "Num_CNA_Groups": len(entropies_cna),
        "Mean_CNA_Entropy": round(np.mean(entropies_cna), 4) if entropies_cna else 0.0,
        "Num_NVD_Groups": len(entropies_nvd),
        "Mean_NVD_Entropy": round(np.mean(entropies_nvd), 4) if entropies_nvd else 0.0,
    })

# === Step 4: Save results ===
entropy_df = pd.DataFrame(entropy_results).sort_values(by="Mean_CNA_Entropy", ascending=False)
# # Uncomment this code below you can save the result
# entropy_df.to_csv("entropy_withShortName.csv", index=False)
print("Saved to 'entropy_withShortName.csv'")