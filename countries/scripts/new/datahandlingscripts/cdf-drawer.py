import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['plt'] = pd.to_numeric(df['plt'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('../../../data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('../../../data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('../../../data/processed/compiled_country_avif_hi.csv')

org_li = process_file('../../../data/processed/compiled_country_org_li.csv')
webp_li = process_file('../../../data/processed/compiled_country_webp_li.csv')
avif_li = process_file('../../../data/processed/compiled_country_avif_li.csv')

# Calculate delta values
delta_values_webp_hi = org_hi['plt'] - webp_hi['plt']
delta_values_avif_hi = org_hi['plt'] - avif_hi['plt']
delta_values_webp_li = org_li['plt'] - webp_li['plt']
delta_values_avif_li = org_li['plt'] - avif_li['plt']

# Function to remove outliers
def remove_outliers(values):
    Q1 = values.quantile(0.25)
    Q3 = values.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_values = values[(values >= lower_bound) & (values <= upper_bound)]
    return filtered_values

# Remove outliers
filtered_delta_values_webp_hi = remove_outliers(delta_values_webp_hi)
filtered_delta_values_avif_hi = remove_outliers(delta_values_avif_hi)
filtered_delta_values_webp_li = remove_outliers(delta_values_webp_li)
filtered_delta_values_avif_li = remove_outliers(delta_values_avif_li)

# Prepare the data for CDF
sorted_data_webp_hi = np.sort(filtered_delta_values_webp_hi)
sorted_data_avif_hi = np.sort(filtered_delta_values_avif_hi)
sorted_data_webp_li = np.sort(filtered_delta_values_webp_li)
sorted_data_avif_li = np.sort(filtered_delta_values_avif_li)

y_values_webp_hi = np.arange(1, len(sorted_data_webp_hi) + 1) / len(sorted_data_webp_hi)
y_values_avif_hi = np.arange(1, len(sorted_data_avif_hi) + 1) / len(sorted_data_avif_hi)
y_values_webp_li = np.arange(1, len(sorted_data_webp_li) + 1) / len(sorted_data_webp_li)
y_values_avif_li = np.arange(1, len(sorted_data_avif_li) + 1) / len(sorted_data_avif_li)


# Aesthetic configurations
plot.rc('xtick', labelsize=12)
plot.rc('ytick', labelsize=12)
plot.rcParams['pdf.fonttype'] = 42
plot.rcParams['ps.fonttype'] = 42

# Plot the CDFs
fig, ax = plot.subplots(figsize=(8, 6))
ax.plot(sorted_data_webp_hi, y_values_webp_hi, marker='o', linestyle='-', markersize=1, alpha=0.8, color='tab:orange', label='Delta values (plt) WEBP - High Income')
ax.plot(sorted_data_avif_hi, y_values_avif_hi, marker='o', linestyle='-', markersize=1, alpha=0.8, color='tab:green', label='Delta values (plt) AVIF - High Income')
ax.plot(sorted_data_webp_li, y_values_webp_li, marker='o', linestyle='-', markersize=1, alpha=0.8, color='tab:red', label='Delta values (plt) WEBP - Low Income')
ax.plot(sorted_data_avif_li, y_values_avif_li, marker='o', linestyle='-', markersize=1, alpha=0.8, color='tab:blue', label='Delta values (plt) AVIF - Low Income')


ax.set_xlabel('Delta Values for Page Load Time (Seconds)', fontsize=12)
ax.set_ylabel('Cumulative Probability', fontsize=12)
ax.legend(loc='upper left', fontsize=12)
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# x_ticks = np.arange(-1200, 2000, step=100)  # Adjust the step value to change the divisions
# ax.set_xticks(x_ticks)
# ax.set_xticklabels(ax.get_xticks(), rotation='vertical')

# y_ticks = np.arange(0, 1, step=0.1)  # Adjust the step value to change the divisions
# ax.set_yticks(y_ticks)


plot.tight_layout()

plot.savefig('cdf_delta_plt.pdf', bbox_inches='tight')
plot.show()
