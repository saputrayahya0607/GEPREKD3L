from flask import Flask, render_template, session, redirect, url_for, request
import json

app = Flask(__name__)
app.secret_key = 'ini_rahasia'

# Load menu dari JSON
def load_menu():
    with open('data/menu.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    items = load_menu()
    return render_template('menu.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"[Kritik & Saran] Dari: {name}, Email: {email}, Pesan: {message}")
        return redirect(url_for('contact'))
    else:
        return render_template('contact.html')

# Tambah item ke keranjang
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form['item']
    price = int(request.form['price'])

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Tambah qty jika sudah ada item yang sama
    for cart_item in cart:
        if cart_item['item'] == item and cart_item['price'] == price:
            cart_item['qty'] += 1
            break
    else:
        # Tambahkan item baru
        cart.append({'item': item, 'price': price, 'qty': 1})

    session['cart'] = cart
    return redirect(url_for('menu'))

# Halaman keranjang
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

# Hapus keranjang
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

# Tampilkan jumlah item di navbar
@app.context_processor
def inject_cart_count():
    return dict(cart_count=sum(item['qty'] for item in session.get('cart', [])))

if __name__ == '__main__':
    app.run(debug=True)
