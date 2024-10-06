create view articles_from_user(id, name, list_id, barcode, owner) as
SELECT articles.id,
       articles.name,
       articles.list_id,
       articles.barcode,
       u.id AS owner
FROM articles
         JOIN list l ON l.id = articles.list_id
         JOIN users u ON u.id = l.owner_id;

alter table articles_from_user
    owner to ksb;

