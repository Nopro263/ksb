create sequence invoices_id_seq;

alter sequence invoices_id_seq owner to ksb;

alter sequence invoices_id_seq owned by invoice.id;

