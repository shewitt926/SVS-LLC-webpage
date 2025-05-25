DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    _name TEXT NOT NULL,
    _price INTEGER NOT NULL,
    _description TEXT,
    _image BLOB
);