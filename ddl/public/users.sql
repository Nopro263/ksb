create table users
(
    id           integer generated by default as identity
        constraint users_pk
            primary key,
    first_name   varchar     not null,
    last_name    varchar     not null,
    email        varchar     not null,
    password     varchar     not null,
    nickname     varchar     not null,
    clearance    integer default 10,
    address      varchar(50) not null,
    phone_number varchar(20) not null
);

alter table users
    owner to ksb;

