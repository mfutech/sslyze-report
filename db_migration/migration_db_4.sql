alter table hosts add column  mozilla_old text  ;
alter table hosts add column  mozilla_intermediate text  ;
alter table hosts add column  mozilla_modern text  ;

alter table certificates add column issuer text ;

create table if not exists last_scan (
    scan_id text,
    host text, 
    port integer,
    primary key (host, port)
)