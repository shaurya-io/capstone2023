import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['plt'] = pd.to_numeric(df['plt'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('data/processed/compiled_country_avif_hi.csv')

org_li = process_file('data/processed/compiled_country_org_li.csv')
webp_li = process_file('data/processed/compiled_country_webp_li.csv')
avif_li = process_file('data/processed/compiled_country_avif_li.csv')

# Sort org_hi and org_li by 'plt' in ascending order and get the sorted index
sorted_index_hi = org_hi['pagesize'].sort_values().index
sorted_index_li = org_li['pagesize'].sort_values().index

# Reorder all DataFrames based on the sorted index
org_hi = org_hi.loc[sorted_index_hi]
webp_hi = webp_hi.loc[sorted_index_hi]
avif_hi = avif_hi.loc[sorted_index_hi]

org_li = org_li.loc[sorted_index_li]
webp_li = webp_li.loc[sorted_index_li]
avif_li = avif_li.loc[sorted_index_li]

# Function to create line charts for the 'plt' variable
def create_line_chart(ax, data_org, data_webp, data_avif, title, ylabel):
    ax.plot(data_org['plt'].values, label='Original')
    ax.plot(data_webp['plt'].values, label='WebP')
    ax.plot(data_avif['plt'].values, label='AVIF')

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Websites arranged in ascending order by Page Size')
    ax.legend()

# Create a single figure with multiple subplots
fig, axes = plt.subplots(2, 1, figsize=(18, 10), sharex=True)

# Create line charts for the 'plt' variable
create_line_chart(axes[0], org_hi, webp_hi, avif_hi, 'Page Load Time (High Income)', 'Page Load Time (seconds)')
create_line_chart(axes[1], org_li, webp_li, avif_li, 'Page Load Time (Low Income)', 'Page Load Time (seconds)')

plt.tight_layout()
plt.show()
