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

# Function to create a box plot with mean and quartiles
def create_box_plot(ax, data, title, ylabel):
    sns.boxplot(data=data, ax=ax, orient='v', showmeans=True, meanprops={'marker': 'o', 'markerfacecolor': 'white', 'markeredgecolor': 'black'})

    # Calculate quartiles
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    mean = data.mean()
    min = data.min()
    max = data.max()

    # Set plot title and labels
    ax.set_title(title)
    ax.set_ylabel(ylabel)

    # Add mean and quartiles as annotations
    ax.annotate(f'Max: {max:.2f}', xy=(0.7, 0.95), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Upper Quartile: {Q3:.2f}', xy=(0.7, 0.85), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Mean: {mean:.2f}', xy=(0.7, 0.8), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Lower Quartile: {Q1:.2f}', xy=(0.7, 0.75), xycoords='axes fraction', fontsize=9)
    ax.annotate(f'Min: {min:.2f}', xy=(0.7, 0.65), xycoords='axes fraction', fontsize=9)

# Create a single figure with multiple subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey = True)

# Create box plots for the 'plt' columns
create_box_plot(axes[0], org_hi['plt'], 'Page Load Time (High Income) - Original', 'plt (seconds)')
create_box_plot(axes[1], webp_hi['plt'], 'Page Load Time (High Income) - WebP', 'plt (seconds)')
create_box_plot(axes[2], avif_hi['plt'], 'Page Load Time (High Income) - AVIF', 'plt (seconds)')

plt.tight_layout()
plt.show()
