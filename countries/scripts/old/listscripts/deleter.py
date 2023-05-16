import csv

input_file = 'data/processed/country_AVIF.csv'
output_file = 'data/processed/country_AVIF_URLmatched.csv'
token = '?EXP_TYPE=AVIF'

# Read the input CSV file
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)

    # Write the output CSV file with the token removed
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        for row in reader:
            # Remove the token from each cell in the row
            updated_row = [cell.replace(token, '') for cell in row]
            writer.writerow(updated_row)
