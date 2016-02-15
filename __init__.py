"""DPLAfest 2016 Presentation Website"""
__author__ = "Jeremy Nelson"

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20161, debug=True)
