import csv

# Define the token lists
li_tokens = ['.mm/', '.vn/', '.ph/', '.id/', '.eg/', '.ir/', '.pk/', '.bd/', '.in/', '.tz/', '.ke/', '.ng/', '.cd/', '.th/', '.et/']
hi_tokens = ['.kr/', '.jp/', '.es/', '.it/', '.fr/', '.uk/', '.de/', '.us/', '.cn/', '.tr/', '.ru/', '.co/', '.br/', '.mx/', '.za/']

# Function to check if a line contains any of the specified tokens
def contains_token(line, tokens):
    for token in tokens:
        if token in line:
            return True
    return False

# Function to sort lines based on the order of tokens in the list
def sort_lines(lines, tokens):
    sorted_lines = []
    for token in tokens:
        for line in lines:
            if token in ','.join(line):
                sorted_lines.append(line)
    return sorted_lines

# Open the original file and read its content
with open('data/processed/country_avif.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read the header

    hi_lines = []
    li_lines = []

    # Iterate through the lines and add them to the appropriate list
    for line in reader:
        line_str = ','.join(line)
        if contains_token(line_str, hi_tokens):
            hi_lines.append(line)
        elif contains_token(line_str, li_tokens):
            li_lines.append(line)

    # Sort the lines according to the token order
    sorted_hi_lines = sort_lines(hi_lines, hi_tokens)
    sorted_li_lines = sort_lines(li_lines, li_tokens)

    # Open the output files and write the header and sorted lines
    with open('data/processed/country_avif_hi.csv', 'w', newline='') as hi_file, open('data/processed/country_avif_li.csv', 'w', newline='') as li_file:
        hi_writer = csv.writer(hi_file)
        li_writer = csv.writer(li_file)

        hi_writer.writerow(header)
        li_writer.writerow(header)

        hi_writer.writerows(sorted_hi_lines)
        li_writer.writerows(sorted_li_lines)
