create table questions(
    session_id UUID not null
        references sessions(id)
        on DELETE cascade,
    question_number int not null,
    question text not null,
    primary key(session_id, question_number),
    unique(session_id,question)
);