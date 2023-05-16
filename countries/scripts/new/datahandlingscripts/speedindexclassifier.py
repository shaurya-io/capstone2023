import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['lh_si'] = pd.to_numeric(df['lh_si'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('../../../data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('../../../data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('../../../data/processed/compiled_country_avif_hi.csv')

# Function to categorize the data
def categorize_lh_si(df):
    categories = pd.cut(df['lh_si'], bins=[0, 3.4, 5.8, float('inf')],
                        labels=['Fast', 'Moderate', 'Slow'])
    df['category'] = categories
    return df

org_hi = categorize_lh_si(org_hi)
webp_hi = categorize_lh_si(webp_hi)
avif_hi = categorize_lh_si(avif_hi)
print(avif_hi)

# Calculate the percentage of each category for each file
org_counts = org_hi['category'].value_counts(normalize=True) * 100
print(org_counts)
webp_counts = webp_hi['category'].value_counts(normalize=True) * 100
print(webp_counts)
avif_counts = avif_hi['category'].value_counts(normalize=True) * 100
print(avif_counts)

# Create a grouped bar chart
categories = ['Slow', 'Moderate', 'Fast']
x_labels = np.arange(len(categories))
bar_width = 0.25

fig, ax = plt.subplots(figsize=(8, 6))

ax.bar(x_labels - bar_width, org_counts, width=bar_width, color='tab:blue', alpha=0.8, label='org')
ax.bar(x_labels, webp_counts, width=bar_width, color='tab:orange', alpha=0.8, label='webp')
ax.bar(x_labels + bar_width, avif_counts, width=bar_width, color='tab:green', alpha=0.8, label='avif')

# Set the title and labels
ax.set_title('Percentage of Slow, Moderate and Fast Speed Indices for High-Income Countries', fontsize=12)
ax.set_xlabel('Speed Index Categories', fontsize=12)
ax.set_ylabel('Percentage', fontsize=12)

# Customize tick labels and grid
ax.set_xticks(x_labels)
ax.set_xticklabels(categories)
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5, axis='y')

# Add a legend to the chart
ax.legend(loc='best', fontsize=12)
plt.tight_layout(pad=2)

plt.savefig('high-income.pdf')
plt.show()

