import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['pagesize'] = pd.to_numeric(df['pagesize'], errors='coerce')
    return df

# Read and process the CSV files
org_hi = process_file('data/processed/compiled_country_org_hi.csv')
webp_hi = process_file('data/processed/compiled_country_webp_hi.csv')
avif_hi = process_file('data/processed/compiled_country_avif_hi.csv')

org_li = process_file('data/processed/compiled_country_org_li.csv')
webp_li = process_file('data/processed/compiled_country_webp_li.csv')
avif_li = process_file('data/processed/compiled_country_avif_li.csv')

#print(avif_li)

# Function to create a box plot with mean and quartiles
def create_box_plot(ax, data, title, ylabel):
    sns.boxplot(data=data, ax=ax, orient='v', showfliers=False, showmeans=True, meanprops={'marker': 'o', 'markerfacecolor': 'white', 'markeredgecolor': 'black'})

    # Calculate quartiles
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    mean = data.mean()
    min = data.loc[data > 0].min()
    max = data.max()

    # min_url = data.loc[data == min].index[0]
    # print(min_url)
    # Set plot title and labels
    ax.set_title(title)
    ax.set_ylabel(ylabel)

    # Add mean and quartiles as annotations
    ax.annotate(f'Max: {max:.2f}', xy=(0.6, 0.95), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Upper Quartile: {Q3:.2f}', xy=(0.6, 0.85), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Mean: {mean:.2f}', xy=(0.6, 0.8), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Lower Quartile: {Q1:.2f}', xy=(0.6, 0.75), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Min: {min:.2f}', xy=(0.6, 0.65), xycoords='axes fraction', fontsize=9)

# Create a single figure with multiple subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharey = True)

# Create box plots for the 'pagesize' columns
create_box_plot(axes[0,0], org_hi['pagesize'], 'Page Size (High Income) - Original', 'Page Size (Kilobytes)')
create_box_plot(axes[0,1], webp_hi['pagesize'], 'Page Size (High Income) - WebP', 'Page Size (Kilobytes)')
create_box_plot(axes[0,2], avif_hi['pagesize'], 'Page Size (High Income) - AVIF', 'Page Size (Kilobytes)')

create_box_plot(axes[1,0], org_li['pagesize'], 'Page Size (Low Income) - Original', 'Page Size (Kilobytes)')
create_box_plot(axes[1,1], webp_li['pagesize'], 'Page Size (Low Income) - WebP','Page Size (Kilobytes)')
create_box_plot(axes[1,2], avif_li['pagesize'], 'Page Size(Low Income) - AVIF', 'Page Size (Kilobytes)')

plt.tight_layout()
plt.show()
