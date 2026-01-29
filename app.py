from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", tool=None)

@app.route("/too-large", methods=["GET", "POST"])
def too_large():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file uploaded", 400

        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output = io.BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="fixed.pdf"
        )

    return render_template("index.html", tool="too-large")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
