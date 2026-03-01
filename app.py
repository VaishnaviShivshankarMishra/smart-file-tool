import streamlit as st
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile
import os
import matplotlib.pyplot as plt

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(page_title="Smart File Tool", page_icon="📦", layout="centered")
st.title("📦 Smart File Tool")
st.markdown("Compress, convert and analyze files easily.")

# ------------------ FILE UPLOAD ------------------ #
uploaded_file = st.file_uploader(
    "Upload your file",
    type=["pdf", "csv", "jpg", "jpeg", "png", "exe", "txt", "docx", "xlsx"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    file_type = uploaded_file.name.split(".")[-1].lower()
    mode = st.radio("Choose Compression Mode", ["Automatic", "Manual"], index=0)

    orig_bytes = uploaded_file.getvalue()
    compressed_bytes = None

    # ------------------ IMAGE ------------------ #
    if file_type in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)

        # Fix RGBA / Transparency issue
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        quality = 60 if mode == "Automatic" else st.slider("Select Image Quality", 10, 95, 60)

        buf = io.BytesIO()
        image.save(buf, format="JPEG", quality=quality, optimize=True)
        buf.seek(0)
        compressed_bytes = buf.getvalue()

        # -------- IMAGE CONVERSION -------- #
        st.subheader("🖼️ Image Conversion")
        if st.checkbox("Convert Image Format"):
            target_format = st.selectbox("Choose target format", ["PNG", "JPEG", "WEBP"])
            buf_conv = io.BytesIO()

            # Convert properly for PNG if needed
            if target_format == "PNG":
                image.save(buf_conv, format="PNG")
            else:
                image.save(buf_conv, format=target_format)

            buf_conv.seek(0)
            converted_bytes = buf_conv.getvalue()

            conv_name = f"converted_{os.path.splitext(uploaded_file.name)[0]}.{target_format.lower()}"

            st.download_button(
                label="⬇️ Download Converted Image",
                data=converted_bytes,
                file_name=conv_name,
                mime=f"image/{target_format.lower()}"
            )

    # ------------------ CSV ------------------ #
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)

        if mode == "Manual":
            st.write("Preview CSV", df.head())

            rows_to_keep = st.text_input("Rows to keep (comma-separated, e.g., 0,1,2)")
            cols_to_keep = st.multiselect("Columns to keep", df.columns.tolist())

            if rows_to_keep:
                rows_idx = [int(i) for i in rows_to_keep.split(",") if i.strip().isdigit()]
                if rows_idx:
                    df = df.iloc[rows_idx]

            if cols_to_keep:
                df = df[cols_to_keep]

            compression = st.selectbox("CSV compression", ["gzip", "zip", "bz2", "None"])
            compression = None if compression == "None" else compression
        else:
            compression = "gzip"

        buf = io.BytesIO()
        df.to_csv(buf, index=False)
        buf.seek(0)

        if compression:
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(uploaded_file.name, buf.getvalue())
            zip_buf.seek(0)
            compressed_bytes = zip_buf.getvalue()
        else:
            compressed_bytes = buf.getvalue()

    # ------------------ PDF ------------------ #
    elif file_type == "pdf":
        reader = PdfReader(uploaded_file)

        if mode == "Manual":
            total_pages = len(reader.pages)
            st.write(f"PDF has {total_pages} pages")
            pages_to_keep = st.multiselect(
                "Pages to keep",
                list(range(1, total_pages + 1)),
                default=list(range(1, total_pages + 1))
            )
        else:
            pages_to_keep = list(range(1, len(reader.pages) + 1))

        writer = PdfWriter()
        for p in pages_to_keep:
            writer.add_page(reader.pages[p - 1])

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        compressed_bytes = buf.getvalue()

    # ------------------ OTHER FILES ------------------ #
    else:
        st.info("This file type will be placed into a .zip archive")

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(uploaded_file.name, orig_bytes)

        buf.seek(0)
        compressed_bytes = buf.getvalue()

    # ------------------ ANALYSIS & DOWNLOAD ------------------ #
    if compressed_bytes:

        if file_type in ["jpg", "jpeg", "png"]:
            dl_name = f"compressed_{os.path.splitext(uploaded_file.name)[0]}.jpg"
        elif file_type in ["csv", "pdf"]:
            dl_name = f"compressed_{uploaded_file.name}"
        else:
            dl_name = f"{uploaded_file.name}.zip"

        st.download_button(
            label="⬇️ Download Compressed File",
            data=compressed_bytes,
            file_name=dl_name,
            mime="application/octet-stream"
        )

        # -------- FILE SIZE ANALYSIS -------- #
        orig_size = len(orig_bytes)
        comp_size = len(compressed_bytes)

        reduction = ((orig_size - comp_size) / orig_size * 100) if orig_size > 0 else 0

        st.subheader("📊 Compression Analysis")
        st.write(f"Original size: **{orig_size/1024:.2f} KB**")
        st.write(f"Compressed size: **{comp_size/1024:.2f} KB**")
        st.write(f"Reduction: **{reduction:.1f}%**")

        # -------- BAR CHART -------- #
        fig, ax = plt.subplots()
        ax.bar(["Original", "Compressed"], [orig_size/1024, comp_size/1024])
        ax.set_ylabel("File size (KB)")
        ax.set_title("File Size Comparison")
        st.pyplot(fig)

        # -------- PIE CHART -------- #
        fig2, ax2 = plt.subplots()
        saved = max(0, orig_size - comp_size)

        ax2.pie(
            [comp_size, saved],
            labels=["Compressed", "Saved"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax2.set_title("Compression Breakdown")
        st.pyplot(fig2)