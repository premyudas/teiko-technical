CREATE TABLE subjects (
    subject         TEXT PRIMARY KEY,
    project         TEXT NOT NULL,
    condition       TEXT NOT NULL,
    age             INTEGER NOT NULL,
    sex             TEXT NOT NULL,
    treatment       TEXT NOT NULL,
    response        TEXT
);

CREATE TABLE samples (
    sample          TEXT PRIMARY KEY,
    subject         TEXT NOT NULL REFERENCES subjects(subject),
    sample_type     TEXT NOT NULL,
    time_from_treatment_start  INTEGER NOT NULL
);

CREATE TABLE cell_counts (
    id              INTEGER PRIMARY KEY, -- auto increments
    sample          TEXT NOT NULL REFERENCES samples(sample),
    population      TEXT NOT NULL,
    count           INTEGER NOT NULL
);