

-----o-----------o-----------o-----------o------
-- TABLES CREATION

-- CREATE TABLE Shopping_Cart (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     buyer_email VARCHAR(20) NOT NULL
-- );

-- CREATE TABLE Products (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     code VARCHAR(20) NOT NULL,
--     name VARCHAR(30) NOT NULL,
--     price DECIMAL(10, 2) NOT NULL,
--     entry_date DATETIME NOT NULL,
--     brand VARCHAR(20) NOT NULL,
--     stock_available INT NOT NULL
-- );

-- CREATE TABLE Invoices (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     invoice_number INT NOT NULL,
--     purchase_date DATETIME NOT NULL,
--     buyer_email VARCHAR(20) NOT NULL,
--     total_amount DECIMAL(10, 2) NOT NULL
-- );

--JOIN TABLES

-- CREATE TABLE ShoppingCart_Products (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     shopping_cart_id INTEGER NOT NULL,
--     product_id INTEGER NOT NULL,
--     quantity INT NOT NULL,
--     FOREIGN KEY (shopping_cart_id) REFERENCES Shopping_Cart(id),
--     FOREIGN KEY (product_id) REFERENCES Products(id)

--     UNIQUE (shopping_cart_id, product_id)
-- );
    --In order to ensure that a product can only be added once to a shopping cart,
    --we can add a UNIQUE constraint on the combination of shopping_cart_id and product_id.

-- CREATE TABLE Invoice_Products (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     invoice_id INTEGER NOT NULL,
--     product_id INTEGER NOT NULL,
--     quantity INT NOT NULL,
--     total_amount DECIMAL(10, 2) NOT NULL,
--     FOREIGN KEY (invoice_id) REFERENCES Invoices(id),
--     FOREIGN KEY (product_id) REFERENCES Products(id)

--     UNIQUE (invoice_id, product_id)
-- );

-----o-----------o-----------o-----------o------
-- ALTER TABLE Exercise

-- SQLite does not allow adding multiple columns in a single ALTER TABLE statement, so we need to execute separate statements for each column addition.
-- Additionally, SQLite does not support adding a new column as a NOT NULL column, so we will set the default value to an empty string for the new columns.

-- ALTER TABLE Invoices
--     ADD COLUMN customer_phone VARCHAR(15) DEFAULT '';

-- ALTER TABLE Invoices
--     ADD COLUMN employee_id VARCHAR(20) DEFAULT '';

-----o-----------o-----------o-----------o------
-- INSERT section before moving to SELECT exercises

-- INSERT INTO Products (code, name, price, entry_date, brand, stock_available)
-- VALUES
-- ('P001', 'Laptop', 450000.00, '2024-01-15 10:00:00', 'ASUS', 50),
-- ('P002', 'Smartphone', 590000.00, '2024-02-20 12:30:00', 'Apple', 100),
-- ('P003', 'Headphones', 30000.00, '2024-03-05 14:45:00', 'JBL', 200),
-- ('P004', 'Smartwatch', 40000.00, '2024-04-10 16:00:00', 'Xiaomi', 150),
-- ('P005', 'Tablet', 150000.00, '2024-05-25 18:15:00', 'SAMSUNG', 80);

-- INSERT INTO Shopping_Cart (buyer_email)
-- VALUES
-- ('betofallas93@example.com'),
-- ('mfer2125@example.com'),
-- ('bob.sponge@example.com'),
-- ('peter.parker@example.com');

-- INSERT INTO Invoices (invoice_number, purchase_date, buyer_email, total_amount)
-- VALUES
-- (1001, '2024-06-01 10:00:00', 'betofallas93@example.com', 450000.00),
-- (1002, '2024-06-02 12:30:00', 'mfer2125@example.com', 1180000.00),
-- (1003, '2024-06-03 14:45:00', 'bob.sponge@example.com', 30000.00),
-- (1004, '2024-06-04 16:00:00', 'peter.parker@example.com', 150000.00)
-- (1005, '2024-08-01 11:27:00', 'betofallas93@example.com', 50000.00),
-- (1006, '2024-11-01 05:30:00', 'betofallas93@example.com', 150000.00),
-- (1007, '2024-07-02 09:20:00', 'mfer2125@example.com', 110000.00),
-- (1008, '2024-08-12 04:10:00', 'mfer2125@example.com', 80000.00),
-- (1009, '2024-10-12 01:17:00', 'mfer2125@example.com', 165000.00),
-- (1010, '2024-10-02 13:16:00', 'peter.parker@example.com', 30000.00),
-- (1011, '2024-11-01 17:09:00', 'peter.parker@example.com', 45000.00);

-- INSERT INTO ShoppingCart_Products (shopping_cart_id, product_id, quantity)
-- VALUES
-- (1, 1, 1),
-- (1, 2, 2),
-- (2, 3, 1),
-- (2, 4, 1),
-- (3, 2, 1),
-- (3, 4, 1),
-- (4, 5, 1),
-- (4, 1, 1);

-- INSERT INTO Invoice_Products (invoice_id, product_id, quantity, total_amount)
-- VALUES
-- (1, 1, 1, 450000.00),
-- (1, 2, 2, 1180000.00),
-- (2, 3, 1, 30000.00),
-- (2, 4, 1, 40000.00),
-- (3, 2, 1, 590000.00),
-- (3, 4, 1, 40000.00),
-- (4, 5, 1, 150000.00),
-- (4, 1, 1, 450000.00);

-----o-----------o-----------o-----------o------
-- SELECT exercises

--1.
-- SELECT * FROM Products;

--2.
-- SELECT * FROM Products
-- WHERE price > 50000.00;

--3.
-- SELECT * FROM Invoice_Products WHERE product_id = 2;

--4.
-- SELECT product_id, SUM(total_amount)
-- AS Total_comprado
-- FROM Invoice_Products
-- GROUP BY product_id;

--5.
-- SELECT buyer_email, COUNT(*) AS Total_facturas
-- FROM Invoices
-- GROUP BY buyer_email
-- HAVING COUNT(*) > 0;

--6.
-- SELECT invoice_number, total_amount
-- AS Total_factura
-- FROM Invoices
-- ORDER BY total_amount DESC;

--7.
-- SELECT * from Invoices
-- WHERE invoice_number = 1007;

