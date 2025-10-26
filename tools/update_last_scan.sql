 insert into last_scan (scan_id,host, port)  select max(scan_id),host,port from hosts group by host,port;
