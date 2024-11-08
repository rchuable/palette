'''
Project:    CS50 Week 10
Author:     Regina Chua
Note:       This project will basically run color thief in a flask web app with
            added dynamic display and download functionality.
References: 
https://github.com/qTipTip/Pylette
https://pytutorial.com/how-to-solve-modulenotfounderror-no-module-named-in-python/
https://stackoverflow.com/questions/75404012/how-can-i-use-colorthief-to-obtain-the-dominant-color-of-multiple-images
'''

# Import modules
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from colorthief import ColorThief
import requests
import io
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# App setup & initialize Database
app = Flask(__name__)
app.config['SECRET_KEY'] = '@itsameregiC!369damnshefine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# SQL tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    palettes = db.relationship('Palette', backref='owner', lazy=True)

class Palette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    colors = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# After initializing
migrate = Migrate(app, db)

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
        response.raise_for_status()

        # Get image and apply color thief
        img = BytesIO(response.content)
        color_thief = ColorThief(img)

        # Get palette and hex code
        palette = color_thief.get_palette(color_count=color_count)
        hex_display = [{'color': '#{:02x}{:02x}{:02x}'.format(r, g, b), 
                        'text_color': get_text_color('#{:02x}{:02x}{:02x}'.format(r, g, b))}
                        for r, g, b in palette]
        hex_download = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in palette]
        
        return hex_display, hex_download
    
    # Handling palette errors
    except requests.exceptions.RequestException:
        hex_display = [{'color': '#FFFFFF', 'text_color': "#000000"}] * color_count
        hex_download = ["#FFFFFF"] * color_count
        return hex_display, hex_download


# Registration
# look at this security! I'm using hashed passwords :)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            # Redirect to saved palettes
            if 'colors' in session and 'name' in session:
                return redirect(url_for('complete_save_palette'))
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Homepage
@app.route("/", methods=['GET', 'POST'])
def home():
    colors_display = None
    colors_download = None
    if request.method == 'POST':
        image_url = request.form['image_url']
        colors_display, colors_download = get_color_palette(image_url)
    colors_str = ','.join(colors_download) if colors_download else None
    return render_template('index.html', colors=colors_display, colors_str=colors_str)

# Download
@app.route("/download_palette")
def download_palette():
    colors = request.args.get('colors').split(',')
    filename = request.args.get('filename', 'palette')
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
        color_block = (i * block_size[0], 0, (i+1) * block_size[0], block_size[1])
        draw.rectangle(color_block, fill=hex_color)

        # Hex code under color
        text_position = (i * block_size[0] + 10, block_size[1] - 20)
        draw.text(text_position, hex_color, fill=get_text_color(hex_color), font=font)

    # Save to an object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png", as_attachment=True, download_name=f"{filename}.png")

# Save
@app.route("/save_palette", methods=['POST'])
def save_palette():
    if not current_user.is_authenticated:
        session['colors'] = request.form['colors']
        session['name'] = request.form['name']
        flash('Please log in to save your palette.', 'info')
        return redirect(url_for('login'))

    if request.method == 'POST':
        colors = session.pop('colors', request.form['colors'])
        name = session.pop('name', request.form['name'])
    else:
        colors = session.get('colors')
        name = session.get('name')

    new_palette = Palette(name=name, colors=colors, owner=current_user)
    db.session.add(new_palette)
    db.session.commit()
    flash('Palette saved successfully! Go to My Palettes to view.', 'success')
    return redirect(url_for('home'))

# Save (from login)
@app.route("/complete_save_palette")
@login_required
def complete_save_palette():
    colors = session.pop('colors', None)
    name = session.pop('name', None)
    if colors and name:
        new_palette = Palette(name=name, colors=colors, owner=current_user)
        db.session.add(new_palette)
        db.session.commit()
        flash('Palette saved successfully!', 'success')
    return redirect(url_for('home'))

# View saved palettes
@app.route('/view_palettes')
@login_required
def view_palettes():
    palettes = Palette.query.filter_by(user_id=current_user.id).all()

    for palette in palettes:
        colors_with_text = [
            {'color': hex_color, 'text_color': get_text_color(hex_color)}
            for hex_color in palette.colors.split(',')
        ]
        palette.colors_with_text = colors_with_text

    return render_template('view_palettes.html', palettes=palettes)

# Delete palettes
@app.route('/delete_palette/<int:palette_id>')
@login_required
def delete_palette(palette_id):
    palette = Palette.query.get_or_404(palette_id)
    if palette.owner != current_user:
        abort(403)
    db.session.delete(palette)
    db.session.commit()
    return redirect(url_for('view_palettes'))


if __name__ == "__main__":
    app.run(debug=True)