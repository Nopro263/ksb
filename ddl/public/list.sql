create table list
(
    id       integer generated always as identity
        constraint list_pk
            primary key,
    owner_id integer not null
        constraint list_users_id_fk
            references users
);

alter table list
    owner to ksb;

