
-- DO $$

-- DECLARE

--     v_user_id INTEGER; -- Para almacenar el ID del usuario que realiza la compra
--     v_cart_id INTEGER; -- Para almacenar el ID del carrito de compras que se va a crear
--     v_stock INTEGER; -- Para almacenar el stock actual de el producto que se va a comprar
--     v_quantity INTEGER = 1; -- Para almacenar la cantidad de el producto que se va a comprar
--     v_bill_id INTEGER; -- Para almacenar el ID de la factura que se va a insertar
--     v_product_price NUMERIC(10, 2); -- Para almacenar el precio del producto que se va a comprar    
--     v_total NUMERIC(10, 2) = 0; -- Para almacenar el total de la factura

-- BEGIN

-- -----------------------------------

--     -- 1. Validar que el usuario existe
--     SELECT id INTO v_user_id
--     FROM users
--     WHERE username = 'beto';

--     IF v_user_id IS NULL THEN
--         RAISE EXCEPTION 'El usuario no existe';
--     END IF;


-- -----------------------------------

--     --2. Creamos el carrito de compras para el usuario
--     INSERT INTO shopping_cart (user_id)
--     VALUES (v_user_id)
--     RETURNING id INTO v_cart_id;

--     INSERT INTO shopping_cart_products (cart_id, product_id, quantity)
--     VALUES (v_cart_id, 2, 2), -- (Iphone12)
--            (v_cart_id, 6, 1), -- (Consola PlayStation 5)
--            (v_cart_id, 7, 3); -- (Auriculares Sony WH-1000XM4)


-- -----------------------------------

--     --3. Validar que los productos que se van a comprar tienen stock suficiente
    
--     --Producto - (Iphone12):
--     SELECT stock INTO v_stock
--     FROM products
--     WHERE id = 2;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 2; 

--         IF v_stock < v_quantity THEN
--             RAISE EXCEPTION 'No hay suficiente stock de el producto';
--         END IF;

--     --Producto - (Consola PlayStation 5):
--     SELECT stock INTO v_stock
--     FROM products
--     WHERE id = 6;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 6; 

--         IF v_stock < v_quantity THEN
--             RAISE EXCEPTION 'No hay suficiente stock de el producto';
--         END IF;

--     --Producto - (Auriculares Sony WH-1000XM4):
--     SELECT stock INTO v_stock
--     FROM products
--     WHERE id = 7;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 7; 

--         IF v_stock < v_quantity THEN
--             RAISE EXCEPTION 'No hay suficiente stock de el producto';
--         END IF;
    
-- -----------------------------------

--     --4. Crear la factura para el usuario con el total de la compra
    
--     --Producto - (Iphone12):
--     SELECT price INTO v_product_price
--     FROM products
--     WHERE id = 2;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 2;

--     v_total := v_total + (v_product_price * v_quantity);

--     --Producto - (Consola PlayStation 5):
--     SELECT price INTO v_product_price
--     FROM products
--     WHERE id = 6;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 6;

--     v_total := v_total + (v_product_price * v_quantity);

--     --Producto - (Auriculares Sony WH-1000XM4):
--     SELECT price INTO v_product_price
--     FROM products
--     WHERE id = 7;

--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 7;

--     v_total := v_total + (v_product_price * v_quantity);

--     INSERT INTO bills (user_id, total)
--     VALUES (v_user_id, v_total)

--     RETURNING id INTO v_bill_id;

-- ------------------------------------

--     --5. Insertar datos en la tabla bill_products y reducir el stock de los productos que se compraron

--     --Producto - (Iphone12):
--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 2;

--     INSERT INTO bills_products (bill_id, product_id, quantity)
--     VALUES (v_bill_id, 2, v_quantity); 

--     UPDATE products
--     SET stock = stock - v_quantity
--     WHERE id = 2;

--     --Producto - (Consola PlayStation 5):
--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 6;

--     INSERT INTO bills_products (bill_id, product_id, quantity)
--     VALUES (v_bill_id, 6, v_quantity);

--     UPDATE products
--     SET stock = stock - v_quantity
--     WHERE id = 6;

--     --Producto - (Auriculares Sony WH-1000XM4):
--     SELECT quantity INTO v_quantity
--     FROM shopping_cart_products
--     WHERE cart_id = v_cart_id AND product_id = 7;

--     INSERT INTO bills_products (bill_id, product_id, quantity)
--     VALUES (v_bill_id, 7, v_quantity);

--     UPDATE products
--     SET stock = stock - v_quantity
--     WHERE id = 7;
    
-- END $$;

-----------------------------------


SELECT * from shopping_cart_products;
