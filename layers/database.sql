create table subject(
	id integer primary key,
	name varchar(255),
	aliases text
);

create table grade(
	id integer primary key,
	amount integer,
	amount_achieved integer,
	date datetime,
	subject_name varchar(255),
	raw_text text,
	subject_id integer,
	FOREIGN KEY(subject_name, subject_id) REFERENCES subject(name, id)
);


