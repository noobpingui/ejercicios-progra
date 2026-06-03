
--TABLES CREATION

-- CREATE TABLE Products (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(50) NOT NULL,
--     price DECIMAL(10, 2) NOT NULL,
--     stock INT NOT NULL DEFAULT 0
-- );


-- CREATE TABLE Users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(50) NOT NULL,
--     email VARCHAR(100) NOT NULL
-- );


-- CREATE TABLE Bills (
--     id SERIAL PRIMARY KEY,
--     user_id INT NOT NULL,
--     total DECIMAL(10, 2) NOT NULL,
--     bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     status VARCHAR(20) NOT NULL DEFAULT 'activa',
--     FOREIGN KEY (user_id) REFERENCES Users(id)
-- );


-- CREATE TABLE Bills_Products (
--     id SERIAL PRIMARY KEY,
--     bill_id INT NOT NULL,
--     product_id INT NOT NULL,
--     quantity INT NOT NULL,

--     UNIQUE (bill_id, product_id),

--     FOREIGN KEY (bill_id) REFERENCES Bills(id),
--     FOREIGN KEY (product_id) REFERENCES Products(id)

-- );

-- CREATE TABLE Shopping_Cart (
--     id SERIAL PRIMARY KEY,
--     user_id INT NOT NULL,
    
--     FOREIGN KEY (user_id) REFERENCES Users(id)
-- );

-- CREATE TABLE Shopping_Cart_Products (
--     id SERIAL PRIMARY KEY,
--     cart_id INT NOT NULL,
--     product_id INT NOT NULL,
--     quantity INT NOT NULL,

--     UNIQUE (cart_id, product_id),

--     FOREIGN KEY (cart_id) REFERENCES Shopping_Cart(id),
--     FOREIGN KEY (product_id) REFERENCES Products(id)

-- );

--DATA INSERTION

-- INSERT INTO Products (name, price, stock) VALUES
-- ('Laptop ASUS ROG STRIX 16', 950000.00, 10),
-- ('Iphone 12', 450000.00, 20),
-- ('Headphones JBL', 600000.00, 15),
-- ('Smart TV Samsung 55"', 1200000.00, 5),
-- ('Tablet Apple iPad Pro', 800000.00, 8),
-- ('Consola PlayStation 5', 500000.00, 7),
-- ('Auriculares Sony WH-1000XM4', 350000.00, 18);

-- INSERT INTO Users (username, email) VALUES
-- ('beto', 'beto@email.com'),
-- ('maria', 'maria@email.com'),
-- ('juan', 'juan@email.com'),
-- ('lucia', 'lucia@email.com'),
-- ('carlos', 'carlos@email.com'),
-- ('ana', 'ana@email.com'),
-- ('pedro', 'pedro@email.com');

-- INSERT INTO Bills (user_id, total) VALUES
-- (1, 1500000.00),
-- (2, 800000.00),
-- (3, 500000.00),
-- (4, 1200000.00),
-- (5, 1200000.00),
-- (6, 350000.00),
-- (7, 450000.00); 

-- INSERT INTO Bills_Products (bill_id, product_id, quantity) VALUES
-- (1, 1, 1),
-- (1, 4, 1),
-- (2, 5, 1),
-- (3, 6, 1),
-- (4, 4, 1),
-- (5, 3, 2),
-- (6, 7, 1),
-- (7, 2, 1);




