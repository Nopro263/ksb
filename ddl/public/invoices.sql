create table invoices
(
    id            integer generated always as identity
        constraint invoices_pk
            primary key,
    creation_time timestamp default clock_timestamp()
);

alter table invoices
    owner to ksb;

