create table topic_tag(
    topic_name varchar(20) unique not null,
	question_id int not null,
    foreign key (question_id) references questions(question_id)
);