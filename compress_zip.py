import os
import zipfile

# Input file (you can test with CSV, PDF, or image)
input_file = "samples/sample_data.csv"  # change to any file in samples
output_zip = f"compressed/{os.path.basename(input_file)}.zip"

# Check if file exists
if not os.path.exists(input_file):
    print(f"File not found: {input_file}")
else:
    # Original size
    original_size = os.path.getsize(input_file)
    
    # Create ZIP
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file, arcname=os.path.basename(input_file))
    
    # Compressed size
    compressed_size = os.path.getsize(output_zip)
    
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"ZIP file saved to: {output_zip}")
