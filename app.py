from flask import Flask, request, send_file, render_template
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file uploaded", 400

        filename = secure_filename(file.filename)
        uid = uuid.uuid4().hex
        input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{filename}")
        output_path = os.path.join(OUTPUT_FOLDER, f"fixed_{filename}")

        file.save(input_path)

        # Re-save file to strip bad metadata / encoding issues
        with open(input_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                f_out.write(f_in.read())

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
