'''
Project:    CS50 Week 10
Author:     Regina Chua
Note:       This project will basically run pylette in a flask web app.
References: 
https://github.com/qTipTip/Pylette
https://pytutorial.com/how-to-solve-modulenotfounderror-no-module-named-in-python/
https://stackoverflow.com/questions/75404012/how-can-i-use-colorthief-to-obtain-the-dominant-color-of-multiple-images
'''

# Import modules
from flask import Flask, render_template, request, redirect, url_for, send_file
#from pylette import Palette #this did not work
#from PIL import Image #dependency for pylette
from colorthief import ColorThief
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import io

# App setup
app = Flask(__name__)

# FUNCTIONS ---

# adjust text color to brightness
def get_text_color(hex_color):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#FFFFFF" if brightness < 128 else "#000000"

# get color palette from an image URL
def get_color_palette(url, color_count=5):
    try:
        response = requests.get(url)
        
        # Handling invalid URLs
        response.raise_for_status()

        # Get image and apply color thief
        img = BytesIO(response.content)
        color_thief = ColorThief(img)

        # Get palette and hex code
        palette = color_thief.get_palette(color_count=color_count)
        #hex_palette = [{'color': '#{:02x}{:02x}{:02x}'.format(r, g, b), 
        #                'text_color': get_text_color('#{:02x}{:02x}{:02x}'.format(r, g, b))}
        #                for r, g, b in palette]
        hex_palette = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in palette]

        return hex_palette

    # White palette if error
    except requests.exceptions.RequestException:
        return["#FFFFFF"] * color_count


# Homepage
@app.route("/", methods=['GET', 'POST'])
def home():
    colors = None
    if request.method == 'POST':
        image_url = request.form['image_url']
        colors = get_color_palette(image_url)
    colors_str = ','.join(colors) if colors else None
    return render_template('index.html', colors=colors, colors_str=colors_str)

# Download
@app.route("/download_palette")
def download_palette():
    colors = request.args.get('colors').split(',')
    block_size = (100, 150)
    image_width = block_size[0] * len(colors)
    image_height = block_size[1]
    img = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(img)

    # Font setup
    try:
        font = ImageFont.truetype("roboto.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for i, hex_color in enumerate(colors):
        color_block = (i * block_size[0], 0, (i+1) * block_size[0], block_size[0])
        draw.rectangle(color_block, fill=hex_color)

        # Hex code under color
        text_position = (i * block_size[0] + 10, block_size[0] + 10)
        draw.text(text_position, hex_color, fill="black" if hex_color > "#7f7f7f" else "white", font=font)

    # Save to an object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="palette.png")


if __name__ == "__main__":
    app.run(debug=True)