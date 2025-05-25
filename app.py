from flask import Flask, render_template, abort, request, url_for, flash, redirect, jsonify, send_file, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import io
from urllib.parse import unquote

app = Flask(__name__)

# grabbing key from file was acting stupid...this fixes it,
# as it was expecting bytes and not reading straight from the file
with open('secret_key.txt', 'rb') as file:
    myKey = file.read()

app.secret_key = myKey  

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database functions
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_product(prod_id):
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE _price = ?',
                        (prod_id,)).fetchone()
    conn.close()
    if products is None:
        abort(404)
    return products

# Dummy user store // CHANGE LATER
users = {'admin': {'password': 'password123'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# ************ Home ************
@app.route('/')
def homepage():
    # Placeholder for products, replace with DB query later
    products = [
        {'name': 'Product 1', 'image': 'static/photos/products/', 'description': 'Description 1'},
        {'name': 'Product 2', 'image': 'static/photos/products/', 'description': 'Description 2'},
        {'name': 'Product 3', 'image': 'static/photos/products/', 'description': 'Description 3'},
    ]
    return render_template('home.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

# ************ Products ************
@app.route('/product_image/<int:product_id>')
def product_image(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT _image FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if product and product['_image']:
        return send_file(
            io.BytesIO(product['_image']),
            mimetype='image/jpeg'
        )
    else:
        # Return a placeholder image if not found
        return send_file('static/photos/products/placeholder.jpg', mimetype='image/jpeg')
    
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return render_template('product_detail.html', product=product)

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

# ************ Authentication ************
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            flash('Invalid credentials, try again!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.id}! This is a protected page.'

# ************ error handling, yeah! ************
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_unavailable(error):
    return render_template('500.html'), 500

""" 
TODO: 
- Add favicon https://www.w3schools.com/howto/howto_html_favicon.asp#:~:text=A%20favicon%20is%20a%20small,simple%20image%20with%20high%20contrast.
"""