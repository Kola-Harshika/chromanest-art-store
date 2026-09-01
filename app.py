# -*- coding: utf-8 -*-
"""
CHROMANEST - Modern Art Store E-Commerce
Flask Backend Application with SQLite Database, User Authentication,
Customer Account Management, and Admin Dashboard.
"""

import os
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify
)
from werkzeug.security import check_password_hash
import database

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY')

# Initialize database tables & seed data on startup
database.init_db()

# -----------------------------------------------------------------------------
# AUTHENTICATION & ACCESS DECORATORS
# -----------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Admin authentication required.', 'error')
            return redirect(url_for('admin_login', next=request.url))
        user = database.get_user_by_id(user_id)
        if not user or user['role'] != 'admin':
            flash('Unauthorized access. Admin privileges required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------------------------------------------
# CONTEXT PROCESSORS (SUPPLY GLOBAL VARIABLES TO ALL TEMPLATES)
# -----------------------------------------------------------------------------

@app.context_processor
def inject_global_data():
    user = None
    if session.get('user_id'):
        user = database.get_user_by_id(session['user_id'])
    return {
        'current_user': user,
        'active_category': request.args.get('category', 'All')
    }

# -----------------------------------------------------------------------------
# STOREFRONT PAGES
# -----------------------------------------------------------------------------

@app.route('/')
def home():
    """Renders the Home page."""
    featured_products = database.get_all_products(include_out_of_stock=False)[:8]
    return render_template('index.html', featured_products=featured_products)

@app.route('/shop')
def shop():
    """Renders the Shop product gallery catalog."""
    category = request.args.get('category', 'All')
    products = database.get_all_products(category=category, include_out_of_stock=True)
    return render_template('shop.html', products=products, category=category)

@app.route('/product')
def product():
    """Renders the single Product details page."""
    product_id = request.args.get('id', 'paint-01')
    p = database.get_product_by_id(product_id)
    if not p:
        p = database.get_all_products()[0]
    return render_template('product.html', product=p)

@app.route('/cart')
def cart():
    """Renders the Shopping Cart page."""
    return render_template('cart.html')

@app.route('/about')
def about():
    """Renders the About page."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Renders the Contact, Inquiries, and FAQ page."""
    return render_template('contact.html')

@app.route('/wishlist')
def wishlist():
    """Wishlist convenience route."""
    return render_template('shop.html', view_mode='wishlist')

# -----------------------------------------------------------------------------
# CUSTOMER AUTHENTICATION ROUTES
# -----------------------------------------------------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Customer registration."""
    next_url = request.args.get('next', '')
    if session.get('user_id'):
        return redirect(url_for('profile'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/signup.html', next_url=next_url)

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('auth/signup.html', next_url=next_url)

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/signup.html', next_url=next_url)

        user_id = database.create_user(name, email, password, role='customer')
        if not user_id:
            flash('An account with this email already exists. Please log in.', 'error')
            return render_template('auth/signup.html', next_url=next_url)

        # Log in newly registered user
        session['user_id'] = user_id
        session['user_name'] = name
        session['user_role'] = 'customer'
        flash('Welcome to CHROMANEST! Your account has been created.', 'success')

        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('profile'))

    return render_template('auth/signup.html', next_url=next_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login."""
    next_url = request.args.get('next', '')
    if session.get('user_id'):
        user = database.get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('profile'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = database.get_user_by_email(email)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid email or password. Please try again.', 'error')
            return render_template('auth/login.html', next_url=next_url)

        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_role'] = user['role']

        flash(f"Welcome back, {user['name'].split()[0]}!", 'success')

        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))

        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('profile'))

    return render_template('auth/login.html', next_url=next_url)

@app.route('/logout')
def logout():
    """Clears user session."""
    session.clear()
    flash('You have been logged out securely.', 'success')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Customer account profile & address editor."""
    user_id = session['user_id']
    user = database.get_user_by_id(user_id)

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            name = request.form.get('name', '').strip()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            city = request.form.get('city', '').strip()
            postal_code = request.form.get('postal_code', '').strip()

            database.update_user_profile(user_id, name, phone, address, city, postal_code)
            session['user_name'] = name
            flash('Profile information saved successfully.', 'success')
            return redirect(url_for('profile'))

        elif action == 'change_password':
            new_pass = request.form.get('new_password', '')
            confirm_pass = request.form.get('confirm_password', '')

            if not new_pass or new_pass != confirm_pass or len(new_pass) < 6:
                flash('Passwords must match and have at least 6 characters.', 'error')
            else:
                database.update_user_password(user_id, new_pass)
                flash('Password updated successfully.', 'success')
            return redirect(url_for('profile'))

    return render_template('customer/profile.html')

@app.route('/orders')
@app.route('/my-orders')
@login_required
def customer_orders():
    """Customer order history page."""
    user_id = session['user_id']
    orders = database.get_orders_by_user_id(user_id)
    return render_template('customer/orders.html', orders=orders)

# -----------------------------------------------------------------------------
# CHECKOUT & ORDER CONFIRMATION
# -----------------------------------------------------------------------------

@app.route('/checkout')
def checkout():
    """Renders the checkout page."""
    return render_template('checkout.html')

@app.route('/order-confirmation/<order_number>')
def order_confirmation(order_number):
    """Renders the order success receipt page."""
    order = database.get_order_by_number(order_number)
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('home'))
    return render_template('order_confirmation.html', order=order)

# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------

@app.route('/api/products', methods=['GET'])
def api_products():
    """Returns JSON list of products from SQLite."""
    category = request.args.get('category', 'All')
    products = database.get_all_products(category=category, include_out_of_stock=True)
    return jsonify(products)

@app.route('/api/products/<product_id>', methods=['GET'])
def api_single_product(product_id):
    """Returns single product JSON."""
    p = database.get_product_by_id(product_id)
    if not p:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(p)

@app.route('/api/orders/place', methods=['POST'])
def api_place_order():
    """Places an order into the SQLite database."""
    try:
        data = request.get_json() or {}
        items = data.get('items', [])
        if not items:
            return jsonify({'success': False, 'message': 'Cart is empty'}), 400

        user_id = session.get('user_id')
        customer_name = data.get('customer_name', 'Art Collector')
        customer_email = data.get('customer_email', 'collector@example.com')
        customer_phone = data.get('customer_phone', '')
        shipping_address = data.get('shipping_address', '')
        city = data.get('city', '')
        postal_code = data.get('postal_code', '')
        payment_method = data.get('payment_method', 'Credit / Debit Card (Simulated)')
        subtotal = data.get('subtotal', 0)
        shipping_fee = data.get('shipping_fee', 0)
        tax = data.get('tax', 0)
        total_amount = data.get('total_amount', 0)

        order_number = database.create_order(
            user_id=user_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            city=city,
            postal_code=postal_code,
            payment_method=payment_method,
            cart_items=items,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            tax=tax,
            total_amount=total_amount
        )

        return jsonify({'success': True, 'order_number': order_number})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# -----------------------------------------------------------------------------
# ADMIN PORTAL & DASHBOARD
# -----------------------------------------------------------------------------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin portal login."""
    if session.get('user_id'):
        user = database.get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = database.get_user_by_email(email)
        if not user or user['role'] != 'admin' or not check_password_hash(user['password_hash'], password):
            flash('Invalid admin credentials.', 'error')
            return render_template('admin/login.html')

        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_role'] = 'admin'
        flash('Admin authenticated successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/login.html')

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard overview."""
    stats = database.get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin product catalog table."""
    products = database.get_all_products(include_out_of_stock=True)
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_product_add():
    """Admin add new product."""
    if request.method == 'POST':
        product_id = request.form.get('id', '').strip()
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', 0)
        original_price = request.form.get('original_price', None)
        badge = request.form.get('badge', None)
        image = request.form.get('image', '/static/images/hero-art.jpg').strip()
        medium = request.form.get('medium', '').strip()
        dimensions = request.form.get('dimensions', '').strip()
        description = request.form.get('description', '').strip()
        details_text = request.form.get('details', '')
        details = [d.strip() for d in details_text.split('\n') if d.strip()]
        in_stock = 1 if request.form.get('in_stock') else 0

        database.create_product(
            product_id=product_id,
            title=title,
            category=category,
            price=price,
            original_price=original_price if original_price else None,
            badge=badge if badge else None,
            image=image,
            medium=medium,
            dimensions=dimensions,
            description=description,
            details=details,
            in_stock=in_stock
        )
        flash(f'Artwork "{title}" published successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', product=None)

@app.route('/admin/products/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def admin_product_edit(product_id):
    """Admin edit product."""
    product = database.get_product_by_id(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('admin_products'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', 0)
        original_price = request.form.get('original_price', None)
        badge = request.form.get('badge', None)
        image = request.form.get('image', '').strip()
        medium = request.form.get('medium', '').strip()
        dimensions = request.form.get('dimensions', '').strip()
        description = request.form.get('description', '').strip()
        details_text = request.form.get('details', '')
        details = [d.strip() for d in details_text.split('\n') if d.strip()]
        in_stock = 1 if request.form.get('in_stock') else 0

        database.update_product(
            product_id=product_id,
            title=title,
            category=category,
            price=price,
            original_price=original_price if original_price else None,
            badge=badge if badge else None,
            image=image,
            medium=medium,
            dimensions=dimensions,
            description=description,
            details=details,
            in_stock=in_stock
        )
        flash(f'Artwork "{title}" updated successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', product=product)

@app.route('/admin/products/delete/<product_id>', methods=['POST'])
@admin_required
def admin_product_delete(product_id):
    """Admin delete product."""
    database.delete_product(product_id)
    flash('Product removed from catalog.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/toggle-stock/<product_id>', methods=['POST'])
@admin_required
def admin_product_toggle_stock(product_id):
    """Toggle in_stock status."""
    database.toggle_product_stock(product_id)
    flash('Product stock status updated.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin customer orders table."""
    orders = database.get_all_orders()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def admin_order_status(order_id):
    """Updates order fulfillment status."""
    new_status = request.form.get('status', 'Pending')
    database.update_order_status(order_id, new_status)
    flash(f'Order #{order_id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin_orders'))

# -----------------------------------------------------------------------------
# 404 ERROR HANDLER
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    print("==================================================")
    print("🎨 CHROMANEST Modern Art Store is running!")
    print("🌐 Storefront: http://127.0.0.1:5000")
    print("🔑 Admin Portal: http://127.0.0.1:5000/admin/login")
    print("==================================================")
    app.run(debug=True, host='127.0.0.1', port=5000)
