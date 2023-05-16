import csv
import sys
import argparse

def sort_csv(input_file, output_file, column_to_sort):
    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        rows = sorted(reader, key=lambda row: row[column_to_sort].lower())

    with open(output_file, 'w', newline='') as sorted_csv_file:
        writer = csv.writer(sorted_csv_file)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort a CSV file alphabetically based on a specified column.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
    parser.add_argument("-c", "--column", type=int, required=True, help="The index of the column to sort by (0-indexed)")

    args = parser.parse_args()

    sort_csv(args.input, args.output, args.column)
