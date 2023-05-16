import os
import matplotlib.pyplot as plt

# Replace 'path/to/your/folder' with the path to your folder
folder_path = '../merged_raw'

# List of supported image file extensions
image_extensions = ['.png', '.jpeg', '.jpg', '.webp', '.avif']

# Initialize a list to store image details
image_list = []

# Iterate through the folder
for file_name in os.listdir(folder_path):
    # Check if the file has a supported image extension
    if any(file_name.endswith(ext) for ext in image_extensions):
        file_path = os.path.join(folder_path, file_name)

        # Get the file size in bytes
        file_size_bytes = os.path.getsize(file_path)
        file_size_kb = file_size_bytes / 1024  # Convert to kilobytes

        # Store the image details in the list
        image_list.append({'name': file_name, 'size': file_size_kb})

# Sort the image list by size
image_list.sort(key=lambda x: x['size'])

# Extract the sizes of the images
image_sizes = [img['size'] for img in image_list]

# Plot the line chart
plt.figure(figsize=(10, 6))
plt.plot(image_sizes)
plt.xlabel('Image Index (sorted by size)')
plt.ylabel('Image Size (KB)')
plt.title('Image Sizes')

# Show the plot
plt.show()
