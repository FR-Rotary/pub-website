-- Initial data for the database


INSERT INTO worker_status (name)
VALUES
    ('worker'),
    ('worker_public'),
    ('ex_worker');

INSERT INTO shift_type (name)
VALUES
    ('bar'),
    ('kitchen'),
    ('bar (SA)'),
    ('kitchen (SA)'),
    ('legacy shift type')
