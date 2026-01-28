from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os
import uuid

app = Flask(__name__)import os
from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.lower().endswith(".pdf"):
            return "Please upload a valid PDF file.", 400

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_name = f"fixed-{uuid.uuid4().hex}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        with open(output_path, "wb") as f:
            writer.write(f)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


UPLOAD_FOLDER = "uploads"
FIXED_FOLDER = "fixed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FIXED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    download_file = None

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            message = "❌ Please upload a PDF file."
            return render_template("index.html", message=message)

        if not file.filename.lower().endswith(".pdf"):
            message = "❌ Only PDF files are supported."
            return render_template("index.html", message=message)

        # Save uploaded file
        unique_name = f"{uuid.uuid4()}.pdf"
        input_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(input_path)

        # Rebuild PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        fixed_name = "fixed_" + file.filename
        output_path = os.path.join(FIXED_FOLDER, fixed_name)

        with open(output_path, "wb") as f:
            writer.write(f)

        message = "✅ File rebuilt successfully. Click below to download."
        download_file = fixed_name

    return render_template(
        "index.html",
        message=message,
        download_file=download_file
    )

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(FIXED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
