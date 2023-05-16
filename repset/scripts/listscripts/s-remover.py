import csv

# Function to remove 's' from the second column of a given line
def remove_s_from_second_column(line):
    second_column = line[1]
    modified_second_column = second_column.replace('s', '')
    line[1] = modified_second_column
    return line

# Open the original file and read its content
with open('../../data/data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read the header

    # Process the header if needed (assuming it doesn't need processing in this case)

    # Open the output file and write the header
    with open('../../data/data2.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)

        # Iterate through the lines, modify the second column, and write them to the output file
        for line in reader:
            modified_line = remove_s_from_second_column(line)
            writer.writerow(modified_line)
