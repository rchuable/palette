# PALETTE EXTRACTOR
#### Video Demo:  https://www.youtube.com/watch?v=8td-xT_DF4w&t
#### Description: 
Palette Extractor is a web-based application I designed to help artists like myself along with designers and basically anyone interested in color theory to extract a palette. The palettes extracted through this tool contain between two to give dominant colors measured by frequency from any image URL. This application is built with Flask, a lightweight web framework for Python, and utilizes the Color Thief library to analyze images and extract the most prominent colors. Each color in the palette is accompanied by its hex code, which can be downloaded as an image file or saved online with a free account, to make it easy to use in digital projects. Why did I use Color Thief instead of Pylette? Simply, Pylette wasn't working for my script ¯\_(ツ)_/¯

The primary goal of Palette Extractor is to simplify the process of color extraction and provide user-friendly interface for users like me to interact with. Whether you're working on digital art, web design, or any other creative project, this application makes it easy to identify and use the colors of an image that inspires you. By simply entering an image URL, users can quickly generate an image preview, a palette of dominant colors, and the palette's hex codes for easy reference.

In terms of functionality, Palette Extractor offers a range of features designed to make color extraction simple and efficient:
- **Accepts Image URLs as Input**: Users can input any image URL to extract colors from the image.
- **Extracts a Color Palette**: The application can generate a palette containing two to five colors, depending on what's available or extractable in the linked image.
- **Displays Hex Codes**: Each color in the palette is displayed with its corresponding hex code, which is essential for accurate color picking in digital art and design.
- **Simple and Clean UI**: The user interface is designed to be intuitive and easy to navigate.
- **Download Palette as Image**: Users can optionally download the extracted palette as a PNG image for easy reference and use in other applications.
- **Save and View Palettes**: With a free account, registered users can save their palettes, name their palettes, and view them later. This is the recommended option to save precious storage space and organize palette references. This is also particularly useful for those who work on multiple projects and need to keep track of different color schemes.

In terms of file contents, here's a breakdown of what each file contains and does:
- **app.py**: This is the main application file that sets up the Flask app, initializes the database, and defines the routes for the application. It includes functions for user registration, login, logout, and handling the core functionality of extracting an displaying color palettes. It also includes some of my references as I was developing this script along with citations of when I had assistance reviewing the code from ChatGPT and Copilot.
- **clear_db.py**: This file "nukes" my databases for the demonstration. It just clears up the tables.
- **requirements.txt**: This file lists the dependencies required for the application. It includes flask, colorthief, pillow, flask-login, flask_sqlalchemy, and Flask-Migrate. This makes sure that, when a virtual environment is set up to run this app, the necessary libraries are installed and available to be imported. I highly encourage using a virtual environment to keep things organized and to isolate any bugs that may arise from changes in the package versions.
- **templates/**: This directory folder contains the HTML templates for the palette extractor application. Each template corresponds to a different page or component of the application, such as the base (navigation), homepage, registration page, login page, and saved palettes page.
    - **base.html**: The template for the navigation bar that lets you maneuver around the application's other routes and pages. It can be found across all the pages.
    - **index.html**: The template for the homepage where users can input an image URL to extract a color palette, preview the image, copy the hex codes, download the color palette, and save the color palette.
    - **login.html**: The template for the login page where registered user can log in their account to access saved palettes. Alternatively, if an unauthenticated user attempts to save an extracted palette, the user will be redirected here to login. That saved palette will be automatically saved to their account since it can pull the data from the current session.
    - **register.html**: If a user does not have a login, the user is encouraged to go here. The template for the registration page where users can create a free, new account to access saved palettes.
    - **view_palettes.html**: The template for the page where authenticated and logged in users can view their saved palettes, download those saved palettes, or delete saved palettes they no longer need.
- **static/**: This directory contains static files such as CSS files.
	- **style.css**: The main CSS file that defines the styles for the application to make sure my application follows a consistent and visually appealing design. Ah, this takes me back to Gaia Online days.
- **__pycache__**: These folders (standalone, within `migrations`, and within `versions`) all simply store compiled Python bytecode files, which help the application run faster by simply reusing these cached files. For example, `app.cpython-312.pyc` is a cached compiled file for the main app to make the application launch faster.
- **images**: This folder contains an image asset for my project. It holds `palette-extractor-1.jpg` to present a screenshot of what the homepage of the app looks like for the `README` file.
- **instance**: This folder stores database file `users.db` where sensitive and instance-specific data goes.
- **migrations**: This folder contains database migration files for tracking schema changes in the database. Files inside help version control for the database structure.
- **alembic.ini** and **script.py.mako**: These are configuration files for Alembic, a tool that manages and applies database migrations.

Now let's talk about **design choices**.
Rather than uploading images, I chose to extract via URL to encourage artists to save their references online rather than locally. As you create more and more digital art pieces, you use up more storage space and that also leads to clutter in your machine. It is more streamlined to do things online and save references on the cloud, whether that's an image-storing service like Google Photos or an image-curating service like Pinterest. I also chose to use image URLs because, if an artist has blocked their image from being downloaded, I believe you need to respect the implicit "please don't use my art or images without permission" request from the creator; don't just screenshot and grab the image.

I chose the Flask framework for its simplicity and flexibility. It was introduced in Week 9 and, while I found it challenging at first, it's been a go-to for me now when thinking about containerization and building web-based application. It's like the first time I learned about streamlit for lightweight dashboard prototyping.

As mentioned earlier, I opted for the Color Thief library over Pylette simply because it worked. It extracted dominant colors from images very accurately and it's efficient and easy to use.

For users and saved palette management, using a combination of Flask-login with SQLite database were sufficient for the needs of this application. I wanted it to be usable even without a login but very easy to store and track palettes if a user chose to create an account. It made for a seamless user experience.

**A few more thoughts...**
Overall, I just wanted to create a simple app for my simple need: getting color palettes from reference images. While it has a simple utility, it is far from simple. It was rather complex to set everything up, but I'm happy to see it in a functional and streamlined state. One day, I hope to get this on its on webpage or integrated in a bigger software product that I'll make. It's an exciting opportunity ahead!


Created to complete https://cs50.harvard.edu/x/2024/project/

![Screenshot](images/palette-extractor-1.jpg)

## Author's (or Artist's) Note
The artwork shown in the example is my own. I built this app so that I could link reference images which had colors that I liked. The palette extractor helps me build gradient maps for digital art so it's easier to adjust the tones and hues of an illustration. I hope that this simple tool will help other artists and designers.

## Features
- Accepts image URLs as input
- Generates a color palette (2-5 colors)
- Displays hex codes for each color
- Simple and clean UI
- Option to download the palette as an image
- Save and view palettes with a free account

## Technologies Used
- Flask: Web framework
- Color Thief: Extracts dominant colors
- HTML/CSS: Front-end styling

## Setup
### Prerequisites
- Python 3.7+
- pip

### Installation
1. Clone the repository:
```
git clone https://github.com/rchuable/palette.git
cd palette
```
2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virual environment
- On Windows: 
```
venv\Scripts\activate
``` 
or 
```
./venv/Scripts/activate
```
- On macOS/Linux: 
```
source venv/bin/activate
```
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Set up the database:
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
6. Run the application:
```
flask run
```
7. Open the application in your browser:
Go to `http://127.0.0.1:5000`

## License
This project is licensed under the MIT License. See LICENSE for more information.