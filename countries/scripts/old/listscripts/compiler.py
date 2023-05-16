import pandas as pd

def process_file(file_path):
    # Read the CSV file into a Pandas DataFrame, treating '-' as NaN
    df = pd.read_csv(file_path, na_values='-')

    # Convert string values to numeric values where possible
    for col in df.columns:
        if col != 'URL':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def compile_data(df):
    # Group by URL and compute the mean for each group
    compiled_df = df.groupby('URL').mean().reset_index()
    compiled_df = compiled_df.round(3)
    return compiled_df

def main():
    input_file = 'data/processed/country_avif_li.csv'
    output_file = 'data/processed/compiled_country_avif_li.csv'

    df = process_file(input_file)
    compiled_df = compile_data(df)

    print(compiled_df)

    # Write the compiled DataFrame to a new CSV file
    compiled_df.to_csv(output_file, index=False)

if __name__ == '__main__':
    main()
