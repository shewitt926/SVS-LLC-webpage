import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('static/photos/products/temp_prod.jpg', 'rb') as img1:
    img1_blob = img1.read()
with open('static/photos/products/temp_prod2.jpg', 'rb') as img2:
    img2_blob = img2.read()

cur.execute("INSERT INTO products (_name, _price, _description, _image) VALUES (?, ?, ?, ?)",
            ('TEST PRODUCT 1', 1, 'Sample description', img1_blob))

cur.execute("INSERT INTO products (_name, _price, _description, _image) VALUES (?, ?, ?, ?)",
            ('TEST PRODUCT 2', 2, 'Sample description', img2_blob))

connection.commit()
connection.close()