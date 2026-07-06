
CREATE TYPE lyfter_car_rental.user_status 
AS ENUM ('active', 'inactive');

CREATE TYPE lyfter_car_rental.car_status 
AS ENUM ('available', 'rented', 'disabled');

CREATE TYPE lyfter_car_rental.rental_status 
AS ENUM ('active', 'completed');