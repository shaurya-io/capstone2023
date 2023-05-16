import pandas as pd
import seaborn as sns
import matplotlib.pyplot as domC

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['domC'] = pd.to_numeric(df['domC'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('data/processed/compiled_country_avif_hi.csv')

org_li = process_file('data/processed/compiled_country_org_li.csv')
webp_li = process_file('data/processed/compiled_country_webp_li.csv')
avif_li = process_file('data/processed/compiled_country_avif_li.csv')

# Sort org_hi and org_li by 'domC' in ascending order and get the sorted index
sorted_index_hi = org_hi['pagesize'].sort_values().index
sorted_index_li = org_li['pagesize'].sort_values().index

# Reorder all DataFrames based on the sorted index
org_hi = org_hi.loc[sorted_index_hi]
webp_hi = webp_hi.loc[sorted_index_hi]
avif_hi = avif_hi.loc[sorted_index_hi]

org_li = org_li.loc[sorted_index_li]
webp_li = webp_li.loc[sorted_index_li]
avif_li = avif_li.loc[sorted_index_li]

# Calculate percentage gains in page load time
webp_hi['gain'] = (org_hi['domC'] - webp_hi['domC']) / org_hi['domC'] * 100
avif_hi['gain'] = (org_hi['domC'] - avif_hi['domC']) / org_hi['domC'] * 100

webp_li['gain'] = (org_li['domC'] - webp_li['domC']) / org_li['domC'] * 100
avif_li['gain'] = (org_li['domC'] - avif_li['domC']) / org_li['domC'] * 100

# Function to create line charts for the percentage gains
def create_line_chart(ax, data_webp, data_avif, title, ylabel):
    ax.plot(data_webp['gain'].values, label='WebP')
    ax.plot(data_avif['gain'].values, label='AVIF')

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Websites arranged in ascending order by Original Page Size')
    ax.legend()

# Create a single figure with multiple subplots
fig, axes = domC.subplots(2, 1, figsize=(18, 10), sharex=True, sharey=True)

# Create line charts for the percentage gains
create_line_chart(axes[0], webp_hi, avif_hi, 'Percentage Gains in DocComplete Time (High Income)', 'Percentage Gains')
create_line_chart(axes[1], webp_li, avif_li, 'Percentage Gains in DocComplete Time (Low Income)', 'Percentage Gains')

axes[0].set_ylim(-100, 100)
axes[1].set_ylim(-100, 100)

domC.tight_layout()
domC.show()
