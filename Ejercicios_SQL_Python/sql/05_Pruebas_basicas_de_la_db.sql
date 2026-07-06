
--Con la DB creada, cree los siguientes scripts:

--1. Un script que agregue un usuario nuevo
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Alberto Fallas', 'afallasl@example.net', 'Afallas93', 'aKMufxlSHq0zyvJ', '1993-02-21');


--2. Un script que agregue un automovil nuevo
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Suzuki', 'Alto', 2019);


--3. Un script que cambie el estado de un usuario
UPDATE  lyfter_car_rental.user_account
SET     status = 'inactive'
WHERE   username = 'Archibald74';


--4. Un script que cambie el estado de un automovil
UPDATE  lyfter_car_rental.car
SET     status = 'disabled'
WHERE   id = 15;


--5. Un script que genere un alquiler nuevo con los datos de un usuario y un automovil
INSERT into lyfter_car_rental.rental(user_id, car_id)
VALUES  (51,26);

-- Nota: Aqui es necesario actualizar el status de car ya que aun no se han aplicado 
-- reglas de negocio. Solo para fines de el ejerccio, pero se implementara la logica 
-- en la parte de creacion de el API.
UPDATE lyfter_car_rental.car
SET status = 'rented'
WHERE id = 26;


--6. Un script que confirme la devolución del auto al completar el alquiler, 
-- colocando el auto como disponible y completando el estado del alquiler
 
UPDATE lyfter_car_rental.rental
SET status = 'completed'
WHERE id = 1;

UPDATE lyfter_car_rental.car
SET status = 'available'
WHERE id = 26;

SELECT * FROM lyfter_car_rental.rental
WHERE id = 1;

SELECT * FROM lyfter_car_rental.car
WHERE id = 26;

--7. Un script que deshabilite un automovil del alquiler
UPDATE lyfter_car_rental.car
SET status = 'disabled'
WHERE id = 14;


--8. Un script que obtenga todos los automoviles alquilados, y 
-- otro que obtenga todos los disponibles.
SELECT * FROM lyfter_car_rental.car
WHERE status = 'rented';

SELECT * FROM lyfter_car_rental.car
WHERE status = 'available';

