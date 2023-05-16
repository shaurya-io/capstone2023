import csv
import os

def split_csv(input_file):
    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

        org_rows = [header]
        avif_rows = [header]
        webp_rows = [header]

        for row in reader:
            for cell in row:
                if "?EXP_TYPE=ORG" in cell:
                    org_rows.append(row)
                    break
                elif "?EXP_TYPE=AVIF" in cell:
                    avif_rows.append(row)
                    break
                elif "?EXP_TYPE=WEBP" in cell:
                    webp_rows.append(row)
                    break

    os.makedirs('data/processed', exist_ok=True)

    with open('data/processed/country_org.csv', 'w', newline='') as org_file:
        writer = csv.writer(org_file)
        writer.writerows(org_rows)

    with open('data/processed/country_avif.csv', 'w', newline='') as avif_file:
        writer = csv.writer(avif_file)
        writer.writerows(avif_rows)

    with open('data/processed/country_webp.csv', 'w', newline='') as webp_file:
        writer = csv.writer(webp_file)
        writer.writerows(webp_rows)

if __name__ == "__main__":
    input_file = "data/processed/sorted_country.csv"
    split_csv(input_file)
