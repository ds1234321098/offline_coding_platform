CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    session_date DATE NOT NULL,
    session_time TIME NOT NULL,
    status VARCHAR(7) NOT NULL CHECK (status IN ('active', 'ended'))
);