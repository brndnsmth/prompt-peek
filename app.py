import os
import argparse
import requests
from flask import Flask, request, render_template, jsonify
from PIL import Image
import piexif
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def download_image(image_url):
    """Download image from a URL synchronously and return the file path."""
    filename = secure_filename(image_url.split("/")[-1])
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        resp = requests.get(image_url, stream=True)
        if resp.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            return file_path
    except Exception as e:
        print(f"Error downloading image: {e}")

    return None


def extract_metadata(image_path):
    """Extract metadata from a PNG or JPG file"""
    metadata = {}

    try:
        with Image.open(image_path) as image:
            if image.format.lower() == "png":
                metadata = image.info
            elif image.format.lower() == "jpeg":
                exif_data = piexif.load(image.info.get("exif", b""))
                metadata = {
                    k: v.decode() if isinstance(v, bytes) else v
                    for k, v in exif_data.get("Exif", {}).items()
                }
    except Exception as e:
        metadata["error"] = str(e)

    return metadata


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handles both file upload and URL-based image processing"""
    file = request.files.get("image")
    image_url = request.form.get("image_url")
    image_path = None

    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)
    elif image_url:
        image_path = download_image(image_url)

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Invalid image or failed to process."}), 400

    metadata = extract_metadata(image_path)
    os.remove(image_path)  # Clean up

    return jsonify({"metadata": metadata})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 5000)),
        help="Port number to run the app",
    )
    args = parser.parse_args()
    app.run(debug=True, host="0.0.0.0", port=args.port)
