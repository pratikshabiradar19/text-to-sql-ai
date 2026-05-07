import sqlite3

# Connect to database (creates ecommerce.db file automatically)
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Create 3 tables
cursor.executescript("""

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT,
    city        TEXT,
    email       TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    price        REAL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    product_id   INTEGER,
    quantity     INTEGER,
    order_date   TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

""")

# Insert sample customers
customers = [
    (1, 'Priya Sharma',  'Mumbai',    'priya@gmail.com'),
    (2, 'Rahul Verma',   'Pune',      'rahul@gmail.com'),
    (3, 'Anita Patel',   'Delhi',     'anita@gmail.com'),
    (4, 'Suresh Kumar',  'Bangalore', 'suresh@gmail.com'),
    (5, 'Meena Joshi',   'Chennai',   'meena@gmail.com'),
    (6, 'Karan Mehta',   'Pune',      'karan@gmail.com'),
    (7, 'Sneha Kulkarni','Mumbai',    'sneha@gmail.com'),
]
cursor.executemany(
    "INSERT OR IGNORE INTO customers VALUES (?,?,?,?)",
    customers
)

# Insert sample products
products = [
    (1, 'iPhone 15',        'Electronics', 79999),
    (2, 'Samsung TV 55"',   'Electronics', 45000),
    (3, 'Nike Air Max',     'Footwear',     8999),
    (4, 'Levi Jeans 501',   'Clothing',     3499),
    (5, 'Boat Headphones',  'Electronics',  2999),
    (6, 'Adidas T-Shirt',   'Clothing',     1299),
    (7, 'HP Laptop',        'Electronics', 65000),
    (8, 'Woodland Boots',   'Footwear',     5499),
]
cursor.executemany(
    "INSERT OR IGNORE INTO products VALUES (?,?,?,?)",
    products
)

# Insert sample orders
orders = [
    (1,  1, 1, 1, '2024-01-15', 79999),
    (2,  2, 3, 2, '2024-01-18', 17998),
    (3,  3, 2, 1, '2024-02-01', 45000),
    (4,  4, 5, 3, '2024-02-10',  8997),
    (5,  5, 4, 2, '2024-02-14',  6998),
    (6,  1, 5, 1, '2024-03-01',  2999),
    (7,  2, 1, 1, '2024-03-15', 79999),
    (8,  3, 3, 1, '2024-03-20',  8999),
    (9,  6, 7, 1, '2024-04-05', 65000),
    (10, 7, 6, 3, '2024-04-10',  3897),
    (11, 4, 8, 1, '2024-04-22',  5499),
    (12, 5, 2, 1, '2024-05-01', 45000),
    (13, 6, 4, 2, '2024-05-10',  6998),
    (14, 7, 1, 1, '2024-05-18', 79999),
    (15, 1, 7, 1, '2024-06-01', 65000),
]
cursor.executemany(
    "INSERT OR IGNORE INTO orders VALUES (?,?,?,?,?,?)",
    orders
)

# Save everything
conn.commit()
conn.close()

print("✅ Database created successfully!")
print("   Tables created: customers, products, orders")
print("   Customers added: 7")
print("   Products added: 8")
print("   Orders added: 15")