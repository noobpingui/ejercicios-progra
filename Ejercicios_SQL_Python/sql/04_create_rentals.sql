

CREATE TABLE lyfter_car_rental.rental(
    id              SERIAL          PRIMARY KEY,
    user_id         INT             NOT NULL    REFERENCES lyfter_car_rental.user_account(id),
    car_id          INT             NOT NULL    REFERENCES lyfter_car_rental.car(id),
    rental_date     TIMESTAMP       NOT NULL    DEFAULT CURRENT_TIMESTAMP,
    status          lyfter_car_rental.rental_status NOT NULL    DEFAULT 'active'

)