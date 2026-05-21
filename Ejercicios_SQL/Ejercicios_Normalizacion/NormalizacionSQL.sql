
-- SQLite


-----o-----------o-----------o-----------o------
--Exercise #!

--Tables Creation
-- CREATE TABLE Customers (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     customer_name VARCHAR(20) NOT NULL,
--     customer_phone VARCHAR(15) NOT NULL
-- );

-- CREATE TABLE Customer_Addresses (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     customer_id INTEGER NOT NULL,
--     address VARCHAR(255) NOT NULL,
--     FOREIGN KEY (customer_id) REFERENCES Customers(id)
-- );

-- CREATE TABLE Orders (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     customer_id INTEGER NOT NULL,
--     customer_address_id INTEGER NOT NULL,
--     delivery_time DATETIME NOT NULL,

--     FOREIGN KEY (customer_id) REFERENCES Customers(id),
--     FOREIGN KEY (customer_address_id) REFERENCES Customer_Addresses(id)
-- );

-- CREATE TABLE Items (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     item_name VARCHAR(50) NOT NULL,
--     price DECIMAL(10, 2) NOT NULL
-- );

-- CREATE TABLE Order_Items (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     order_id INTEGER NOT NULL,
--     item_id INTEGER NOT NULL,
--     quantity INTEGER NOT NULL,
--     special_request VARCHAR(255),

--     FOREIGN KEY (order_id) REFERENCES Orders(id),
--     FOREIGN KEY (item_id) REFERENCES Items(id)
-- );

--Data Insertion

-- INSERT INTO Customers (customer_name, customer_phone) 
-- VALUES
-- ('Alice', '123-456-7890'),
-- ('Bob', '987-654-3210'),
-- ('Claire', '555-123-4567');

-- INSERT INTO Customer_Addresses (customer_id, address)
-- VALUES
-- (1, '123 Main St'),
-- (2, '456 Elm St'),
-- (2, '4th Avenue'),
-- (3, '789 Oak St'),
-- (3, '464 Georgia St');

-- INSERT INTO Orders (customer_id, customer_address_id, delivery_time)
-- VALUES
-- (1, 1, '2026-01-01 18:00:00'),
-- (2, 2, '2026-01-01 19:30:00'),
-- (2, 3, '2026-01-01 19:30:00'),
-- (3, 4, '2026-01-01 12:00:00'),
-- (3, 5, '2026-01-01 17:00:00');

-- INSERT INTO Items (item_name, price)
-- VALUES
-- ('Cheeseburger', 8.00),
-- ('Fries', 3.00),
-- ('Pizza', 12.00),
-- ('Salad', 6.00),
-- ('Water', 1.00);

-- INSERT INTO Order_Items (order_id, item_id, quantity, special_request)
-- VALUES
-- (1, 1, 2, 'No onions'),
-- (1, 2, 1, 'Extra ketchup'),
-- (2, 3, 1, 'Extra cheese'),
-- (3, 2, 2, 'None'),
-- (4, 4, 1, 'No croutons'),
-- (5, 5, 1, 'None');

-- Test Queries

-- SELECT * FROM Customers;
-- SELECT * FROM Customer_Addresses;
-- SELECT * FROM Orders;
-- SELECT * FROM Items;
-- SELECT * FROM Order_Items;

-----o-----------o-----------o-----------o------

-- Proceso de normalización para ejercicio Orders: 

-- 1. Se identifica redundancia en la tabla original: 
--     • clientes repetidos 
--     • direcciones repetidas 
--     • productos repetidos 
--     • precios repetidos 
      
-- 2. Se detectan las entidades principales: 
--     • Customers 
--     • Addresses 
--     • Orders 
--     • Items 
      
-- 3. Se separan los datos del cliente en Customers.
 
-- 4. Se separan las direcciones en Customer_Addresses para permitir múltiples direcciones por cliente.

-- 5. Se separan los productos en Items.

-- 6. Se crea Orders para representar cada pedido individual.

-- 7. Se detecta una relación N:M entre:
--     • Orders 
--     • Items 
      
-- 8. Se crea la tabla puente Order_Items para resolver la relación N:M.

-- 9. Se mueven los atributos que pertenecen a la relación pedido-producto: 
--     • quantity 
--     • special_request
      
-- 10. Se elimina redundancia y dependencias incorrectas.

-- NOTA: Se detecta una inconsistencia con los datos en la tabla original. Parece que los dos pedidos de Bob pertenecen a la misma orden, 
-- a pesar de que ambos tienen la misma hora de entrega, van hacia direcciones distintas, lo cual no hace sentido. 
-- Por lo que en la resolución, se separa en dos pedidos. 

