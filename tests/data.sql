-- Populate worker_status & shift_type is done in seed.sql when intializing the database

-- Populate beer_category
INSERT INTO beer_category (name_sv, name_en, priority) VALUES
('Fatöl', 'On tap', 1),
('IPA', 'IPA', 2),
('Stout', 'Stout', 3);

-- Populate beer
INSERT INTO beer (name, style, country_iso_3166_id, abv, volume_ml, price_kr, category_id, available) VALUES
('Falcon', 'Fatöl', '752', 5.2, 330, 20, 1, 1),
('Punk IPA', 'IPA', '826', 5.6, 330, 25, 2, 1),
('Guinness', 'Stout', '372', 4.2, 440, 30, 3, 1);

-- Populate food
INSERT INTO food (name, price_kr, available) VALUES
('Burgare', 99, 1),
('Fish and Chips', 89, 1),
('Vegansk Sallad', 75, 1);

-- Populate snack
INSERT INTO snack (name, price_kr, available) VALUES
('Chips', 20, 1),
('Nötter', 25, 1),
('Oliver', 30, 1);

-- Populate worker
INSERT INTO worker (display_name, first_name, last_name, personal_id_number, telephone, email, address, note, status_id) VALUES
('JohnD', 'John', 'Doe', '850505-1234', '0701234567', 'john.doe@example.com', 'Example Street 1', 'No allergies', 1),
('JaneD', 'Jane', 'Doe', '860606-2345', '', 'jane.doe@example.com', 'Example Street 2', '', 2);

-- Populate shift
INSERT INTO shift (worker_id, shift_type_id, date, start, end) VALUES
(1, 1, '2023-04-01', '08:00', '16:00'),
(2, 2, '2023-04-01', '16:00', '00:00');

-- Populate opening_hours
INSERT INTO opening_hours (date, start, end) VALUES
('2023-04-01', '08:00', '23:00'),
('2023-04-02', '10:00', '20:00');

-- Populate news
INSERT INTO news (time, title_en, body_en, title_sv, body_sv) VALUES
('2023-04-01 12:00', 'Grand Opening', 'We are excited to announce the grand opening of our pub.', 'Stor Öppning', 'Vi är glada att meddela den stora öppningen av vår pub.');