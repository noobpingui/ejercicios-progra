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

-- CREATE TABLE Vehicles (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     vin VARCHAR(20) NOT NULL,
--     vehicle_make VARCHAR(15) NOT NULL,
--     vehicle_model VARCHAR(15) NOT NULL,
--     vehicle_year INTEGER NOT NULL,
--     vehicle_color VARCHAR(15) NOT NULL,
--     owner_id INTEGER NOT NULL,
--     insurance_company_id INTEGER NOT NULL,
--     insurance_policy VARCHAR(20) NOT NULL,

--     FOREIGN KEY (owner_id) REFERENCES Owners(id),
--     FOREIGN KEY (insurance_company_id) REFERENCES Insurance_Companies(id)
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

-- INSERT INTO Vehicles (vin, vehicle_make, vehicle_model, vehicle_year, vehicle_color, owner_id, insurance_company_id, insurance_policy)
-- VALUES
-- ('1HGCM82633A', 'Honda', 'Accord', 2003, 'Silver', 1, 1, 'Fire & Theft'),
-- ('1HGCM82633A', 'Honda', 'Accord', 2003, 'Silver', 2, 2, 'Full Cover'),
-- ('5J6RM4H79EL', 'Honda', 'CR-V', 2014, 'Blue', 3, 3, 'Collision'),
-- ('1G1RA6EH1FU', 'Chevrolet', 'Volt', 2015, 'Red', 4, 4, 'Basic Legal');

-- Test Queries

-- SELECT * FROM Owners;
-- SELECT * FROM Insurance_Companies;
-- SELECT * FROM Vehicles;

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
