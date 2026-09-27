CREATE TABLE session_students (
    session_id UUID NOT NULL
        REFERENCES sessions(id)
        ON DELETE CASCADE,
    roll_number VARCHAR(30) NOT NULL
        REFERENCES students(roll_number),
    question_number INT NOT NULL
        REFERENCES questions(question_number),
    result VARCHAR(20) NOT NULL
        DEFAULT 'Not attempted'
        CHECK (result IN ('Passed', 'TLE', 'Failed', 'Not attempted', 'MLE')),
    PRIMARY KEY (session_id, roll_number, question_number)
);