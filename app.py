from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfReader, PdfWriter
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
FIXED_FOLDER = "fixed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FIXED_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename.lower().endswith(".pdf"):
            message = "Please upload a valid PDF file."
            return render_template("index.html", message=message)

        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
        file.save(input_path)

        # Rebuild PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_path = os.path.join(FIXED_FOLDER, "fixed_" + file.filename)

        with open(output_path, "wb") as f:
            writer.write(f)

        message = "✅ File rebuilt successfully. If your upload failed before, try this version."

        return send_file(output_path, as_attachment=True)

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
