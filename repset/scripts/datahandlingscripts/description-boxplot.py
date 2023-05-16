import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Aesthetic configurations
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df[['plt', 'lh_si', 'pagesize', 'numreq', 'fcp', 'domC']] = df[['plt', 'lh_si', 'pagesize', 'numreq', 'fcp', 'domC']].apply(pd.to_numeric, errors='coerce')
    return df

# Read and process the CSV file
data = process_file('../../data/data.csv')

# Group data by experiment type
org_data = data[data['URL'].str.contains("EXP_TYPE=ORG")]
webp_data = data[data['URL'].str.contains("EXP_TYPE=WEBP")]
avif_data = data[data['URL'].str.contains("EXP_TYPE=AVIF")]

# Prepare data for seaborn
data_seaborn = pd.concat([org_data['plt'], webp_data['plt'], avif_data['plt']], axis=1)
data_seaborn.columns = ['Original', 'WebP', 'AVIF']

# Create the box plot
plt.figure(figsize=(8, 6))
box_plot = sns.boxplot(data=data_seaborn, orient='v', showfliers=False)
box_plot.set_title('Page Load Time Comparison (Representative Set)', fontsize=12)
box_plot.set_ylabel('Page Load Time (Seconds)', fontsize=12)

# Add median value annotations
# for i in range(3):
#     median = data_seaborn.iloc[:, i].median()
#     plt.text(i, median, f'Median: {median:.2f}', ha='center', va='bottom', fontsize=12)

# Add mean value annotations
for i in range(3):
    mean = data_seaborn.iloc[:, i].mean()
    plt.scatter(i, mean, color='red', s=30, zorder=3)
    # plt.text(i, mean, f'{mean:.2f}', ha='center', va='top', fontsize=12, color='r')
    plt.annotate(f'{mean:.2f}', xy=(i + 0.1, mean), xycoords='data', fontsize=11,
                    ha='left', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=1))

y_ticks = np.arange(0, 45, step=5)
plt.yticks(y_ticks)

plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.savefig('plt_desc_repset.pdf')
plt.show()

