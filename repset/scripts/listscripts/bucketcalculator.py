import pandas as pd
from urllib.parse import urlsplit
from tqdm import tqdm

def extract_domain(url):
    # Split the URL and extract the netloc
    netloc = urlsplit(url).netloc

    # Remove 'www.' if it exists and split the netloc by '.'
    parts = netloc.replace('www.', '').split('.')

    # Return the domain in "url.tld" format
    domain = '.'.join(parts[:2])
    return domain

def bucket_by_index(index):
    ranges = [
        (1, 100),
        (101, 300),
        (301, 700),
        (701, 1500),
        (1501, 3100),
        (3101, 6300),
        (6301, 12700),
        (12701, 25500),
        (25501, 51100),
        (51101, 102300),
        (102301, 204700),
        (204701, 409500),
        (409501, 819100),
        (819101, 999999)
    ]
    for i, (start, end) in enumerate(ranges, 1):
        if start <= index <= end:
            return f"{start}-{end}"
    return None

# Load data.csv and 1m.csv
data_df = pd.read_csv("../../data/data.csv")
one_million_df = pd.read_csv("../../data/1m.csv", header=None, names=["domain"])

# Extract domains from URLs in data.csv
data_df["domain"] = data_df["URL"].apply(extract_domain)

# Create a dictionary for faster domain look-up in 1m.csv
one_million_dict = one_million_df["domain"].to_dict()

# Initialize the bucket column
data_df["bucket"] = ""
count = 0
# Iterate through the data.csv dataframe with a progress bar
for index, row in tqdm(data_df.iterrows(), total=len(data_df), desc="Processing URLs"):
    domain = row["domain"]
    
    # Find the index of the matching domain in 1m.csv
    matched_index = None
    for i, one_million_domain in one_million_dict.items():
        if domain == one_million_domain:
            matched_index = i + 1
            break

    # If a match is found, assign the bucket
    if matched_index is not None:
        data_df.at[index, "bucket"] = bucket_by_index(matched_index)
        count+=1

# Save the result to a new CSV file
#data_df.to_csv("data_with_buckets.csv", index=False)
print(count)