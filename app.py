from flask import Flask, render_template, abort, request, url_for, flash, redirect

app = Flask(__name__)

# TODO: create 404 template
@app.errorhandler(404)
def page_not_found(error):
    return render_template(), 404

@app.route('/')
def home():
    return render_template('home.html')