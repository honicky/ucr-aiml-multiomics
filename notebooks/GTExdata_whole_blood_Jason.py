import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import timeit

# read 10 genes first 
n_genes = 56200# 56202
tpm = pd.read_csv("tpm.gct", sep='\t', skiprows=2)
tpm.head(5)

# log2 transform the data
tpm_log2 = np.log2(tpm.iloc[:, 2:] + 1)  # Adding 1 to avoid log(0) errors
tpm_log2.index = tpm["Name"].values
tpm_log2.head(3)

# meta data
metadata = pd.read_csv("metadata.txt",sep="\t")
metadata.head(5)
wholeblood = metadata[metadata['SMTSD'] == 'Whole Blood'] # can change to ther tissue type
wholeblood.head(5)


## combine tpm with metatdata to select blood sample
# Replace '.' with '-' in dat column names from the 3rd column onward
tpm_log2.columns = list(tpm_log2.columns[:2]) + [col.replace('.', '-') for col in tpm_log2.columns[2:]]

# Extract sample IDs
sampids = wholeblood['SAMPID'].tolist()

# Identify sample IDs that are in dat's column names
sampids_in_tpm = [sampid for sampid in sampids if sampid in tpm_log2.columns]

# Select those columns from dat and add back the first two columns
matched_dat = tpm_log2[sampids_in_tpm]

# combine with age and sex
age_sex = pd.read_csv("metadata2.txt", sep="\t")[["SUBJID", "SEX", "AGE"]]
age_sex.head(5)

# Create a mapping dictionary for age ranges to midpoints using what RJ did
age_to_midpoint = {
    '20-29': 25,
    '30-39': 35,
    '40-49': 45,
    '50-59': 55,
    '60-69': 65,
    '70-79': 75
}
# Map the age ranges to midpoints
age_sex['AGE_midpoint'] = age_sex['AGE'].map(age_to_midpoint)
age_sex.drop(columns=["AGE"], inplace=True)
age_sex.head(5)


# Extract SUBJID from SAMPID
matched_dat= matched_dat.transpose()
matched_dat['SUBJID'] = matched_dat.index.map(lambda x: '-'.join(x.split('-')[:2]))

# Merge with age_sex dataframe on SUBJID
combined_all = pd.merge(matched_dat, age_sex, on='SUBJID', how='left')
combined_all.index = matched_dat.index
combined_all


# run the regression analysis


# Columns to exclude from regression
metadata_cols = ['SUBJID', 'SEX', 'AGE_midpoint']
gene_cols = list(combined_all.columns[:n_genes])

# convert SEX to categorical
combined_all['SEX'] = combined_all['SEX'].astype('category')



## regression for all the genes
# Start timing
start_time = timeit.default_timer()
results = []

for gene in gene_cols:
    print(gene)
    formula = f'Q("{gene}")' +"~ AGE_midpoint + SEX + AGE_midpoint:SEX"
    model = smf.ols(formula, data=combined_all).fit()
    # Extract coefficients, p-values, R²
    result = {
        'Gene': gene,
        'R_squared': model.rsquared,
        'p_AGE': model.pvalues.get('AGE_midpoint', None),
        'p_SEX': model.pvalues.get('SEX[T.2.0]', None),  # depends on category levels
        'p_Interaction': model.pvalues.get('AGE_midpoint:SEX[T.2.0]', None)
    }
    results.append(result)

# Create result dataframe
results_df = pd.DataFrame(results)

# End timing
end_time = timeit.default_timer()

print(f"Training completed in {end_time - start_time:.2f} seconds")

results_df["Description"] = tpm["Description"].values

results_df.to_csv("gene_regression_results.csv", index=False)


pval_summary = results_df[['p_AGE', 'p_SEX', 'p_Interaction']].describe()


from statsmodels.stats.multitest import multipletests

# Copy results_df to avoid modifying original
fdr_df = results_df.copy()

# Apply FDR correction (Benjamini-Hochberg) to each p-value set
for col in ['p_AGE', 'p_SEX', 'p_Interaction']:
    mask = fdr_df[col].notna()  # Only apply to valid p-values
    _, qvals, _, _ = multipletests(fdr_df.loc[mask, col], method='fdr_bh')
    fdr_df.loc[mask, f'q_{col.split("_")[1]}'] = qvals  # e.g., q_AGE


sig_AGE = fdr_df[fdr_df['q_AGE'] < 0.05]
sig_SEX = fdr_df[fdr_df['q_SEX'] < 0.05]
sig_INTERACTION = fdr_df[fdr_df['q_Interaction'] < 0.05]

# Add counts
print(f"Significant genes (q < 0.05):")
print(f"  AGE effect: {len(sig_AGE)} genes")
print(f"  SEX effect: {len(sig_SEX)} genes")
print(f"  AGE × SEX effect: {len(sig_INTERACTION)} genes")

results_df.to_csv("gene_regression_results_qvalue.csv", index=False)

# interaction plot
import seaborn as sns
gene_inter = combined_all[["ENSG00000176728.7","SEX", "AGE_midpoint"]]
plt.figure(figsize=(3, 3))
sns.lmplot(
    data=gene_inter,
    x="AGE_midpoint",
    y="ENSG00000176728.7",
    hue="SEX",
    ci=None,
    aspect=1.5,
    height=6
)
plt.title("Interaction between AGE and SEX on TTTY14")
plt.xlabel("Age")
plt.ylabel("Gene Expression (TTTY14)")
plt.tight_layout()
plt.show()