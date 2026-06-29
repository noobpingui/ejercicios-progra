
--TABLE creation user_account:

CREATE TABLE lyfter_car_rental.user_account(
    id              SERIAL          PRIMARY KEY,
    name            VARCHAR(50)     NOT NULL,
    email           VARCHAR(255)    UNIQUE  NOT NULL,
    username        VARCHAR(255)    UNIQUE  NOT NULL,
    password_hash   VARCHAR(255)    NOT NULL,
    birth_date      DATE            NOT NULL, --Format: YYYY-MM-DD
    status          lyfter_car_rental.user_status   NOT NULL    DEFAULT 'active',
    is_delinquent   BOOLEAN         NOT NULL    DEFAULT false
)

--DATA INSERT for TABLE user_account:

Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Marguerite Strosin', 'Kolby_Dickinson@example.net', 'Devon91', 'iLKehwlSJm0xqxC', '1988-02-23');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Jody Kilback', 'Leda54@example.org', 'Liza82', 'Ae8V16WQVxGFZjz', '1991-06-25');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Kenny Kuhlman', 'Ethelyn_Russel@example.org', 'Bettie_Balistreri', 'HMOXZdHxj32M8lK', '2003-10-25');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Morris Wilderman', 'Javonte_Funk@example.org', 'Yolanda.Kassulke19', 'qsf3Chlw4oG4ybV', '1981-05-12');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Archie Toy', 'Jermey.Jakubowski@example.net', 'Ken_McClure74', 'r0INnyuSpEK497E', '1995-06-08');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Darla Kshlerin', 'Eliza8@example.org', 'Tatyana92', '4ba_ZWvj1hMAuyl', '2007-09-24');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Sally Ortiz-Jerde', 'Maude_Braun-Windler@example.com', 'Howell_Bauch', 'lx3KunfjH4FEBu8', '2000-11-20');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Marlene Mertz', 'Edwina98@example.com', 'Sydnee.Macejkovic', 'rhG1Yut0DgLMk4f', '1986-02-27');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Mr. Willard Muller Sr.', 'Coty58@example.net', 'Lou.Turner82', 'uO_35JIpN_f4Qmp', '2003-10-10');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Christy Hettinger', 'Zackary_Hettinger@example.org', 'Susana11', 'm0xxs_cE2NViaSH', '2004-11-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Dr. Edmond Koelpin', 'Brittany67@example.com', 'Fabiola48', 'hljsdjEmaYMsJh1', '2005-10-18');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Perry Cole IV', 'Vena81@example.net', 'Paxton69', 'COxNJ8dc72iruUo', '2003-10-10');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Eleanor Bernier', 'Maybelle_Fahey-Wuckert@example.net', 'Yesenia54', 'vzgEb5MHdo4j4Mq', '2001-03-28');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Robyn Quigley', 'Alf_Lynch@example.org', 'Sincere1', '22hdxweyxgh5wfi', '2006-03-18');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Jamie Feil', 'Rose45@example.com', 'Archibald74', 'DQzKSnCy0V4cOqq', '2000-06-04');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Wilbur Corkery', 'Coleman.Leuschke@example.net', 'Annamarie.Trantow', 'yrgyNb2Ic5nXmR7', '2006-01-19');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Spencer Schoen', 'Jakayla.Baumbach@example.com', 'Crawford_Bernhard80', 'BiZEGJ7Yb09qjLf', '2006-06-21');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Courtney McKenzie', 'Marlee.Muller98@example.net', 'Tatum.Ferry73', 'U75tcSOa2Qfgdnz', '1994-12-28');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Miss Terry Grimes-Russel', 'Dorothy.Bashirian33@example.com', 'Stephon.Osinski-Rogahn', '8u8C8igeCaQ04QC', '2003-10-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Maxine Kohler', 'Nona.Kihn4@example.com', 'Kayli96', 'vzvh_R8VM6wswZA', '1991-02-28');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Ms. Diana Nienow', 'Janis_Koepp@example.com', 'Rylee64', 'ja4F9hARx1h41Ub', '2001-02-18');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Ms. Lula Bartell', 'Major81@example.net', 'Jonathan_Reilly', '9w9zQe1Py8oUWAj', '2001-05-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Angelina Jast', 'Oda_Zemlak@example.org', 'Addie63', 'x1Ne_p4HAPk8VyG', '2002-07-14');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Gordon Schumm', 'Marianna_Luettgen@example.net', 'Luis_Yundt7', 'cQgLC8pUxFi6D95', '2000-11-14');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Sara Haley', 'Claud.Dach65@example.com', 'Desiree.Davis32', 'k8RKRaSO2Mk13rn', '2006-06-12');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Samantha Bernier PhD', 'Alex.Ward81@example.net', 'Jarrett_Carter', '23juNmR83rbX0fF', '2003-01-10');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Rickey Christiansen', 'Estella_Funk@example.com', 'Noemy.Jacobs', 'gN7ioVm2rsSQNYO', '2001-09-18');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Rita Roob', 'Rebeka_Wisozk53@example.com', 'Millie.Tromp49', '0FTxvPfKxLHtxyb', '2000-04-03');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Sherri Yundt MD', 'Melba.Schowalter@example.net', 'Jimmie68', 'lzF8c63e4EFVutZ', '2002-07-04');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Sophie Kunze', 'Ellen_Upton84@example.com', 'Caitlyn75', 'e2tPjqgPWeA4Axj', '1992-09-02');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Lorenzo Hintz', 'Lois54@example.com', 'Marta_Rolfson', 'OPLTEsYDjjsqbca', '2005-11-08');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Janet Rau', 'Audreanne.Terry@example.org', 'Vincenza_Conroy29', 'zeD0IXAVzYUv91h', '1980-07-19');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Miss Kristy Mann', 'Kiera_Kunze@example.net', 'Jillian.Casper68', 'kCrg8snbmxBZxwp', '1997-02-19');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Shelia Hane', 'Regan_Schuster@example.org', 'Destinee_Carroll-Gerlach8', 'h6cB_it0XrcOXvD', '1989-10-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Mr. Benny Renner DDS', 'Lilian.Glover84@example.net', 'Fay_Dickinson', 'MkFk8v_IrZzFHEr', '1997-03-06');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Javier Jacobson', 'Toy.Denesik@example.org', 'Chad.Brakus21', '3wvJ2j4xu9iDbCM', '2001-04-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Arturo Tremblay', 'Geovany_Lang@example.org', 'Herman40', 'o5mEs_mw8uViFZx', '2004-04-18');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Miss Eva Nolan Jr.', 'Samanta_Daniel67@example.org', 'Reyna_Maggio44', 'Lb_Kb_Ng_1LcP77', '2001-08-17');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Dr. Edward Reilly', 'Alexys.Bins25@example.org', 'Dedrick_Champlin20', 'mJSJgX5OCyrm0gc', '2005-12-13');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Kerry Weimann', 'Braxton7@example.net', 'Dina.Rowe48', '2Z7hhdxjL9MC7zA', '2003-04-08');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Emanuel Stark', 'Autumn_Gorczany56@example.com', 'Lora.Bins1', 'QPSToxnxD10S0mJ', '2005-10-19');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Elvira Boyer', 'Angela_Graham@example.com', 'Rosalind71', 'Q3sznLLmUfiRCdn', '2005-06-27');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Elijah Goldner', 'Kiarra.Schmeler@example.org', 'Amir.Bogisich', 'P99HzNGroX_q7J3', '2007-09-10');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Rosa Hyatt', 'Abagail.Langosh88@example.org', 'Aubrey_Mills', 'H5q1BuKtPnT9p3n', '2005-05-21');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Delores Runolfsdottir', 'Adolfo0@example.net', 'Emelia.Stanton10', 'oINwty2uBSkGyeU', '2003-03-08');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Krystal Gleason', 'Edwina88@example.com', 'Jacky_Grant', 'axXi7m51B9ARjuG', '1987-09-05');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Alvin Hartmann', 'Myron41@example.com', 'Freddie_Raynor89', 'P4akn3z8PeJgBc0', '2004-12-09');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Ramiro Keebler', 'Roxane.Waters@example.org', 'Urban_Nicolas44', 'RTX370iiLzoQTd1', '1997-04-09');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Naomi Schimmel', 'Vidal92@example.org', 'Yesenia_Gerlach', 'a8dhjZr0DMbscOw', '2003-10-24');
Insert Into lyfter_car_rental.user_account (name, email, username, password_hash, birth_date) 
VALUES ('Ms. Sheri Rau', 'Einar_Pouros@example.com', 'Craig_Huels73', 'c2j3fkvTSmCcPtO', '2004-08-27');