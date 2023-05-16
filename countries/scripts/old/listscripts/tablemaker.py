import pandas as pd
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

# Calculate pagesize efficiency gains
webp_hi['gain'] = (org_hi['pagesize'] - webp_hi['pagesize']) / org_hi['pagesize'] * 100
avif_hi['gain'] = (org_hi['pagesize'] - avif_hi['pagesize']) / org_hi['pagesize'] * 100

webp_li['gain'] = (org_li['pagesize'] - webp_li['pagesize']) / org_li['pagesize'] * 100
avif_li['gain'] = (org_li['pagesize'] - avif_li['pagesize']) / org_li['pagesize'] * 100

# Calculate quartiles
Q1_hi = org_hi['pagesize'].quantile(0.25)
Q3_hi = org_hi['pagesize'].quantile(0.75)
Q1_li = org_li['pagesize'].quantile(0.25)
Q3_li = org_li['pagesize'].quantile(0.75)

# Filter data by quartiles
webp_hi_lower = webp_hi[org_hi['pagesize'] <= Q1_hi]
avif_hi_lower = avif_hi[org_hi['pagesize'] <= Q1_hi]
webp_li_lower = webp_li[org_li['pagesize'] <= Q1_li]
avif_li_lower = avif_li[org_li['pagesize'] <= Q1_li]

webp_hi_upper = webp_hi[org_hi['pagesize'] >= Q3_hi]
avif_hi_upper = avif_hi[org_hi['pagesize'] >= Q3_hi]
webp_li_upper = webp_li[org_li['pagesize'] >= Q3_li]
avif_li_upper = avif_li[org_li['pagesize'] >= Q3_li]

# Calculate average gains for each format and income group by quartiles
avg_webp_hi_lower = webp_hi_lower['gain'].mean()
avg_avif_hi_lower = avif_hi_lower['gain'].mean()
avg_webp_li_lower = webp_li_lower['gain'].mean()
avg_avif_li_lower = avif_li_lower['gain'].mean()

avg_webp_hi_upper = webp_hi_upper['gain'].mean()
avg_avif_hi_upper = avif_hi_upper['gain'].mean()
avg_webp_li_upper = webp_li_upper['gain'].mean()
avg_avif_li_upper = avif_li_upper['gain'].mean()

# Create a DataFrame to display the results in a table
data = {'Income Group': ['High Income', 'High Income', 'Low Income', 'Low Income'],
        'Quartile': ['Lower Quartile org pagesize', 'Upper Quartile org pagesize', 'Lower Quartile org pagesize', 'Upper Quartile org pagesize'],
        'WebP': [avg_webp_hi_lower, avg_webp_hi_upper, avg_webp_li_lower, avg_webp_li_upper],
        'AVIF': [avg_avif_hi_lower, avg_avif_hi_upper, avg_avif_li_lower, avg_avif_li_upper]}

df = pd.DataFrame(data)

# Calculate the overall average gains for each format
overall_webp_avg = (avg_webp_hi_lower + avg_webp_hi_upper + avg_webp_li_lower + avg_webp_li_upper) / 4
overall_avif_avg = (avg_avif_hi_lower + avg_avif_hi_upper + avg_avif_li_lower + avg_avif_li_upper) / 4

# Add the overall average gains to the DataFrame
df = df.append({'Income Group': 'Overall', 'Quartile': 'Overall', 'WebP': overall_webp_avg, 'AVIF': overall_avif_avg}, ignore_index=True)

# Transpose the DataFrame to switch rows and columns
df = df.set_index(['Income Group', 'Quartile']).T

# Create a table plot using Matplotlib
fig, ax = plt.subplots(figsize=(16, 8))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center')

# Save the table as an image
plt.savefig('table_as_image.png', dpi=300, bbox_inches='tight')

# Display the table plot
plt.show()
