import os
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import gzip

def compress_csv(input_file, output_file, dedup=True, columns=None, rows=None):
    df = pd.read_csv(input_file)
    if dedup:
        df = df.drop_duplicates()
    if columns:
        df = df[columns]
    if rows:
        df = df.head(rows)
    with gzip.open(output_file, 'wt', encoding='utf-8') as gzfile:
        df.to_csv(gzfile, index=False)
    return os.path.getsize(input_file), os.path.getsize(output_file)

def compress_pdf(input_file, output_file, pages=None):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    if pages:
        for p in pages:
            if 0 <= p < len(reader.pages):
                writer.add_page(reader.pages[p])
    else:
        for page in reader.pages:
            writer.add_page(page)
    with open(output_file, "wb") as f:
        writer.write(f)
    return os.path.getsize(input_file), os.path.getsize(output_file)

def compress_image(input_file, output_file, quality=40, resize_percent=None):
    img = Image.open(input_file)
    if resize_percent and 1 <= resize_percent <= 100:
        new_size = (int(img.width * resize_percent / 100),
                    int(img.height * resize_percent / 100))
        img = img.resize(new_size)
    img.save(output_file, optimize=True, quality=quality)
    return os.path.getsize(input_file), os.path.getsize(output_file)

# --- main logic ---
print("=== Advanced File Compressor ===")
file_path = input("Enter path of file (CSV, PDF or Image): ").strip()

if not os.path.exists(file_path):
    print("File not found!")
    exit()

mode = input("Choose mode: [A]utomatic or [M]anual? ").strip().lower()
ext = os.path.splitext(file_path)[1].lower()
compressed_dir = "compressed"
os.makedirs(compressed_dir, exist_ok=True)

if mode == 'a':
    if ext == '.csv':
        out_file = os.path.join(compressed_dir, os.path.basename(file_path) + ".gz")
        orig, comp = compress_csv(file_path, out_file)
    elif ext == '.pdf':
        out_file = os.path.join(compressed_dir, "compressed_" + os.path.basename(file_path))
        orig, comp = compress_pdf(file_path, out_file)
    elif ext in ['.jpg', '.jpeg', '.png']:
        out_file = os.path.join(compressed_dir, "compressed_" + os.path.basename(file_path))
        orig, comp = compress_image(file_path, out_file)
    else:
        print("Unsupported file type for automatic mode")
        exit()
else:
    if ext == '.csv':
        dedup_choice = input("Remove duplicates? (y/n): ").strip().lower() == 'y'
        col_choice = input("Enter columns to keep (comma-separated) or leave blank for all: ").strip()
        columns = [c.strip() for c in col_choice.split(',')] if col_choice else None
        row_choice = input("Enter number of rows to keep (leave blank for all): ").strip()
        rows = int(row_choice) if row_choice else None
        out_file = os.path.join(compressed_dir, os.path.basename(file_path) + ".gz")
        orig, comp = compress_csv(file_path, out_file, dedup=dedup_choice, columns=columns, rows=rows)

    elif ext == '.pdf':
        pages_input = input("Enter page numbers to keep (comma-separated, 1-based) or leave blank for all: ").strip()
        pages = [int(p.strip()) - 1 for p in pages_input.split(',')] if pages_input else None
        out_file = os.path.join(compressed_dir, "compressed_" + os.path.basename(file_path))
        orig, comp = compress_pdf(file_path, out_file, pages=pages)

    elif ext in ['.jpg', '.jpeg', '.png']:
        q = int(input("Enter image quality (10-90, lower = smaller size): "))
        resize_input = input("Resize percentage (1-100) or leave blank for no resize: ").strip()
        resize_percent = int(resize_input) if resize_input else None
        out_file = os.path.join(compressed_dir, "compressed_" + os.path.basename(file_path))
        orig, comp = compress_image(file_path, out_file, quality=q, resize_percent=resize_percent)

    else:
        print("Unsupported file type for manual mode")
        exit()

print(f"Original size: {orig} bytes")
print(f"Compressed size: {comp} bytes")
print(f"Compressed file saved to: {out_file}")
