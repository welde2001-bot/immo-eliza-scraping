

import pandas as pd

# Load CSV with correct separator
df = pd.read_csv(
    r"C:\Users\sandy\Desktop\immo-eliza-scraping\properties.csv",  # your file path
    encoding="utf-8"                           # specify encoding
)

# Clean up column names: strip spaces, lowercase, replace spaces with underscores
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Optional: drop 'equipped_kitchen' if you want
df.drop(columns=['equipped_kitchen'], errors='ignore', inplace=True)
df.drop(columns=['furnished'], errors='ignore', inplace=True)
df.drop(columns=['garden_area'], errors='ignore', inplace=True)

# Quick check
print(df.columns.tolist())
print(df.head())

df

