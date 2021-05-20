-- Initial data for the database

INSERT INTO beer_category (name)
VALUES
    ('on_keg'),
    ('lager'),
    ('ale'),
    ('porter_stout'),
    ('weiss'),
    ('barleywine'),
    ('belgian'),
    ('lambic'),
    ('other'),
    ('wine'),
    ('cider'),
    ('nonalcoholic');

INSERT INTO worker_status (name)
VALUES
    ('worker'),
    ('worker_public'),
    ('ex_worker');

INSERT INTO shift_type (name)
VALUES
    ('bar'),
    ('kitchen'),
    ('legacy shift type')
