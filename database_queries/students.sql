create table students(
    roll_number varchar(15) primary key,
    name varchar(20) not null,
    semester int not null check(semester between 1 and 8),
    branch varchar(5) not null,
    password_hash varchar(255) not null
);