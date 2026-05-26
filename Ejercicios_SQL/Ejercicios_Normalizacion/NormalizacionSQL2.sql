-- SQLite

-----o-----------o-----------o-----------o------
--Exercise #2

--Tables Creation

-- CREATE TABLE Owners (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     owner_name VARCHAR(20) NOT NULL,
--     owner_phone VARCHAR(20) NOT NULL
-- );

-- CREATE TABLE Insurance_Companies (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     company_name VARCHAR(20) NOT NULL
-- );

-- CREATE TABLE Insurance_Policies (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     insurance_company_id INTEGER NOT NULL,
--     insurance_policy_name VARCHAR(50) NOT NULL,

--     FOREIGN KEY (insurance_company_id) REFERENCES Insurance_Companies(id)
-- );

-- CREATE TABLE Makes (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     make_name VARCHAR(20) NOT NULL
-- );

-- CREATE TABLE Models (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     make_id INTEGER NOT NULL,
--     model_name VARCHAR(20) NOT NULL,

--     FOREIGN KEY (make_id) REFERENCES Makes(id)
-- );

-- CREATE TABLE Vehicles (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     vin VARCHAR(20) NOT NULL,
--     model_id INTEGER NOT NULL,
--     vehicle_year INTEGER NOT NULL,
--     vehicle_color VARCHAR(20) NOT NULL,
--     owner_id INTEGER NOT NULL,
--     insurance_policy_id INTEGER NOT NULL,

--     FOREIGN KEY (model_id) REFERENCES Models(id),
--     FOREIGN KEY (owner_id) REFERENCES Owners(id),
--     FOREIGN KEY (insurance_policy_id) REFERENCES Insurance_Policies(id)
-- );

--Data Insertion

-- INSERT INTO Owners (owner_name, owner_phone)
-- VALUES 
-- ('Alice', '123-456-7890'),
-- ('Bob', '987-654-3210'),
-- ('Claire', '555-123-4567'),
-- ('Dave', '111-222-3333');


-- INSERT INTO Insurance_Companies (company_name)
-- VALUES
-- ('ABC Insurance'),
-- ('XYZ Insurance'),
-- ('DEF INSURANCE'),
-- ('GHI Insurance');

-- INSERT INTO Insurance_Policies (insurance_company_id, insurance_policy_name)
-- VALUES
-- (1, 'Fire & Theft'),
-- (2, 'Full Cover'),
-- (3, 'Collision'),
-- (4, 'Basic Legal');

-- INSERT INTO Makes (make_name)
-- VALUES
-- ('Honda'),
-- ('Chevrolet'),
-- ('Toyota'),
-- ('Ford');

-- INSERT INTO Models (make_id, model_name)
-- VALUES
-- (1, 'Accord'),
-- (1, 'CR-V'),
-- (2, 'Volt'),
-- (3, 'Camry'),
-- (4, 'Mustang');

-- INSERT INTO Vehicles (vin, model_id, vehicle_year, vehicle_color, owner_id, insurance_policy_id)
-- VALUES
-- ('1HGCM82633A', 1, 2003, 'Silver', 1, 1),
-- ('1HGCM82633A', 1, 2003, 'Silver', 2, 2),
-- ('5J6RM4H79EL', 2, 2014, 'Blue', 3, 3),
-- ('1G1RA6EH1FU', 3, 2015, 'Red', 4, 4);

-- Test Queries

-- SELECT * FROM Owners;
-- SELECT * FROM Insurance_Companies;
-- SELECT * FROM Vehicles;
-- SELECT * FROM Insurance_Policies;
-- SELECT * FROM Makes;
-- SELECT * FROM Models;

-----o-----------o-----------o-----------o------

-- Proceso de normalización para ejercicio Cars: 

-- 1. Se identifica redundancia en la tabla original: 
--     • owner_name repetido 
--     • owner_phone repetido 
--     • insurance_company repetida 

-- 2. Se detectan las entidades principales: 
--     • Owners 
--     • Insurance_Companies 
--     • Vehicles 

-- 3. Se separa la información de propietarios en Owners.
 
-- 4. Se Separan las aseguradoras en Insurance_Companies.
 
-- 5. Se crea Vehicles para almacenar: 
--     • VIN 
--     • make 
--     • model 
--     • year 
--     • color 
--     • owner_id 
--     • insurance_company_id 
--     • insurance_policy 


-- 6. Se relacionan las tablas usando PK y FK: 
--     • Vehicles.owner_id → Owners.id 
--     • Vehicles.insurance_company_id → Insurance_Companies.id 
      
-- 7. Se detectan las relaciones: 
--     • Owners 1:N Vehicles 
--     • Insurance_Companies 1:N Vehicles 

-- 8. Se determina que no era necesaria una tabla cruz porque no existe relación N:M.

-- 9. Se elimina redundancia y dependencias incorrectas.

-- Nota: Al igual que en el ejercicio anterior, se detentan inconsistencias en los datos de la tabla original. 
-- En este caso, existe dos registros con el mismo VIN, marca, modelo, año y color, en otras palabras, se trata del mismo vehículo, sin embargo, 
-- se muestra un dueño diferente con una aseguradora diferente. Dicho esto, podría ser que el vehículo cambiara de dueño o bien, 
-- para fines del “negocio” el vehículo esta registrado con dos dueños. Por esta razón, se mantiene como dos registros distintos.
