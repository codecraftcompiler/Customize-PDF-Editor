import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter

# OUTPUT_FOLDER = "outputs"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def crop_merge_pdf(file_paths, crop_box=None):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Step 1: Merge PDFs using PyPDF2
    merged_path = os.path.join(OUTPUT_DIR, "merged_temp.pdf")
    writer = PdfWriter()

    for input_path in file_paths:
        reader = PdfReader(input_path)
        for page in reader.pages:
            writer.add_page(page)

    with open(merged_path, "wb") as f:
        writer.write(f)

    # Step 2: Crop using fitz
    doc = fitz.open(merged_path)
    cropped_path = os.path.join(OUTPUT_DIR, "merged_and_cropped.pdf")

    # Default crop rectangle if not given: (x0, y0, x1, y1)
    if crop_box is None:
        crop_box = fitz.Rect(180, 460, 410, 815)

    for page in doc:
        page.set_cropbox(crop_box)
        page.set_mediabox(crop_box)

    doc.save(cropped_path)
    doc.close()

    # Clean up temporary merged file
    os.remove(merged_path)

    return cropped_path
