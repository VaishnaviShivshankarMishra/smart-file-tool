from PIL import Image
import os

# --- Image Conversion Script ---
print("=== Image Format Converter ===")
file_path = input("Enter path of image: ").strip()

if not os.path.exists(file_path):
    print("File not found!")
    exit()

ext = os.path.splitext(file_path)[1].lower()
target_format = input("Convert to format (jpeg/png): ").strip().lower()

if target_format not in ['jpeg', 'png']:
    print("Unsupported format")
    exit()

# Define output path
base_name = os.path.splitext(os.path.basename(file_path))[0]
output_file = f"converted_{base_name}.{target_format}"
img = Image.open(file_path)

# Convert
if target_format == 'jpeg':
    img = img.convert('RGB')  # JPEG does not support alpha
img.save(output_file, optimize=True, quality=85)

print(f"Image converted and saved to: {output_file}")
