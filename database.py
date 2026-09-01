# -*- coding: utf-8 -*-
"""
CHROMANEST - SQLite Database Layer
Handles database schema, seeding, user accounts, products, and order management.
"""

import os
import json
import random
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromanest.db')

def get_db_connection():
    """Establishes a connection to the SQLite database with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """Initializes the database tables and seeds initial products and admin account."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer',
            phone TEXT,
            address TEXT,
            city TEXT,
            postal_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL,
            rating REAL DEFAULT 5.0,
            reviews_count INTEGER DEFAULT 0,
            badge TEXT,
            image TEXT NOT NULL,
            medium TEXT NOT NULL,
            dimensions TEXT NOT NULL,
            description TEXT NOT NULL,
            details_json TEXT NOT NULL DEFAULT '[]',
            in_stock INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            shipping_address TEXT NOT NULL,
            city TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            subtotal REAL NOT NULL,
            shipping_fee REAL NOT NULL,
            tax REAL NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )
    """)

    # 4. Order Items Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            image TEXT NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
        )
    """)

    conn.commit()

    # Seed Default Admin Account
    cursor.execute('SELECT id FROM users WHERE email = ?', ('admin@chromanest.com',))
    if not cursor.fetchone():
        admin_pass = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, ('Studio Administrator', 'admin@chromanest.com', admin_pass, 'admin'))

    # Seed Sample Customer Account
    cursor.execute('SELECT id FROM users WHERE email = ?', ('collector@chromanest.com',))
    if not cursor.fetchone():
        cust_pass = generate_password_hash('customer123')
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, phone, address, city, postal_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ('Art Collector', 'collector@chromanest.com', cust_pass, 'customer', '+1 555-0199', '742 Evergreen Terrace', 'Springfield', '97477'))

    # Seed Products if empty
    cursor.execute('SELECT COUNT(*) as count FROM products')
    count = cursor.fetchone()['count']
    if count == 0:
        seed_initial_products(cursor)

    conn.commit()
    conn.close()
    print('[*] SQLite Database initialized & seeded successfully.')

def seed_initial_products(cursor):
    """Seeds the 18 initial catalog items."""
    initial_products = [
        # --- PAINTINGS ---
        {
            "id": "paint-01",
            "title": "Ethereal Whispers",
            "category": "Paintings",
            "price": 280.0,
            "original_price": 320.0,
            "rating": 4.9,
            "reviews_count": 24,
            "badge": "Curator's Pick",
            "image": "/static/images/ethereal-whispers.jpg",
            "medium": "Oil & 24K Gold Leaf on Belgian Linen",
            "dimensions": "24 × 36 in (60 × 90 cm)",
            "description": "An evocative exploration of quiet twilight horizons. Layered glazes of amethyst, soft blush, and hand-applied 24K gold leaf reflect changing room light throughout the day, evoking serene stillness.",
            "details": ["Original 1-of-1 studio creation", "Finished with museum-grade protective UV varnish", "Includes signed Certificate of Authenticity", "Ready to hang with custom solid oak floater frame"],
            "in_stock": 1
        },
        {
            "id": "paint-02",
            "title": "Golden Horizon",
            "category": "Paintings",
            "price": 340.0,
            "original_price": 380.0,
            "rating": 5.0,
            "reviews_count": 19,
            "badge": "Bestseller",
            "image": "/static/images/golden-horizon.jpg",
            "medium": "Textured Heavy Acrylic & Gold Leaf on Gallery Canvas",
            "dimensions": "30 × 40 in (76 × 101 cm)",
            "description": "Rich sculptural impasto strokes capture the warmth of the setting sun over rugged earthen landscape silhouettes. The tactile texture creates depth and dynamic shadows.",
            "details": ["Heavy impasto palette knife technique", "Signature on lower right & reverse", "Includes Certificate of Authenticity", "Shipped in heavy-duty reinforced wooden crate"],
            "in_stock": 1
        },
        {
            "id": "paint-03",
            "title": "Serenade in Indigo",
            "category": "Paintings",
            "price": 220.0,
            "original_price": None,
            "rating": 4.8,
            "reviews_count": 15,
            "badge": "New Release",
            "image": "/static/images/serenade-indigo.jpg",
            "medium": "Deep Mineral Pigment Wash on 640gsm Cold-Press Paper",
            "dimensions": "20 × 28 in (50 × 70 cm)",
            "description": "Hypnotic layers of lapis lazuli and indigo wash fluidly into soft mist. The organic crystallization of pure raw pigments creates a celestial meditation on paper.",
            "details": ["Hand-deckled archival cotton rag paper", "Mounted behind anti-reflective museum glass", "Includes Certificate of Authenticity", "Signed and dated by the artist"],
            "in_stock": 1
        },
        {
            "id": "paint-04",
            "title": "Wild Botanical Bloom",
            "category": "Paintings",
            "price": 310.0,
            "original_price": 350.0,
            "rating": 5.0,
            "reviews_count": 18,
            "badge": "Limited Release",
            "image": "/static/images/wild-botanical-bloom.jpg",
            "medium": "Oil & Botanical Glazes on Heavy Belgian Canvas",
            "dimensions": "28 × 36 in (70 × 90 cm)",
            "description": "A lush, painterly floral masterpiece featuring soft blush peonies, garden roses, and eucalyptus sprigs emerging from deep moody forest tones with rich impasto textures.",
            "details": ["Original 1-of-1 studio floral composition", "Finished with protective museum satin varnish", "Includes signed Certificate of Authenticity", "Ready to hang in bespoke natural walnut floater frame"],
            "in_stock": 1
        },

        # --- RESIN ART ---
        {
            "id": "resin-01",
            "title": "Oceanic Geode Flow",
            "category": "Resin Art",
            "price": 195.0,
            "original_price": 230.0,
            "rating": 4.9,
            "reviews_count": 31,
            "badge": "Bestseller",
            "image": "/static/images/oceanic-geode.jpg",
            "medium": "Multi-Layer Crystal Epoxy Resin, Real Quartz & Sea Pigments",
            "dimensions": "20 × 20 in (50 × 50 cm)",
            "description": "Translucent aquatic depths blended with shimmering mica swirls and embedded natural raw quartz points. Captures the eternal dance between sea foam and coastal reef.",
            "details": ["High-gloss heat and scratch resistant topcoat", "Natural raw crushed quartz inclusions", "Solid birch wood substrate foundation", "Includes Certificate of Authenticity"],
            "in_stock": 1
        },
        {
            "id": "resin-02",
            "title": "Emerald Nebula Tray",
            "category": "Resin Art",
            "price": 145.0,
            "original_price": None,
            "rating": 4.9,
            "reviews_count": 18,
            "badge": "Handcrafted",
            "image": "/static/images/emerald-nebula.jpg",
            "medium": "Hand-Poured Artisan Resin with Brushed Brass Handles",
            "dimensions": "16 × 12 in (40 × 30 cm)",
            "description": "A functional art centerpiece featuring deep emerald green pigment currents interlaced with gold glitter veining and solid brushed brass hardware.",
            "details": ["Food-safe, scratch-resistant cured resin", "Heavy brushed solid brass handles", "Velvet padded bottom to protect furniture", "Care instructions included"],
            "in_stock": 1
        },
        {
            "id": "resin-03",
            "title": "Celestial Pearl Coasters",
            "category": "Resin Art",
            "price": 65.0,
            "original_price": 75.0,
            "rating": 4.7,
            "reviews_count": 42,
            "badge": "Set of 4",
            "image": "/static/images/celestial-pearl.jpg",
            "medium": "Mother-of-Pearl Inlay & Lavender Epoxy Resin Set",
            "dimensions": "4.5 in diameter (11.5 cm) each",
            "description": "A luxurious 4-piece coaster suite infused with iridescent shell fragments, subtle lavender mineral clouds, and hand-gilded gold leaf edges.",
            "details": ["Set of 4 individual coasters", "Heat-resistant up to 90°C (194°F)", "Hand-painted metallic gilded rim", "Gift-ready signature CHROMANEST linen box"],
            "in_stock": 1
        },

        # --- WALL ART ---
        {
            "id": "wall-01",
            "title": "Textured Terracotta Arcs",
            "category": "Wall Art",
            "price": 240.0,
            "original_price": 280.0,
            "rating": 5.0,
            "reviews_count": 27,
            "badge": "Trending",
            "image": "/static/images/textured-terracotta.jpg",
            "medium": "3D Plaster & Mineral Earth Pigments on Reinforced Panel",
            "dimensions": "24 × 32 in (60 × 80 cm)",
            "description": "Architectural minimalism meets Mediterranean warmth. Rhythmic raised concentric arcs create captivating three-dimensional shadows across minimalist living spaces.",
            "details": ["Sculpted dimensional plaster relief", "Natural organic matte finish", "Integrated heavy-duty hanging hardware", "Signed on reverse with edition stamp"],
            "in_stock": 1
        },
        {
            "id": "wall-02",
            "title": "Monochrome Rhythm",
            "category": "Wall Art",
            "price": 210.0,
            "original_price": None,
            "rating": 4.8,
            "reviews_count": 14,
            "badge": "Minimalist",
            "image": "/static/images/monochrome-rhythm.jpg",
            "medium": "Geometric Ash Wood Slats & Blackened Mineral Canvas",
            "dimensions": "28 × 28 in (70 × 70 cm)",
            "description": "A study in balance, symmetry, and negative space. Hand-finished charred ash wood segments intersect on a textured linen backboard.",
            "details": ["Solid sustainable kiln-dried ash wood", "Matte soot pigment wash", "Ultra-modern frameless aesthetic", "Includes mounting template"],
            "in_stock": 1
        },
        {
            "id": "wall-03",
            "title": "Gilded Botanical Relief",
            "category": "Wall Art",
            "price": 310.0,
            "original_price": 350.0,
            "rating": 4.9,
            "reviews_count": 19,
            "badge": "Limited Edition",
            "image": "/static/images/gilded-botanical.jpg",
            "medium": "Hand-Carved Bas-Relief with Antique Gold Leaf Patina",
            "dimensions": "22 × 34 in (56 × 86 cm)",
            "description": "Inspired by pressed heritage ferns and ancient herbal manuscripts. Delicate leaf veins are hand-carved in high relief and finished in aged gold patina.",
            "details": ["Hand-carved casting compound", "Distressed antique metallic leafing", "Encased in slim satin walnut shadowbox", "Certificate of Authenticity attached"],
            "in_stock": 1
        },

        # --- HANDMADE ---
        {
            "id": "hand-01",
            "title": "Sculpted Clay Muse Vase",
            "category": "Handmade",
            "price": 135.0,
            "original_price": 155.0,
            "rating": 4.9,
            "reviews_count": 38,
            "badge": "Studio Exclusive",
            "image": "/static/images/sculpted-clay-vase.jpg",
            "medium": "Wheel-Thrown Stoneware with Matte Raw Glaze",
            "dimensions": "11 × 7 in (28 × 18 cm)",
            "description": "Hand-sculpted organic silhouette inspired by classical Greek amphorae and modern brutalism. Each vessel bears subtle finger ridges from the potter's wheel.",
            "details": ["100% waterproof glazed interior", "Tactile raw sand exterior texture", "Individually hand-thrown in studio", "Artist studio stamp on base"],
            "in_stock": 1
        },
        {
            "id": "hand-02",
            "title": "Artisan Ceramic Vessel",
            "category": "Handmade",
            "price": 110.0,
            "original_price": None,
            "rating": 4.7,
            "reviews_count": 22,
            "badge": "Original",
            "image": "/static/images/artisan-ceramic-vessel.jpg",
            "medium": "Matte Charcoal Studio Stoneware with Speckled Lip",
            "dimensions": "9 × 6 in (23 × 15 cm)",
            "description": "A striking minimalist statement vessel with earthy charcoal tones and an asymmetrical organic mouth, celebrating the wabi-sabi beauty of imperfection.",
            "details": ["High-fire reduction stoneware", "Handmade in small batches", "Sturdy heavy-weight base", "Care booklet included"],
            "in_stock": 1
        },
        {
            "id": "hand-03",
            "title": "Handwoven Dune Tapestry",
            "category": "Handmade",
            "price": 175.0,
            "original_price": 200.0,
            "rating": 5.0,
            "reviews_count": 16,
            "badge": "Hand-Loomed",
            "image": "/static/images/woven-tapestry-dune.jpg",
            "medium": "Organic Merino Wool, Raw Flax Linen & Brass Bar",
            "dimensions": "18 × 36 in (45 × 90 cm)",
            "description": "Textured wall fiber art hand-loomed with undyed ethical wool and raw linen fibers. Inspired by shifting desert dunes and organic earthen topography.",
            "details": ["Spun from 100% cruelty-free merino wool", "Suspended on solid natural brass rod", "Subtle fringed bottom drape", "Comes ready to hang"],
            "in_stock": 1
        },

        # --- ART PRINTS ---
        {
            "id": "print-01",
            "title": "Sunlit Olive Grove",
            "category": "Art Prints",
            "price": 75.0,
            "original_price": 90.0,
            "rating": 4.8,
            "reviews_count": 52,
            "badge": "Archival Giclée",
            "image": "/static/images/sunlit-olive-grove.jpg",
            "medium": "Museum-Grade 310gsm 100% Cotton Rag Archival Giclée",
            "dimensions": "18 × 24 in (45 × 60 cm)",
            "description": "Dappled sunlight filtering through silvery Tuscan olive branches. Printed with 12-color archival pigment inks guaranteed to remain vibrant for over 100 years.",
            "details": ["Hahnemühle Photo Rag paper", "12-color pigment Lucia PRO ink", "Hand-embossed CHROMANEST seal", "Shipped flat in protective acid-free sleeve"],
            "in_stock": 1
        },
        {
            "id": "print-02",
            "title": "Abstract Fluidity No. 4",
            "category": "Art Prints",
            "price": 85.0,
            "original_price": None,
            "rating": 4.9,
            "reviews_count": 29,
            "badge": "Limited Edition",
            "image": "/static/images/abstract-fluidity.jpg",
            "medium": "Hand-Numbered Fine Art Lithograph on Textured Velvet Paper",
            "dimensions": "20 × 28 in (50 × 70 cm)",
            "description": "A dynamic composition of flowing mauve, plum, and warm ochre shapes. Part of an exclusive numbered edition of only 100 prints worldwide.",
            "details": ["Hand-numbered and pencil signed", "Certificate of Authenticity included", "Acid-free archival backing", "Fits standard gallery frames"],
            "in_stock": 1
        },
        {
            "id": "print-03",
            "title": "Midnight Flora Lithograph",
            "category": "Art Prints",
            "price": 65.0,
            "original_price": 80.0,
            "rating": 4.7,
            "reviews_count": 34,
            "badge": "Popular",
            "image": "/static/images/midnight-flora.jpg",
            "medium": "Embossed Midnight Blue & Silver Ink Botanical Print",
            "dimensions": "16 × 20 in (40 × 50 cm)",
            "description": "Botanical elegance captured in nocturnal tones. Silver metallic botanical silhouettes shimmer delicately over a deep navy velvety background.",
            "details": ["Double-hit metallic silver ink print", "Deckled bottom edge", "Archival matte paper", "Includes hanging guidelines"],
            "in_stock": 1
        },

        # --- CUSTOMIZED GIFTS ---
        {
            "id": "gift-01",
            "title": "Bespoke Couple Watercolor",
            "category": "Customized Gifts",
            "price": 185.0,
            "original_price": 220.0,
            "rating": 5.0,
            "reviews_count": 64,
            "badge": "Custom Commission",
            "image": "/static/images/custom-watercolor-gift.jpg",
            "medium": "Custom Hand-Painted Watercolor from Your Reference Photo",
            "dimensions": "12 × 16 in (30 × 40 cm)",
            "description": "Transform your favorite memory, wedding photo, or family moment into a luminous, expressive watercolor portrait handcrafted by our master illustrators.",
            "details": ["Custom painted directly from your photo", "Digital preview & approval before final varnishing", "Includes personalized calligraphy inscription", "Gift-boxed with luxury satin ribbon"],
            "in_stock": 1
        },
        {
            "id": "gift-02",
            "title": "Personalized Resin Plaque",
            "category": "Customized Gifts",
            "price": 125.0,
            "original_price": None,
            "rating": 4.9,
            "reviews_count": 47,
            "badge": "Personalized",
            "image": "/static/images/custom-resin-plaque.jpg",
            "medium": "Hand-Poured Botanical Resin with Custom Gilded Inscription",
            "dimensions": "10 × 10 in (25 × 25 cm)",
            "description": "Real pressed flowers, gold flakes, and crystal-clear resin cast around your custom names, anniversary dates, or meaningful vows.",
            "details": ["Custom laser-engraved or gilded script", "Preserved organic botanicals", "Includes solid wood tabletop display easel", "Turnaround time: 5-7 business days"],
            "in_stock": 1
        }
    ]

    for p in initial_products:
        cursor.execute("""
            INSERT INTO products (id, title, category, price, original_price, rating, reviews_count, badge, image, medium, dimensions, description, details_json, in_stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p['id'], p['title'], p['category'], p['price'], p['original_price'],
            p['rating'], p['reviews_count'], p['badge'], p['image'], p['medium'],
            p['dimensions'], p['description'], json.dumps(p['details']), p['in_stock']
        ))

# -----------------------------------------------------------------------------
# USER HELPERS
# -----------------------------------------------------------------------------

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE LOWER(email) = LOWER(?)', (email.strip(),)).fetchone()
    conn.close()
    return user

def create_user(name, email, password, role='customer', phone=None, address=None, city=None, postal_code=None):
    conn = get_db_connection()
    password_hash = generate_password_hash(password)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, phone, address, city, postal_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name.strip(), email.strip().lower(), password_hash, role, phone, address, city, postal_code))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def update_user_profile(user_id, name, phone, address, city, postal_code):
    conn = get_db_connection()
    conn.execute("""
        UPDATE users
        SET name = ?, phone = ?, address = ?, city = ?, postal_code = ?
        WHERE id = ?
    """, (name.strip(), phone, address, city, postal_code, user_id))
    conn.commit()
    conn.close()

def update_user_password(user_id, new_password):
    conn = get_db_connection()
    password_hash = generate_password_hash(new_password)
    conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------
# PRODUCT HELPERS
# -----------------------------------------------------------------------------

def get_all_products(category=None, include_out_of_stock=True):
    conn = get_db_connection()
    if category and category.lower() != 'all':
        if include_out_of_stock:
            query = 'SELECT * FROM products WHERE LOWER(category) = LOWER(?) ORDER BY created_at DESC'
            products = conn.execute(query, (category,)).fetchall()
        else:
            query = 'SELECT * FROM products WHERE LOWER(category) = LOWER(?) AND in_stock = 1 ORDER BY created_at DESC'
            products = conn.execute(query, (category,)).fetchall()
    else:
        if include_out_of_stock:
            products = conn.execute('SELECT * FROM products ORDER BY created_at DESC').fetchall()
        else:
            products = conn.execute('SELECT * FROM products WHERE in_stock = 1 ORDER BY created_at DESC').fetchall()
    conn.close()
    
    result = []
    for p in products:
        item = dict(p)
        try:
            item['details'] = json.loads(p['details_json'])
        except Exception:
            item['details'] = []
        result.append(item)
    return result

def get_product_by_id(product_id):
    conn = get_db_connection()
    p = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not p:
        return None
    item = dict(p)
    try:
        item['details'] = json.loads(p['details_json'])
    except Exception:
        item['details'] = []
    return item

def create_product(product_id, title, category, price, original_price=None, badge=None, image=None, medium=None, dimensions=None, description=None, details=None, in_stock=1):
    conn = get_db_connection()
    if not image:
        image = '/static/images/hero-art.jpg'
    details_json = json.dumps(details if isinstance(details, list) else [d.strip() for d in (details or '').split('\n') if d.strip()])
    
    conn.execute("""
        INSERT INTO products (id, title, category, price, original_price, badge, image, medium, dimensions, description, details_json, in_stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_id, title.strip(), category.strip(), float(price),
        float(original_price) if original_price else None,
        badge.strip() if badge else None,
        image.strip(),
        medium.strip() if medium else 'Original Studio Mixed Media',
        dimensions.strip() if dimensions else 'Standard Gallery Dimensions',
        description.strip() if description else 'Original handcrafted artwork from CHROMANEST Atelier.',
        details_json, int(in_stock)
    ))
    conn.commit()
    conn.close()
    return product_id

def update_product(product_id, title, category, price, original_price=None, badge=None, image=None, medium=None, dimensions=None, description=None, details=None, in_stock=1):
    conn = get_db_connection()
    details_json = json.dumps(details if isinstance(details, list) else [d.strip() for d in (details or '').split('\n') if d.strip()])
    
    conn.execute("""
        UPDATE products
        SET title = ?, category = ?, price = ?, original_price = ?, badge = ?, image = ?,
            medium = ?, dimensions = ?, description = ?, details_json = ?, in_stock = ?
        WHERE id = ?
    """, (
        title.strip(), category.strip(), float(price),
        float(original_price) if original_price else None,
        badge.strip() if badge else None,
        image.strip() if image else '/static/images/hero-art.jpg',
        medium.strip() if medium else 'Original Studio Mixed Media',
        dimensions.strip() if dimensions else 'Standard Gallery Dimensions',
        description.strip() if description else '',
        details_json, int(in_stock), product_id
    ))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

def toggle_product_stock(product_id):
    conn = get_db_connection()
    conn.execute('UPDATE products SET in_stock = CASE WHEN in_stock = 1 THEN 0 ELSE 1 END WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# -----------------------------------------------------------------------------
# ORDER HELPERS
# -----------------------------------------------------------------------------

def create_order(user_id, customer_name, customer_email, customer_phone, shipping_address, city, postal_code, payment_method, cart_items, subtotal, shipping_fee, tax, total_amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    order_number = f"CHR-{datetime.now().strftime('%y%m%d')}-{random.randint(1000, 9999)}"
    
    cursor.execute("""
        INSERT INTO orders (order_number, user_id, customer_name, customer_email, customer_phone, shipping_address, city, postal_code, payment_method, subtotal, shipping_fee, tax, total_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (
        order_number, user_id, customer_name.strip(), customer_email.strip().lower(),
        customer_phone, shipping_address.strip(), city.strip(), postal_code.strip(),
        payment_method, float(subtotal), float(shipping_fee), float(tax), float(total_amount)
    ))
    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, title, price, quantity, image, subtotal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, item['id'], item['title'], float(item['price']),
            int(item['quantity']), item.get('image', '/static/images/hero-art.jpg'),
            float(item['price']) * int(item['quantity'])
        ))

    conn.commit()
    conn.close()
    return order_number

def get_orders_by_user_id(user_id):
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
    
    result = []
    for o in orders:
        order_dict = dict(o)
        items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (o['id'],)).fetchall()
        order_dict['items'] = [dict(i) for i in items]
        result.append(order_dict)
    conn.close()
    return result

def get_all_orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    result = []
    for o in orders:
        order_dict = dict(o)
        items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (o['id'],)).fetchall()
        order_dict['items'] = [dict(i) for i in items]
        result.append(order_dict)
    conn.close()
    return result

def get_order_by_number(order_number):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE order_number = ?', (order_number,)).fetchone()
    if not order:
        conn.close()
        return None
    order_dict = dict(order)
    items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],)).fetchall()
    order_dict['items'] = [dict(i) for i in items]
    conn.close()
    return order_dict

def get_order_by_id(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order:
        conn.close()
        return None
    order_dict = dict(order)
    items = conn.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],)).fetchall()
    order_dict['items'] = [dict(i) for i in items]
    conn.close()
    return order_dict

def update_order_status(order_id, new_status):
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db_connection()
    total_products = conn.execute('SELECT COUNT(*) as c FROM products').fetchone()['c']
    total_orders = conn.execute('SELECT COUNT(*) as c FROM orders').fetchone()['c']
    total_revenue = conn.execute('SELECT COALESCE(SUM(total_amount), 0) as s FROM orders WHERE status != "Cancelled"').fetchone()['s']
    total_customers = conn.execute('SELECT COUNT(*) as c FROM users WHERE role = "customer"').fetchone()['c']
    in_stock_count = conn.execute('SELECT COUNT(*) as c FROM products WHERE in_stock = 1').fetchone()['c']
    pending_orders = conn.execute('SELECT COUNT(*) as c FROM orders WHERE status = "Pending"').fetchone()['c']
    recent_orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC LIMIT 5').fetchall()
    
    conn.close()
    return {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'in_stock_count': in_stock_count,
        'pending_orders': pending_orders,
        'recent_orders': [dict(o) for o in recent_orders]
    }

if __name__ == '__main__':
    init_db()
