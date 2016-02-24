"""DPLAfest 2016 Presentation Website"""
__author__ = "Jeremy Nelson"

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/slide/")
@app.route("/slide/<number>")
def show_slide(number=None):
    if not number:
        return render_template("slides/index.html")
    return render_template("slides/{}.html".format(number))

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20161, debug=True)
