create table users
(
    id         integer generated always as identity
        constraint users_pk
            primary key,
    first_name varchar not null,
    last_name  varchar not null,
    email      varchar not null,
    password   varchar not null,
    nickname   varchar not null
);

alter table users
    owner to ksb;

