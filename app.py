from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample product data
products = [
    {'id': 1, 'name': 'Moter bike 1', 'price': 10000.00},
    {'id': 2, 'name': 'Moter bike 2', 'price': 15000.00},
    {'id': 3, 'name': 'Moter bike 3', 'price': 20000.00},
    {'id': 4, 'name': 'Moter bike 4', 'price': 25000.00},
    {'id': 5, 'name': 'Moter bike 5', 'price': 30000.00}
]

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [p for p in cart if p['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
