import pandas as pd
import matplotlib.pyplot as plt

# Aesthetic configurations
plt.rc('xtick', labelsize=8)
plt.rc('ytick', labelsize=8)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['pagesize'] = pd.to_numeric(df['pagesize'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('../../../data/processed/compiled_country_org_hi.csv')
org_li = process_file('../../../data/processed/compiled_country_org_li.csv')

# Function to categorize the data
def categorize_pagesize(df):
    categories = pd.cut(df['pagesize'], bins=[0, 381, 913, 1993, 4062, 8195, float('inf')],
                        labels=['0-381', '382-913', '914-1993', '1994-4062', '4063-8195', '>8195'])
    return categories.value_counts().sort_index()

# Categorize the data for high income and low income groups
hi_categories = categorize_pagesize(org_hi)
li_categories = categorize_pagesize(org_li)

# Create bar charts for high income and low income groups
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

hi_categories.plot(kind='bar', ax=axes[0], color='tab:blue', alpha=0.8)
axes[0].set_title('High Income')
axes[0].set_xlabel('Page Size (Kilobytes)')
axes[0].set_ylabel('Frequency')
axes[0].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

li_categories.plot(kind='bar', ax=axes[1], color='tab:blue', alpha=0.8)
axes[1].set_title('Low Income')
axes[1].set_xlabel('Page Size (Kilobytes)')
axes[1].set_ylabel('Frequency')
axes[1].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.show()
