from flask import Flask, render_template, abort, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user store
users = {'admin': {'password': 'password123'}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# wanna see the webpage?
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

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

# error handling, yeah!
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_unavailable(error):
    return render_template('500.html'), 500

""" 
TODO: 
- Facebook fetcher
- Add favicon https://www.w3schools.com/howto/howto_html_favicon.asp#:~:text=A%20favicon%20is%20a%20small,simple%20image%20with%20high%20contrast.
"""