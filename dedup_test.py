import pandas as pd

# Path to your sample CSV file
csv_path = "samples/sample_data.csv"  # change if your file name differs

# Load CSV
df = pd.read_csv(csv_path)
print("Original rows:", len(df))

# Drop duplicate rows
dedup_df = df.drop_duplicates()
print("Rows after removing duplicates:", len(dedup_df))

# --- Interactive column filter ---
print("\nColumns available in CSV:", list(dedup_df.columns))
cols_input = input("Enter columns to keep (comma-separated, e.g. id,name): ")

# Convert input string to list and remove extra spaces
columns_to_keep = [col.strip() for col in cols_input.split(",")]

# Validate columns
valid_columns = [col for col in columns_to_keep if col in dedup_df.columns]
if not valid_columns:
    print("No valid columns selected. Keeping all columns.")
    valid_columns = dedup_df.columns.tolist()

# Filter columns
filtered_df = dedup_df[valid_columns]

# Save deduplicated+filtered file
output_path = "compressed/sample_data_dedup_filtered.csv"
filtered_df.to_csv(output_path, index=False)

print(f"\nFiltered CSV saved to: {output_path}")
