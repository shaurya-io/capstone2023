from urllib.parse import urlsplit

def extract_domain(url):
    # Split the URL and extract the netloc
    netloc = urlsplit(url).netloc

    # Remove 'www.' if it exists and split the netloc by '.'
    parts = netloc.replace('www.', '').split('.')

    # Return the domain in "url.tld" format
    domain = '.'.join(parts[:2])
    return domain

# Test the function with various URL formats
urls = [
    "http://url.tld/",
    "https://url.tld",
    "https://www.url.tld/",
    "http://www.url.tld/",
    "https://www.romhacking.net/?EXP_TYPE=ORG"
]

for url in urls:
    print(f"Original URL: {url}\nExtracted domain: {extract_domain(url)}\n")
