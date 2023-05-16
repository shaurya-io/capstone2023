import pandas as pd
import matplotlib.pyplot as plot
import numpy as np

# Load data_with_buckets.csv
data_df = pd.read_csv("../../data/data_with_buckets.csv")

# Convert all columns except 'URL', 'domain', and 'bucket' to numerical values, treating '-' as NaN
numerical_columns = data_df.columns.difference(['URL', 'domain', 'bucket'])
data_df[numerical_columns] = data_df[numerical_columns].apply(pd.to_numeric, errors='coerce')

# Categorize the rows by the value in the 'buckets' column
grouped_data = data_df.groupby('bucket', sort=False)

# Initialize the data for the plot
buckets = []
avif_avg_pagesize = []
webp_avg_pagesize = []
org_avg_pagesize = []

# Calculate the average 'pagesize' value for each EXP_TYPE within each bucket
for bucket, group in grouped_data:
    avif_rows = group[group['URL'].str.contains('EXP_TYPE=AVIF')]
    webp_rows = group[group['URL'].str.contains('EXP_TYPE=WEBP')]
    org_rows = group[group['URL'].str.contains('EXP_TYPE=ORG')]

    avif_avg = avif_rows['pagesize'].mean()
    webp_avg = webp_rows['pagesize'].mean()
    org_avg = org_rows['pagesize'].mean()

    buckets.append(bucket)
    avif_avg_pagesize.append(avif_avg)
    webp_avg_pagesize.append(webp_avg)
    org_avg_pagesize.append(org_avg)

# Bucket order mapping
bucket_order = {
    '1-100': 1,
    '101-300': 2,
    '301-700': 3,
    '701-1500': 4,
    '1501-3100': 5,
    '3101-6300': 6,
    '6301-12700': 7,
    '12701-25500': 8,
    '25501-51100': 9,
    '51101-102300': 10,
    '102301-204700': 11,
    '204701-409500': 12,
    '409501-819100': 13,
    '819101-999999': 14
}

# Sort the data by the specific bucket order
sorted_data = sorted(zip(buckets, org_avg_pagesize, webp_avg_pagesize, avif_avg_pagesize),
                     key=lambda x: bucket_order[x[0]])

# Unzip the sorted data
buckets, org_avg_pagesize, webp_avg_pagesize, avif_avg_pagesize = zip(*sorted_data)


new_labels = ['Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Set 6', 'Set 7', 'Set 8', 'Set 9', 'Set 10', 'Set 11', 'Set 12', 'Set 13', 'Set 14'] 



# Prepare the multi-bar chart
x = np.arange(len(buckets))
width = 0.2

fig, ax = plot.subplots(figsize=(14,6))
rects1 = ax.bar(x - width, org_avg_pagesize, width, label='org', color='tab:blue')
rects2 = ax.bar(x, webp_avg_pagesize, width, label='webp', color='tab:orange')
rects3 = ax.bar(x + width, avif_avg_pagesize, width, label='avif', color='tab:green')


# Configure the plot
ax.set_ylabel('Average Page Size (Kilobytes)', fontsize=12)
ax.set_title('Average Page Size by image format and domain ranking', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(new_labels, fontsize=12)
ax.legend(fontsize=12, loc='upper left')
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
# Hardcode the y-axis range and step
y_min, y_max = 0, 4000  # Set the y-axis range
y_step = 500 # Set the y-axis step
ax.set_ylim(y_min, y_max)
ax.set_yticks(np.arange(y_min, y_max + y_step, y_step))


fig.tight_layout()
plot.savefig('pagesize_by_popularity.pdf', bbox_inches='tight')
# Show the plot
plot.show()
