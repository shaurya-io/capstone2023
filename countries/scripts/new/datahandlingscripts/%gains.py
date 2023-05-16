import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['pagesize'] = pd.to_numeric(df['pagesize'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('../../../data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('../../../data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('../../../data/processed/compiled_country_avif_hi.csv')
org_li = process_file('../../../data/processed/compiled_country_org_li.csv')
webp_li = process_file('../../../data/processed/compiled_country_webp_li.csv')
avif_li = process_file('../../../data/processed/compiled_country_avif_li.csv')

# Function to categorize the data
def categorize_pagesize(df):
    categories = pd.cut(df['pagesize'], bins=[0, 381, 913, 1993, 4062, 8195, float('inf')],
                        labels=['0-381', '382-913', '914-1993', '1994-4062', '4063-8195', '>8195'])
    df['category'] = categories
    return df

def calculate_avg_pagesize(df, url_list):
    filtered_df = df[df['URL'].isin(url_list)]
    Q1 = filtered_df['pagesize'].quantile(0.25)
    Q3 = filtered_df['pagesize'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    no_outliers_df = filtered_df[(filtered_df['pagesize'] >= lower_bound) & (filtered_df['pagesize'] <= upper_bound)]

    return no_outliers_df['pagesize'].mean()

org_hi = categorize_pagesize(org_hi)
org_li = categorize_pagesize(org_li)

categories = ['0-381', '382-913', '914-1993', '1994-4062', '4063-8195', '>8195']
# Define the new labels
new_labels = ['p(0-10)', 'p(11-25)', 'p(26-50)', 'p(51-75)', 'p(76-90)', 'p(91-100)']
x_labels = np.arange(len(categories))
bar_width = 0.25

def calculate_percentage_gain(org_df, new_format_df, url_list):
    org_mean = calculate_avg_pagesize(org_df, url_list)
    new_format_mean = calculate_avg_pagesize(new_format_df, url_list)
    percentage_gain = ((org_mean - new_format_mean) / org_mean) * 100
    return percentage_gain

fig, axes = plot.subplots(1, 2, figsize=(14, 6), sharey=True)

for i, group in enumerate(['High Income', 'Low Income']):
    org_df = org_hi if group == 'High Income' else org_li
    webp_df = webp_hi if group == 'High Income' else webp_li
    avif_df = avif_hi if group == 'High Income' else avif_li

    webp_gains, avif_gains = [], []

    for category in categories:
        url_list = org_df[org_df['category'] == category]['URL'].tolist()
        webp_gains.append(calculate_percentage_gain(org_df, webp_df, url_list))
        avif_gains.append(calculate_percentage_gain(org_df, avif_df, url_list))

    axes[i].bar(x_labels - bar_width / 2, webp_gains, width=bar_width, color='tab:orange', alpha=0.8, label='webp')
    axes[i].bar(x_labels + bar_width / 2, avif_gains, width=bar_width, color='tab:green', alpha=0.8, label='avif')

    axes[i].set_title(group)
    axes[i].set_xticks(x_labels)
    axes[i].set_xticklabels(new_labels)
    axes[i].set_xlabel('Categories by Page Size', fontsize=12)
    axes[i].set_ylabel('Percentage Gain in Page Size (kilobytes)', fontsize=12)
    axes[i].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# Add a legend to the chart
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=12)

plot.tight_layout(pad=2)
plot.savefig('%pagesize savings by buckets.pdf')
plot.show()
