import kagglehub

# Download latest version
path = kagglehub.dataset_download("harturo123/online-adds-of-used-cars")

print("Path to dataset files:", path)