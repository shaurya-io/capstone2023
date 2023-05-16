import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def delete_rows_with_zero_orgsize(df):
    return df[df['orgsize'] > 0.75]

# Function to remove outliers based on IQR method
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Replace '../your/folder' with the path to your folders
merged_raw_folder = '../merged_raw'
avif_files_folder = '../avif_files'
webp_files_folder = '../webp_files'

# Initialize the dataframe
data = {'name': [], 'orgsize': [], 'avifsize': [], 'webpsize': []}
df = pd.DataFrame(data)

# Read image files from merged_raw folder
for file_name in os.listdir(merged_raw_folder):
    if file_name.endswith(('.jpg', '.jpeg', '.png')): 
        file_path = os.path.join(merged_raw_folder, file_name)
        file_size_kb = os.path.getsize(file_path) / 1024
        df = df.append({'name': file_name, 'orgsize': file_size_kb}, ignore_index=True)

# Add AVIF and WebP file sizes to the dataframe
for index, row in df.iterrows():
    avif_name = os.path.splitext(row['name'])[0] + '.avif'
    avif_path = os.path.join(avif_files_folder, avif_name)
    webp_name = os.path.splitext(row['name'])[0] + '.webp'
    webp_path = os.path.join(webp_files_folder, webp_name)

    if os.path.isfile(avif_path):
        avif_size_kb = os.path.getsize(avif_path) / 1024
        df.at[index, 'avifsize'] = avif_size_kb

    if os.path.isfile(webp_path):
        webp_size_kb = os.path.getsize(webp_path) / 1024
        df.at[index, 'webpsize'] = webp_size_kb

# Reorder the dataframe in increasing order based on the orgsize column
df.sort_values(by='orgsize', inplace=True)
df.reset_index(drop=True, inplace=True)

# Calculate the percentage difference between orgsize and avifsize, as well as orgsize and webpsize for each row
df['avif_pct_diff'] = (df['orgsize'] - df['avifsize']) / df['orgsize'] * 100
df['webp_pct_diff'] = (df['orgsize'] - df['webpsize']) / df['orgsize'] * 100

df1 = remove_outliers(df, 'avif_pct_diff')
df2 = delete_rows_with_zero_orgsize(df1)
df_no_outliers = remove_outliers(df2, 'orgsize')


# Calculate the average percentage difference for both avif and webp for every 10% of the images
num_groups = 10
group_size = len(df_no_outliers) // num_groups
avif_pct_diff_means = []
webp_pct_diff_means = []

for i in range(num_groups):
    start_idx = i * group_size
    end_idx = (i + 1) * group_size if i < num_groups - 1 else len(df_no_outliers)
    avif_pct_diff_means.append(df_no_outliers['avif_pct_diff'][start_idx:end_idx].mean())
    webp_pct_diff_means.append(df_no_outliers['webp_pct_diff'][start_idx:end_idx].mean())
    print(df_no_outliers['orgsize'][start_idx:end_idx].mean())

# Plot this information on a multiple bar chart
x = np.arange(num_groups)
bar_width = 0.35

fig, ax = plt.subplots()

bar1 = ax.bar(x - bar_width / 2, webp_pct_diff_means, bar_width, label='WebP', color='tab:orange')
bar2 = ax.bar(x + bar_width / 2, avif_pct_diff_means, bar_width, label='AVIF', color='tab:green')


ax.set_xlabel('Percentile Groups')
ax.set_ylabel('Average Percentage Difference')
ax.set_title('Average Percentage Difference in Image Size (Overall)')
ax.set_xticks(x)
ax.set_xticklabels([f'{i*10}-{(i+1)*10}%' for i in range(num_groups)], fontsize=8)

ax.legend()

fig.tight_layout()
plt.savefig('(webp-avif vs jpg) image-decile-analysis.pdf', bbox_inches='tight')
plt.show()
