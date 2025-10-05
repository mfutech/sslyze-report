

CREATE TABLE scans (
    date timestamp default current_timestamp,
    scanid text
);

alter table certificates add column  scan_id text  ; 
alter table scan_errors add column  scan_id text  ;