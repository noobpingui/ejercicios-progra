
--TABLE creation cars:

CREATE TABLE lyfter_car_rental.car(
    id              SERIAL          PRIMARY KEY,
    brand           VARCHAR(50)    NOT NULL,
    model           VARCHAR(50)    NOT NULL,
    year            INTEGER         NOT NULL        CHECK (year BETWEEN 1886 AND 2100),
    status          lyfter_car_rental.car_status    NOT NULL    DEFAULT 'available'
)

--DATA INSERT for TABLE cars:

Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Toyota', 'Corolla', 2017);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Honda', 'Fit', 2015);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Nissan', 'Kicks', 2022);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Kia', 'Rio', 2025);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Hyundai', 'Accent', 2016);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Kia', 'Forte', 2019);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Toyota', 'Yaris', 2018);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Hyundai', 'Elantra', 2021);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Kia', 'Sportage', 2023);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Honda', 'HR-V', 2025);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Hyundai', 'Tucson', 2023);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Kia', 'Seltos', 2020);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Toyota', 'Camry', 2019);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Hyundai', 'Santa Fe', 2015);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Nissan', 'Rogue', 2017);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Kia', 'Soul', 2018);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Nissan', 'Altima', 2020);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Honda', 'CR-V', 2021);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Hyundai', 'Kona', 2022);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Nissan', 'Versa', 2024);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Toyota', 'RAV4', 2021);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Nissan', 'Sentra', 2017);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Honda', 'Accord', 2015);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Toyota', 'Prius', 2016);
Insert Into lyfter_car_rental.car (brand, model, year) 
VALUES ('Honda', 'Civic', 2023);