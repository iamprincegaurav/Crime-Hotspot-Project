import pandas as pd

# Load the dataset
df = pd.read_csv("data/crime_data.csv")

# Convert date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Show first few rows
print("Dataset Head:")
print(df.head())

# Column info check
print("\nDataset Info:")
print(df.info())
