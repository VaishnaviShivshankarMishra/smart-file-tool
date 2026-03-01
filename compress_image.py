from PIL import Image
import os

# Path to input image
input_path = "samples/sample_image.jpg"
output_folder = "compressed"
output_path = os.path.join(output_folder, "sample_image_compressed.jpg")

# Create compressed folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Check if image exists
if not os.path.exists(input_path):
    print(f"Image not found: {input_path}")
else:
    # Open image
    img = Image.open(input_path)
    
    # Convert to RGB (important if PNG with transparency)
    img = img.convert("RGB")

    # Compress and save
    img.save(output_path, optimize=True, quality=50)
    print(f"Image compressed and saved to: {output_path}")