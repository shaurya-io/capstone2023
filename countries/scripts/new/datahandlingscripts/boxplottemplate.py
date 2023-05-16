import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plot
import numpy as np

# Aesthetic configurations
plot.rc('xtick', labelsize=12)
plot.rc('ytick', labelsize=12)
plot.rcParams['pdf.fonttype'] = 42
plot.rcParams['ps.fonttype'] = 42

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

def create_combined_box_plot(ax, data_org, data_webp, data_avif, title, ylabel):
    # Filter the data to include only values of plt > 1
    data_combined = [data_org[data_org['plt'] > 0]['plt'], data_webp[data_webp['plt'] > 0]['plt'], data_avif[data_avif['plt'] > 0]['plt']]
    
    box_plots = sns.boxplot(data=data_combined, ax=ax, orient='v', showfliers=False)

    ax.set_title(title, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticklabels(['Original', 'WebP', 'AVIF'])

    # Add labels to the box plots
    for i, box in enumerate(box_plots.artists):
        box.set_edgecolor('black')
        
        # Set the facecolors for each box
        if i == 0:
            box.set_facecolor('tab:blue')
        elif i == 1:
            box.set_facecolor('tab:orange')
        else:
            box.set_facecolor('tab:green')

    # Add mean value annotations
    for i, mean in enumerate(data_combined):
        y_mean = mean.mean()
        
        # Add a small dot/circle for the mean value
        ax.scatter(i, y_mean, color='red', s=30, zorder=3)
        
        # Add the mean value text next to the dot/circle
        ax.annotate(f'{y_mean:.2f}', xy=(i + 0.1, y_mean), xycoords='data', fontsize=12,
                    ha='left', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=1))

    # Add a semi-transparent grid in the background
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    # Set smaller divisions on the y-axis
    y_max = max(data_org['plt'].max(), data_webp['plt'].max(), data_avif['plt'].max())
    y_ticks = np.arange(0, 55, step=5)  # Adjust the step value to change the divisions
    ax.set_yticks(y_ticks)


# Create a single figure with two subplots
fig, axes = plot.subplots(1, 2, figsize=(12, 6), sharey=True)


# Create combined box plots for high-income and low-income groups
create_combined_box_plot(axes[0], org_hi, webp_hi, avif_hi, 'Page Load Time - High Income', 'Page Load Time (seconds)')
create_combined_box_plot(axes[1], org_li, webp_li, avif_li, 'Page Load Time - Low Income', '')


plot.tight_layout(pad=0.5)
plot.savefig('plt.pdf')
plot.show()