CREATE TABLE certificates (
    date timestamp default current_timestamp,
    hostname text,
    port text,
    serial_number text,
    subject text,
    public_key_type text,
    sslv2 text,
    sslv3 text,
    tls1_0 text,
    tls1_1 text,
    tls1_2 text,
    tls1_3 text,
    not_after timestamp,
    weak_algo boolean
);

CREATE TABLE scan_errors (
    date timestamp default current_timestamp,
    hostname text,
    port text,
    error_message text
);