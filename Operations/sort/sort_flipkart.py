import fitz  # PyMuPDF
import os
import json

def sort_pdf_by_flipkart_skus(input_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SKU_FILE = os.path.join(BASE_DIR, "..", "..", "sku_data", "flipkart_skus.json")
    OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, "flipkart_sorted_output.pdf")

    # ✅ Step 2: Load SKUs from JSON
    try:
        with open(SKU_FILE, "r", encoding="utf-8") as f:
            sku_list = json.load(f)
    except Exception as e:
        print(f"Error reading SKU file: {e}")
        return None

    if not sku_list:
        print("No SKUs found in the JSON file.")
        return None

    # ✅ Step 3: Open PDF
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None

    # ✅ Step 4: Match pages to SKUs (allow duplicates)
    matched_pages = []
    unmatched_pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        matched = False
        for sku in sku_list:
            if sku in text:
                matched_pages.append((sku, page_num))
                matched = True
                break
        if not matched:
            unmatched_pages.append(page_num)
            print(f"⚠ Page {page_num + 1}: SKU not found")

    # ✅ Step 5: Sort matched pages by SKU order
    sorted_pages = []
    for sku in sku_list:
        for sku_found, page_index in matched_pages:
            if sku_found == sku:
                sorted_pages.append(page_index)

    # ✅ Step 6: Create new PDF
    sorted_pdf = fitz.open()
    for index in sorted_pages:
        sorted_pdf.insert_pdf(doc, from_page=index, to_page=index)

    if not sorted_pages:
        print("❌ No matching SKUs found in any page. No output PDF generated.")
        OUTPUT_PATH = None
    else:
        sorted_pdf.save(OUTPUT_PATH)
        print(f"✅ Sorted PDF saved to: {OUTPUT_PATH}")

    doc.close()
    sorted_pdf.close()
    return OUTPUT_PATH
