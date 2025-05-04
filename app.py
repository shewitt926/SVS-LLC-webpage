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
def homepage():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

""" 
TODO: 
- Facebook fetcher
- Add favicon https://www.w3schools.com/howto/howto_html_favicon.asp#:~:text=A%20favicon%20is%20a%20small,simple%20image%20with%20high%20contrast.
- Refine pages
"""