from PyPDF2 import PdfMerger
import os

# OUTPUT_FOLDER = "outputs"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def merge_pdfs(file_paths):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    merger = PdfMerger()
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            merger.append(file_path)
    
    output_path = os.path.join(OUTPUT_DIR, "merged.pdf")
    merger.write(output_path)
    merger.close()
    return output_path