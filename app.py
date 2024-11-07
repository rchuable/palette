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
from flask import Flask, render_template, request, redirect, url_for
#from pylette import Palette
#from PIL import Image
from colorthief import ColorThief
import requests
from io import BytesIO

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
        hex_palette = [{'color': '#{:02x}{:02x}{:02x}'.format(r, g, b), 
                        'text_color': get_text_color('#{:02x}{:02x}{:02x}'.format(r, g, b))}
                        for r, g, b in palette]
        #hex_palette = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in palette]

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
    
    return render_template('index.html', colors=colors)

if __name__ == "__main__":
    app.run(debug=True)