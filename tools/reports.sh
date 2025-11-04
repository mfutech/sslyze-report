#!/bin/bash

echo "--$0--"
BASEDIR=$(dirname "${0}")
OUTDIR=${BASEDIR}/out
mkdir -p "${OUTDIR}"

DB_FILE=$(dirname "${0}")/../data/sslyze_report.db

echo "using : ${DB_FILE}"

OUTEXT=$(date +%Y%m%d_%H%M)

echo "output : ${OUTDIR}/XX.${OUTEXT}"

echo "sslv2 hosts"
sqlite3 -header -csv -separator \; ${DB_FILE} "select h.date, h.host, h.port, json_extract(sslv2, '\$.enabled') as sslv2_activated from hosts h join last_scan s on (s.host = h.host and s.port = h.port) where sslv2_activated = 1;" | tee ${OUTDIR}/hosts_sslv2.${OUTEXT}.csv
echo "sslv3 hosts"
sqlite3 -header -csv -separator \; ${DB_FILE} "select h.date, h.host, h.port, json_extract(sslv3, '\$.enabled') as sslv3_activated from hosts h join last_scan s on (s.host = h.host and s.port = h.port) where sslv3_activated = 1;" | tee ${OUTDIR}/hosts_sslv3.${OUTEXT}.csv
echo "outdate certificates"
sqlite3 -header -csv -separator \; ${DB_FILE} "select distinct subject,fingerprintSHA256, not_after from certificates c  inner join  last_scan s  on (c.scan_id = s.scan_id) and c.not_after <= date('now');" | tee ${OUTDIR}/expired_certs.${OUTEXT}.csv

echo "hosts with outdated certificates"
sqlite3 -header -csv -separator \; ${DB_FILE} "select distinct  h.date,h.host,h.port,c.subject,c.not_after from hosts h left join last_scan s on (h.host = s.host and h.port = s.port) left join certificates c on (h.fingerprintSHA256 like concat('%',c.fingerprintSHA256,'%')) where c.not_after is not null and c.not_after <  date('now');" | tee ${OUTDIR}/host_expired_certs.${OUTEXT}.csv
