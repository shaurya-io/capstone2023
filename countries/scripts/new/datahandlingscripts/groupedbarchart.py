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
    # [includes outliers] return df[df['URL'].isin(url_list)]['pagesize'].mean()
    # [excludes outliers using the interquartile range to calculate mean]

    filtered_df = df[df['URL'].isin(url_list)]
    Q1 = filtered_df['pagesize'].quantile(0.25) #this line determines which variable is plotted
    Q3 = filtered_df['pagesize'].quantile(0.75) #this line determines which variable is plotted
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    no_outliers_df = filtered_df[(filtered_df['pagesize'] >= lower_bound) & (filtered_df['pagesize'] <= upper_bound)]

    return no_outliers_df['pagesize'].mean() #this line and the one above it determines which variable is plotted


org_hi = categorize_pagesize(org_hi)
org_li = categorize_pagesize(org_li)

categories = ['0-381', '382-913', '914-1993', '1994-4062', '4063-8195', '>8195']
# Define the new labels
new_labels = ['p(0-10)', 'p(11-25)', 'p(26-50)', 'p(51-75)', 'p(76-90)', 'p(91-100)']

x_labels = np.arange(len(categories))
bar_width = 0.25

# Aesthetic configurations
plot.rc('xtick', labelsize=12)
plot.rc('ytick', labelsize=12)
plot.rcParams['pdf.fonttype'] = 42
plot.rcParams['ps.fonttype'] = 42

fig, axes = plot.subplots(1, 2, figsize=(14, 6), sharey=True)

for i, group in enumerate(['High Income', 'Low Income']):
    org_df = org_hi if group == 'High Income' else org_li
    webp_df = webp_hi if group == 'High Income' else webp_li
    avif_df = avif_hi if group == 'High Income' else avif_li

    org_avgs, webp_avgs, avif_avgs = [], [], []

    for category in categories:
        url_list = org_df[org_df['category'] == category]['URL'].tolist()
        org_avgs.append(calculate_avg_pagesize(org_df, url_list))
        webp_avgs.append(calculate_avg_pagesize(webp_df, url_list))
        avif_avgs.append(calculate_avg_pagesize(avif_df, url_list))

    axes[i].bar(x_labels - bar_width, org_avgs, width=bar_width, color='tab:blue', alpha=0.8, label='org')
    axes[i].bar(x_labels, webp_avgs, width=bar_width, color='tab:orange', alpha=0.8, label='webp')
    axes[i].bar(x_labels + bar_width, avif_avgs, width=bar_width, color='tab:green', alpha=0.8, label='avif')

    axes[i].set_title(group)
    axes[i].set_xticks(x_labels)
    axes[i].set_xticklabels(new_labels)
    axes[i].set_xlabel('Categories by Page Size', fontsize=12)
    axes[i].set_ylabel('Average Page Size (Kilobytes)', fontsize=12)
    # axes[i].set_yscale('log') #checking logarithmic scale
    axes[i].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# Add a legend to the chart
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=3, fontsize=12)

plot.tight_layout(pad=2)
plot.savefig('pagesize savings by buckets.pdf')
plot.show()

