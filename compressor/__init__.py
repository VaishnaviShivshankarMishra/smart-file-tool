import os
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import gzip

def compress_csv(input_file, output_file, dedup=True):
    df = pd.read_csv(input_file)
    if dedup:
        df = df.drop_duplicates()
    with gzip.open(output_file, 'wt', encoding='utf-8') as gzfile:
        df.to_csv(gzfile, index=False)
    return os.path.getsize(input_file), os.path.getsize(output_file)

def compress_pdf(input_file, output_file, page_range=None):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    pages = page_range if page_range else range(len(reader.pages))
    for i in pages:
        writer.add_page(reader.pages[i])
    with open(output_file, "wb") as f:
        writer.write(f)
    return os.path.getsize(input_file), os.path.getsize(output_file)

def compress_image(input_file, output_file, quality=40):
    img = Image.open(input_file)
    img.save(output_file, optimize=True, quality=quality)
    return os.path.getsize(input_file), os.path.getsize(output_file)
