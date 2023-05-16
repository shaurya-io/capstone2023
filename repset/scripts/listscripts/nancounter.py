import pandas as pd

# Function to read and process the CSV file
def process_file(file_path):
    df = pd.read_csv(file_path, na_values='-')
    return df

# Read and process the CSV file
df = process_file('../../../data2/data2.csv')

# Count the missing values in the DataFrame
missing_values_count = df.isna().sum().sum()

# Print the number of missing values
print(f'The number of missing values in the DataFrame is: {missing_values_count}')
