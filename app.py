from flask import Flask, render_template, session, redirect, url_for, request, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ini_rahasia'

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Ganti dengan user MySQL Anda
    'password': '',  # Ganti dengan password MySQL Anda
    'database': 'D3L'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"DEBUG: Checking login for session user_id: {session.get('user_id')}")
        if 'user_id' not in session:
            print("DEBUG: User not logged in, redirecting to login")
            return redirect(url_for('login'))
        print("DEBUG: User logged in, proceeding to requested page")
        return f(*args, **kwargs)
    return decorated_function

# User registration
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)
#
#         connection = get_db_connection()
#         if connection is None:
#             flash('Database connection error')
#             return redirect(url_for('register'))
#
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
#         existing_user = cursor.fetchone()
#         if existing_user:
#             cursor.close()
#             connection.close()
#             flash('Username sudah digunakan')
#             return redirect(url_for('register'))
#
#         cursor.execute("INSERT INTO pengguna (username, password, created_at) VALUES (%s, %s, %s)",
#                        (username, hashed_password, datetime.now()))
#         connection.commit()
#         cursor.close()
#         connection.close()
#         flash('Registrasi berhasil, silakan login')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection is None:
            flash('Database connection error')
            return redirect(url_for('login'))

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pengguna WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(f"DEBUG: User fetched in login: {user}")
        if user:
            print(f"DEBUG: Stored password hash: {user['password']}")
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            print(f"DEBUG: User {user['username']} logged in successfully")
            return redirect(url_for('admin'))
        else:
            error = 'Username atau password salah'
            print(f"DEBUG: Login failed for user {username}")
            return render_template('login.html', error=error)
    return render_template('login.html')

# User logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Load menu from database
def load_menu():
    connection = get_db_connection()
    if connection is None:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    cursor.close()
    connection.close()
    return items

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

# Admin menu management page
@app.route('/admin')
@login_required
def admin():
    items = load_menu()
    # Debug print to check item ids
    for item in items:
        print(f"DEBUG: Menu item id: {item.get('id')}, nama: {item.get('nama')}")
    return render_template('admin.html', items=items)

import os
from werkzeug.utils import secure_filename

# Create new menu item
@app.route('/admin/create', methods=['GET', 'POST'])
@login_required
def admin_create():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        # Handle file upload
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'img', filename)
            file.save(upload_path)
        else:
            filename = None

        connection = get_db_connection()
        if connection is None:
            flash('Database connection error')
            return redirect(url_for('admin_create'))

        cursor = connection.cursor()
        cursor.execute("INSERT INTO menu (nama, harga, gambar) VALUES (%s, %s, %s)",
                       (name, price, filename))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('admin'))
    return render_template('admin_form.html', form_title='Tambah Menu Baru', form_action=url_for('admin_create'), submit_label='Tambah')

# Update menu item
@app.route('/admin/update/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_update(item_id):
    connection = get_db_connection()
    if connection is None:
        flash('Database connection error')
        return redirect(url_for('admin'))

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu WHERE id = %s", (item_id,))
    item = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        # Handle file upload
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('static', 'img', filename)
            file.save(upload_path)
        else:
            filename = item['gambar']  # Keep existing filename if no new file uploaded

        cursor.execute("UPDATE menu SET nama = %s, harga = %s, gambar = %s WHERE id = %s",
                       (name, price, filename, item_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('admin'))

    cursor.close()
    connection.close()
    return render_template('admin_form.html', form_title='Edit Menu', form_action=url_for('admin_update', item_id=item_id), submit_label='Update', item=item)

# Delete menu item
@app.route('/admin/delete/<int:item_id>')
@login_required
def admin_delete(item_id):
    connection = get_db_connection()
    if connection is None:
        flash('Database connection error')
        return redirect(url_for('admin'))

    cursor = connection.cursor()
    cursor.execute("DELETE FROM menu WHERE id = %s", (item_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('admin'))

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

def create_default_admin():
    connection = get_db_connection()
    if connection is None:
        print("Database connection error, cannot create default admin")
        return
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pengguna WHERE username = %s", ('admin',))
    user = cursor.fetchone()
    print(f"DEBUG: User fetched for default admin check: {user}")
    if not user:
        hashed_password = generate_password_hash('admin123')
        cursor.execute("INSERT INTO pengguna (username, password, created_at) VALUES (%s, %s, %s)",
                       ('admin', hashed_password, datetime.now()))
        connection.commit()
        print("Default admin user created with username 'admin' and password 'admin123'")
    else:
        print("Default admin user already exists")
    cursor.close()
    connection.close()

@app.route('/admin_user_edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit():
    error = None
    success = None
    username = ''
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username FROM pengguna WHERE id = %s", (session['user_id'],))
        row = cursor.fetchone()
        if row:
            username = row['username']
    except Exception as e:
        error = 'Gagal mengambil data admin.'

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        if not new_username or not new_password:
            error = 'Username dan password harus diisi.'
        else:
            try:
                hashed_password = generate_password_hash(new_password)
                cursor.execute("UPDATE pengguna SET username = %s, password = %s WHERE id = %s",
                               (new_username, hashed_password, session['user_id']))
                connection.commit()
                success = 'Data admin berhasil diperbarui.'
                username = new_username
            except Exception as e:
                error = 'Gagal memperbarui data admin.'
            finally:
                cursor.close()
                connection.close()

    return render_template('admin_user_edit.html', error=error, success=success, username=username)

if __name__ == '__main__':
    create_default_admin()
    app.run(debug=True)
