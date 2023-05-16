import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV files into Pandas DataFrames
org_df = pd.read_csv('data/processed/country_org.csv')
webp_df = pd.read_csv('data/processed/country_webp.csv')

# Convert the 'pagesize' columns to numeric values
org_df['pagesize'] = pd.to_numeric(org_df['pagesize'], errors='coerce')
webp_df['pagesize'] = pd.to_numeric(webp_df['pagesize'], errors='coerce')

# Merge the DataFrames on the 'URL' column
merged_df = org_df.merge(webp_df, on='URL', suffixes=('_org', '_webp'))

# Calculate the difference in pagesize between the two files
merged_df['pagesize_diff'] = merged_df['pagesize_org'] - merged_df['pagesize_webp']

# Visualize the difference using a box plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=merged_df[['pagesize_diff']], ax=ax)
ax.set_title('Difference in pagesize (ORG - WEBP)')

plt.tight_layout()
plt.show()
