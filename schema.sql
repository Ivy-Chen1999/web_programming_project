CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    coach_id INTEGER REFERENCES users(id),
    name TEXT,
    description TEXT,
    time TIMESTAMP
);


CREATE TABLE participation (
    id SERIAL PRIMARY KEY,
    trainee_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    joined_at TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE trainee_reviews (
    id SERIAL PRIMARY KEY,
    trainee_id INTEGER REFERENCES users(id),
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    stars INTEGER CHECK (stars BETWEEN 1 AND 5),
    comment TEXT
);

CREATE TABLE coach_feedback (
    id SERIAL PRIMARY KEY,
    coach_id INTEGER REFERENCES users(id),
    trainee_id INTEGER REFERENCES users(id),
    activity_id INTEGER REFERENCES activities(id) ON DELETE CASCADE,
    feedback TEXT
);