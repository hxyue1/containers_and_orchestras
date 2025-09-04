CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    age INT,
    signup_date DATE
);

INSERT INTO users (username, age, signup_date)
SELECT
    'user_' || gs,                      -- usernames like user_1 … user_1000
    (random() * 60 + 18)::int,          -- random ages between 18–78
    CURRENT_DATE - (random() * 365)::int -- random signup date within past year
FROM generate_series(1, 1000) gs;
