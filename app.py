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
    
    return render_template('index.html', colors=colors)

if __name__ == "__main__":
    app.run(debug=True)