create database email_sender;

-- connect to database 
\c email_sender

create table emails (
    id serial not null,
    date timestamp not null default CURRENT_TIMESTAMP,
    subject varchar(100) not null,
    message varchar(250) not null
);
