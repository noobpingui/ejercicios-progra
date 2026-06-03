
-- DO $$

-- DECLARE
--     v_bill_id INT;
--     v_quantity INT;

-- ------------------------------------------

-- BEGIN

--     -- 1. Verificar que la factura existe
--     SELECT id INTO v_bill_id
--     from bills
--     WHERE id = 16;

--         IF v_bill_id IS NULL THEN
--             RAISE EXCEPTION 'La factura no existe';
--         END IF;

-- ------------------------------------------

--     -- 2. Aumentar el stock de los productos

--     --Producto - (Iphone 12):
--     SELECT quantity INTO v_quantity
--     FROM bills_products
--     WHERE bill_id = v_bill_id AND product_id = 2;

--     UPDATE products
--     SET stock = stock + v_quantity
--     WHERE id = 2;

--     --Producto - (Consola PlayStation 5):
--     SELECT quantity INTO v_quantity
--     FROM bills_products
--     WHERE bill_id = v_bill_id AND product_id = 6;

--     UPDATE products
--     SET stock = stock + v_quantity
--     WHERE id = 6;

--     --Producto - (Auriculares Sony WH-1000XM4):
--     SELECT quantity INTO v_quantity
--     FROM bills_products
--     WHERE bill_id = v_bill_id AND product_id = 7;

--     UPDATE products
--     SET stock = stock + v_quantity
--     WHERE id = 7;

-- ------------------------------------------

--     --3. Modificar la factura original para marcarla con el estado de "Retornada"
--     UPDATE bills
--     SET status = 'Retornada'
--     WHERE id = v_bill_id;

-- ------------------------------------------

-- END $$;
