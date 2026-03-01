import pandas as pd
import gzip
import shutil

# Path to sample CSV
csv_path = "samples/sample_data.csv"

# Load CSV
df = pd.read_csv(csv_path)
print("Original rows:", len(df))

# Drop duplicates
dedup_df = df.drop_duplicates()
print("Rows after removing duplicates:", len(dedup_df))

# Column filter (interactive)
print("\nColumns available in CSV:", list(dedup_df.columns))
cols_input = input("Enter columns to keep (comma-separated, e.g. id,name): ")
columns_to_keep = [col.strip() for col in cols_input.split(",")]
valid_columns = [col for col in columns_to_keep if col in dedup_df.columns]

if not valid_columns:
    print("No valid columns selected. Keeping all columns.")
    valid_columns = dedup_df.columns.tolist()

filtered_df = dedup_df[valid_columns]

# Save filtered CSV
filtered_csv_path = "compressed/sample_filtered.csv"
filtered_df.to_csv(filtered_csv_path, index=False)
print(f"\nFiltered CSV saved to: {filtered_csv_path}")

# --- Gzip compression ---
gzip_path = "compressed/sample_filtered.csv.gz"
with open(filtered_csv_path, 'rb') as f_in:
    with gzip.open(gzip_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"Gzip compressed CSV saved to: {gzip_path}")
