
CREATE TABLE host_details (
    date timestamp default current_timestamp,
    host text,
    port integer,
    scan_started timestamp,
    scan_completed timestamp,
    scan_result_json text,
    scan_id text
);