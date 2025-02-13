from flask import Flask, request, render_template, jsonify
from PIL import Image
import piexif
import io

app = Flask(__name__)


def extract_metadata(image_file):
    """Extract metadata from a PNG or JPG file"""
    try:
        image = Image.open(image_file)
        metadata = {}

        # Extract text-based metadata (if stored in PNG tEXt or EXIF)
        if "png" in image.format.lower():
            metadata = image.info  # PNG metadata
        elif "jpeg" in image.format.lower():
            exif_data = piexif.load(image.info["exif"]) if "exif" in image.info else {}
            metadata = {
                k: v.decode() if isinstance(v, bytes) else v
                for k, v in exif_data.get("Exif", {}).items()
            }

        return metadata
    except Exception as e:
        return {"error": str(e)}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image_file = request.files["image"]
    metadata = extract_metadata(image_file)

    return jsonify({"metadata": metadata})


if __name__ == "__main__":
    app.run(debug=True)
