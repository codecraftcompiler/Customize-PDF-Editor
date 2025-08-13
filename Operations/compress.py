import os
from PyPDF2 import PdfReader, PdfWriter

# OUTPUT_FOLDER = "outputs"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def compress_pdf(input_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_path = os.path.join(OUTPUT_DIR, "compressed.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
