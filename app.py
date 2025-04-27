from flask import Flask, render_template, abort, request, url_for, flash, redirect

app = Flask(__name__)

# TODO: create 404 template
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

'''
@app.errorhandler(500)
def page_unavailable(error):
    return render_template('500.html'), 500
'''

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/')
# def ():

# DEBUG!!
'''
if __name__ == "__main__":
    app.run(debug=True)
'''