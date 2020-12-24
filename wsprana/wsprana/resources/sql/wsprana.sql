/*
 Package Data
*/
CREATE TABLE appdata(
    author      TEXT,
    copyright   TEXT,
    license     TEXT,
    version     TEXT,
    email       TEXT,
    status      TEXT
);
INSERT INTO appdata(author,copyright,license,version,email,status) VALUES
    ('Greg Beam',
    '2020',
    'Apache 2.0',
    '0.1.0',
    'ki7mt@yahoo.com',
    'Development'
);

/*
 Record Table
*/
CREATE TABLE records(
    spot_id         TEXT    PRIMARY KEY UNIQUE  NOT NULL,
    timestamp       TEXT,
    reporter        TEXT,
    reporter_grid   TEXT,
    snr             TEXT,
    frequency       TEXT,
    call_sign       TEXT,
    grid            TEXT,
    power           TEXT,
    drift           TEXT,
    distance        TEXT,
    azimuth         TEXT,
    band            TEXT,
    version         TEXT,
    code            INTEGER
);

/*
 Archive Status Table
*/
CREATE TABLE IF NOT EXISTS status(
    name           TEXT    PRIMARY KEY UNIQUE  NOT NULL,
    date_added     TEXT,
    columns        TEXT,
    records        TEXT
);