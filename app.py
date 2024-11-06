'''
Project:    CS50 Week 10
Author:     Regina Chua
Note:       This project will basically run pylette in a flask web app.
'''

# Import modules
import requests
from flask import Flask, render_template, request, redirect, url_for
from pylette import Palette
from io import BytesIO
from PIL import Image

# App setup
app = Flask(__name__)

# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Extractor
@app.route("/extract_palette", methods=["POST"])
def extract_palette():
    image_url = request.form.get("image_url")

    if not image_url:
        flash("Please provide an image URL.")
        return redirect(url_for("index"))

    # Download the image from the URL
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        flash("Could not load image from URL.")
        return redirect(url_for("index"))
    
    # Extract with Pylette
    palette = Palette(image)
    colors = palette.colors[:5] # Only top 5

    # Sort colors by brightness
    colors = sorted(colors, key=lambda color: color.brightness)

    # Convert colors to hex
    hex_colors = [color.hex_format() for color in colors]

    return render_template("palette.html", hex_colors=hex_colors)


if __name__ == "__main__":
    app.run(debug=True)