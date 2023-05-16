import pandas as pd

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    df['lh_si'] = pd.to_numeric(df['lh_si'], errors='coerce')
    return df

# Read and process the CSV file
org_hi = process_file('../../../data/processed/compiled_country_avif_hi.csv')

# Function to categorize the data
def categorize_lh_si(value):
    if value < 3.4:
        return 'FAST'
    elif value >= 3.4 and value < 5.8:
        return 'MODERATE'
    else:
        return 'SLOW'

# Apply the categorization function to the 'lh_si' column
org_hi['category'] = org_hi['lh_si'].apply(categorize_lh_si)

# Count the number of entries in each category
category_counts = org_hi['category'].value_counts()

# Print the number of entries in each category
print("Number of entries in each category:")
print(category_counts)
