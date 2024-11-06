'''
Project:    CS50 Week 10
Author:     Regina Chua
Note:       This project will basically run pylette in a flask web app.
'''

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image_url = request.form.get("image_url")
        return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)