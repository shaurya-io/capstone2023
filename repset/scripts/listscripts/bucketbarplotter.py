import pandas as pd
import matplotlib.pyplot as plt

plt.rc('xtick', labelsize=2)
plt.rc('ytick', labelsize=12)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Read the CSV file into a DataFrame
data = pd.read_csv('data_with_buckets.csv')

# Count the frequency of different values in the 'bucket' column
bucket_counts = data['bucket'].value_counts()

# Create the bar chart
plt.bar(bucket_counts.index, bucket_counts.values/9)

# Set chart labels and title
plt.xlabel('Bucket')
plt.ylabel('Frequency')
plt.title('Frequency of Different Buckets')

# Show the chart
plt.show()
