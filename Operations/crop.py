import os
import fitz  # PyMuPDF

# OUTPUT_FOLDER = "outputs"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def crop_pdf(input_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, 'crop_output.pdf')
    doc = fitz.open(input_path)

    user_crop_rect = fitz.Rect(180, 460, 410, 815)

    for page in doc:
        # Ensure crop_rect is within the page's MediaBox
        current_media_box = page.rect
        safe_crop_rect = user_crop_rect & current_media_box  # intersect
        if safe_crop_rect.is_empty:
            # fallback if the intersection is invalid
            safe_crop_rect = current_media_box

        page.set_cropbox(safe_crop_rect)
        page.set_mediabox(safe_crop_rect)

    doc.save(output_path)
    doc.close()
    return output_path
