import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to remove outliers based on IQR method
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Define your directories
merged_raw_folder = '../data/merged_raw'
avif_files_folder = '../data/avif_files'
webp_files_folder = '../data/webp_files'

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

# Calculate delta values
df['delta_webp'] = df['orgsize'] - df['webpsize']
df['delta_avif'] = df['orgsize'] - df['avifsize']

# Remove outliers
df = remove_outliers(df, 'delta_webp')
df = remove_outliers(df, 'delta_avif')

# Calculate the cumulative distribution for WebP and AVIF deltas
sorted_webp_delta = np.sort(df['delta_webp'])
y_values_webp = np.arange(len(sorted_webp_delta)) / float(len(sorted_webp_delta))
sorted_avif_delta = np.sort(df['delta_avif'])
y_values_avif = np.arange(len(sorted_avif_delta)) / float(len(sorted_avif_delta))

# Plot the CDFs
fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(sorted_webp_delta, y_values_webp, linestyle='-', color='tab:orange', label='Delta values (filesize) WEBP')
ax.plot(sorted_avif_delta, y_values_avif, linestyle='-', color='tab:green', label='Delta values (filesize) AVIF')

ax.set_xlabel('Delta Values for File Size (Kilobytes)', fontsize=12)
ax.set_ylabel('Cumulative Probability', fontsize=12)
ax.legend(loc='best', fontsize=12)

# Add a grid
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

plt.tight_layout(pad=0.1)
plt.savefig('(webp-avif vs jpg) delta-cdf-analysis.pdf')
plt.show()