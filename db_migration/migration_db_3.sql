
CREATE TABLE scan_details (
    date timestamp default current_timestamp,
    host text,
    port integer,
    scan_started timestamp,
    scan_completed timestamp,
    scan_result_json text,
    scan_id text
);

CREATE TABLE hosts (
    date timestamp default current_timestamp,
    host text,
    port integer,
    sslv2 text,
    sslv3 text,
    tls1_0 text,
    tls1_1 text,
    tls1_2 text,
    tls1_3 text,
    scan_id text,
    certificate_serial_number text,
    weak_algo boolean

);

ALTER TABLE certificates RENAME TO certificates_v1;

CREATE TABLE certificates (
    date timestamp default current_timestamp,
    serial_number text,
    subject text,
    public_key_type text,
    not_after timestamp,
    weak_algo boolean,
    parent_certificate_serial_number text,
    scan_id text

);