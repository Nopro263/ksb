create table articles
(
    id         integer               not null
        constraint articles_pk
            primary key,
    name       varchar               not null,
    list_id    integer               not null
        constraint articles_list_id_fk
            references list,
    barcode    integer,
    imported   boolean default false not null,
    invoice_id integer
        constraint articles_invoices_id_fk
            references invoices
);

alter table articles
    owner to ksb;

create index articles_barcode_index
    on articles (barcode);

