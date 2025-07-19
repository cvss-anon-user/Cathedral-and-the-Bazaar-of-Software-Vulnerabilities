# Cathedral-and-the-Bazaar-of-Software-Vulnerabilities

This repository provides the datasets used in our paper for analyzing entry-level and group-level inconsistencies between CNAs and the NVD.  
**Note**: The private CNA dataset (referred to as *Company X*) used in our experiments and analysis is not included in this repository. The script below uses only public CNA data obtained from VulnCheck.

# Usage
Environment Python 3.10.9

# Folder Contents

## Original Dataset

As the files `vulCheck_v31.csv`, `vulCheck_v31_Cleaned.csv`, and `vulCheck_v31_Cleaned_withShortName.csv` are large in size, we have uploaded each of them as a separate zip archive.  
Please follow the instructions below to properly extract and use the full dataset and code.

- **Step 1**: Download all three zipped CSV files.  
- **Step 2**: Unzip the files and place them in the folder named `Original Dataset`.

Please note:
- The file `vulCheck_v31_Cleaned.csv` was generated using our preprocessing script `vulCheck_DataPreprocessing.py`. You can also regenerate it by uncommenting the save file instruction in the script.
- The file `vulCheck_v31_Cleaned_withShortName.csv` was created based on `vulCheck_v31_Cleaned.csv` by manually reviewing and annotating short names for each CNA.

## d Disagreement Metric

This module computes the overall disagreement between CNA and NVD CVSS vector assignments using the Hamming distance.  
It includes:
- `hamming_distance.py`: Computes Hamming distance for each CVE between CNA and NVD.
- `Hamming_Distance_AllCNA.csv`: The full output of Hamming distance results. You can regenerate it by uncommenting the save file instruction in `hamming_distance.py`.
- `Median_d_withShortName.csv`: Median disagreement score per CNA for visualization. You can regenerate it by uncommenting the save file instruction in `hamming_distance.py`.

### Per-Metric Disagreement Coefficient (PMDC)

This module quantifies how often each CVSS base metric (e.g., AV, AC, PR) differs between CNA and NVD.  
It includes:
- `PMDC.py`: Computes metric-level disagreement rates.
- `PMDC_withShortName.csv`: The output file containing per-metric disagreement coefficients per CNA. You can regenerate it by uncommenting the save file instruction in `hamming_distance.py`.

## Odds Ratio

## Entropy

## Regression Analysis
