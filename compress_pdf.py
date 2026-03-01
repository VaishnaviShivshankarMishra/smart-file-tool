import PyPDF2
import os

# Paths
input_pdf = "samples/sample.pdf"
output_pdf = "compressed/sample_compressed.pdf"

# Check if PDF exists
if not os.path.exists(input_pdf):
    print(f"PDF not found: {input_pdf}")
else:
    # Open the input PDF
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Copy all pages to writer
        for page in reader.pages:
            writer.add_page(page)

        # Write compressed PDF
        with open(output_pdf, "wb") as out_file:
            writer.write(out_file)

    print(f"PDF compressed and saved to: {output_pdf}")
