import os
import json
import fitz
import pandas as pd  
from flask import Flask, render_template, request, redirect, url_for, send_file
from Operations.merge import merge_pdfs
from Operations.rotate import rotate_pdf
from Operations.crop import crop_pdf
from Operations.compress import compress_pdf
from Operations.sort.sort_amazon import sort_pdf_by_amazon_skus
from Operations.sort.sort_flipkart import sort_pdf_by_flipkart_skus

from werkzeug.utils import secure_filename
from Operations.crop_merge import crop_merge_pdf


UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


app = Flask(__name__)
DATA_DIR = "sku_data"
os.makedirs(DATA_DIR, exist_ok=True)

flipkart_file = os.path.join(DATA_DIR, "flipkart_skus.json")
amazon_file = os.path.join(DATA_DIR, "amazon_skus.json")

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/delete_file", methods=["POST"])
def delete_file():
    filename = request.form.get("filename")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for("home"))

@app.route("/delete_all_skus", methods=["POST"])
def delete_all_skus():
    platform = request.form["platform"]
    save_skus(platform, [])  # Save empty list
    return redirect(url_for('sku'))

@app.route('/sku')
def sku():
    flipkart_skus = load_skus("flipkart")
    amazon_skus = load_skus("amazon")
    return render_template("sku.html", flipkart_skus=flipkart_skus, amazon_skus=amazon_skus)

def load_skus(platform):
    path = flipkart_file if platform == "flipkart" else amazon_file
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_skus(platform, sku_list):
    path = flipkart_file if platform == "flipkart" else amazon_file
    with open(path, "w") as f:
        json.dump(sku_list, f, indent=2)

@app.route("/add_sku", methods=["POST"])
def add_sku():
    sku = request.form["sku"].strip()
    platform = request.form["platform"]
    sku_list = load_skus(platform)
    if sku not in sku_list:
        sku_list.append(sku)
        save_skus(platform, sku_list)
    return redirect(url_for('sku'))

@app.route("/delete_sku", methods=["POST"])
def delete_sku():
    sku = request.form["sku"].strip()
    platform = request.form["platform"]
    sku_list = load_skus(platform)
    if sku in sku_list:
        sku_list.remove(sku)
        save_skus(platform, sku_list)
    return redirect(url_for('sku'))

@app.route("/upload_sku_excel", methods=["POST"])
def upload_sku_excel():
    file = request.files.get("sku_file")
    platform = request.form.get("platform")

    if not file or not platform:
        return "Missing file or platform", 400

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ['.csv', '.xlsx']:
        return "Only .csv or .xlsx files are allowed", 400

    # Load data
    if ext == '.csv':
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Assume SKU IDs are in the first column
    sku_column = df.columns[0]
    new_skus = df[sku_column].dropna().astype(str).tolist()

    # Load, merge, and save
    existing_skus = load_skus(platform)
    combined = list(set(existing_skus + new_skus))
    save_skus(platform, combined)

    return redirect(url_for("sku"))

@app.route('/process', methods=['POST'])
def process():
    operation = request.form['operation']

    if operation == "merge":
        output_path = merge_pdfs(request.files.getlist('file'))

    elif operation == "crop_merge":
        files = request.files.getlist('file')
        crop_box = fitz.Rect(180, 460, 410, 815)
        output_path = crop_merge_pdf(files, crop_box)

    elif operation == "rotate90":
        output_path = rotate_pdf(request.files['file'], 90)

    elif operation == "rotate180":
        output_path = rotate_pdf(request.files['file'], 180)

    elif operation == "rotate270":
        output_path = rotate_pdf(request.files['file'], 270)

    elif operation == "crop":
        output_path = crop_pdf(request.files['file'])

    elif operation == 'compress':
        output_path = compress_pdf(request.files['file'])

    elif operation == "sortamazon":
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        input_path = os.path.join("uploads", filename)
        uploaded_file.save(input_path)
        output_path = sort_pdf_by_amazon_skus(input_path)

    elif operation == "sortflipcart":
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        input_path = os.path.join("uploads", filename)
        uploaded_file.save(input_path)
        output_path = sort_pdf_by_flipkart_skus(input_path)

    elif operation == "allfunction":
        files = request.files.getlist('file')
        crop_box = fitz.Rect(180, 460, 410, 815)
        firstoutputFile = crop_merge_pdf(files, crop_box)
        output_path = sort_pdf_by_flipkart_skus(firstoutputFile)
 
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
