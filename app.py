from flask import Flask, jsonify
from flask_cors import CORS

import configparser
from email.mime import message
import sqlite3
import argparse
import json
import re

CONFIGFILE = "config.ini"
DEFAULT_DB = "data/sslyze_report.db"
DEFAULT_ERROR_LOG = "data/error.log"


# read configuration file
config = configparser.ConfigParser()
config.read(CONFIGFILE)

# connect to the database
db_filename = config.get("sqlite", "db_path", fallback=DEFAULT_DB)


# instantiate the app
app = Flask(
    __name__,
    static_url_path="/",
    static_folder="./client/dist",
)

app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# list certifcates
@app.route("/api/certificates", methods=["GET"])
def list_certificates():
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """
SELECT c.date as last_scan, c.serial_number, c.fingerprintSHA256, c.subject, c.public_key_type, c.not_after, count(h.host) as nb_host,
    c.not_before

from certificates c
        join hosts h on ( INSTR(h.fingerprintSHA256, c.fingerprintSHA256) > 0 )
        join last_scan s on (s.scan_id = h.scan_id and s.host = h.host and s.port = h.port)

group by c.serial_number, c.fingerprintSHA256, c.subject, c.public_key_type, c.not_after
order by nb_host DESC
"""
    )
    rows = cursor.fetchall()
    certificates = []
    for row in rows:
        certificate = {
            "date": row["last_scan"],
            "serial_number": row["serial_number"],
            "subject": row["subject"],
            "public_key_type": row["public_key_type"],
            "not_after": row["not_after"],
            "not_before": row["not_before"],
            "nb_host": row["nb_host"],
            "fingerprint": row["fingerprintSHA256"],
        }
        certificates.append(certificate)
    return jsonify({"status": "success", "certificates": certificates})


@app.route("/api/host/<host>/<port>", methods=["GET"])
def view_host(host, port):

    host = sanize_input(host)
    port = sanize_input_int(port)

    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    cursor.execute(
        """ SELECT date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, 
            mozilla_old, mozilla_intermediate, mozilla_modern, fingerprintSHA256
            FROM hosts h
                   WHERE host = ? AND port = ?
                   ORDER BY date DESC
                   """,
        (host, port),
    )
    rows = cursor.fetchall()
    scans = []
    for row in rows:
        scan = {
            "date": row["last_scan"],
            "host": row["host"],
            "port": row["port"],
            "sslv2": json.loads(row["sslv2"]),
            "sslv3": json.loads(row["sslv3"]),
            "tls1_0": json.loads(row["tls1_0"]),
            "tls1_1": json.loads(row["tls1_1"]),
            "tls1_2": json.loads(row["tls1_2"]),
            "tls1_3": json.loads(row["tls1_3"]),
            "moz_old": json.loads(row["mozilla_old"]),
            "moz_intermediate": json.loads(row["mozilla_intermediate"]),
            "moz_modern": json.loads(row["mozilla_modern"]),
            "certificate_serial_number": [
                f"{c}" for c in json.loads(row["certificate_serial_number"])
            ],
            "certificate_fingerprint": json.loads(row["fingerprintSHA256"]),
        }
        scans.append(scan)
    return jsonify({"status": "success", "host": host, "port": port, "scans": scans})


@app.route("/api/hosts", methods=["GET"])
def list_hosts():
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """ SELECT date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, 
            certificate_serial_number, mozilla_old, mozilla_intermediate, mozilla_modern,
            fingerprintSHA256
            FROM hosts h
            INNER JOIN  last_scan s
            ON  h.scan_id = s.scan_id AND h.host = s.host AND h.port = s.port
        """
    )
    rows = cursor.fetchall()
    hosts = []
    for row in rows:
        host = {
            "date": row["last_scan"],
            "host": row["host"],
            "port": row["port"],
            "sslv2": json.loads(row["sslv2"]),
            "sslv3": json.loads(row["sslv3"]),
            "tls1_0": json.loads(row["tls1_0"]),
            "tls1_1": json.loads(row["tls1_1"]),
            "tls1_2": json.loads(row["tls1_2"]),
            "tls1_3": json.loads(row["tls1_3"]),
            "moz_old": json.loads(row["mozilla_old"]),
            "moz_intermediate": json.loads(row["mozilla_intermediate"]),
            "moz_modern": json.loads(row["mozilla_modern"]),
            "certificate_serial_number": json.loads(row["certificate_serial_number"]),
            "certificate_fingerprint": json.loads(row["fingerprintSHA256"]),
        }
        hosts.append(host)
    return jsonify({"status": "success", "hosts": hosts})


@app.route("/api/certificate/<cert_id>", methods=["GET"])
def view_certificate(cert_id):

    cert_id = sanize_input(cert_id)

    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """SELECT c.date as last_scan, serial_number, subject, public_key_type, not_after, weak_algo, fingerprintSHA256,
                    not_before
                   FROM certificates c INNER JOIN last_scan s ON c.scan_id = s.scan_id
                   WHERE fingerprintSHA256 = ?
                   """,
        (cert_id,),
    )
    row = cursor.fetchone()
    certificate = {
        "date": row["last_scan"],
        "serial_number": row["serial_number"],
        "subject": row["subject"],
        "public_key_type": row["public_key_type"],
        "not_after": row["not_after"],
        "fingerprint": row["fingerprintSHA256"],
        "not_before": row["not_before"],
    }
    cursor.execute(
        """SELECT h.date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, 
                   certificate_serial_number, mozilla_old, mozilla_intermediate, mozilla_modern, fingerprintSHA256
                   FROM hosts h 
                   WHERE fingerprintSHA256 like ?
                   ORDER BY h.date ASC
                   """,
        (f'%"{cert_id}"%',),
    )
    rows = cursor.fetchall()
    hosts = []
    for row in rows:
        host = {
            "date": row["last_scan"],
            "host": row["host"],
            "port": row["port"],
            "sslv2": json.loads(row["sslv2"]),
            "sslv3": json.loads(row["sslv3"]),
            "tls1_0": json.loads(row["tls1_0"]),
            "tls1_1": json.loads(row["tls1_1"]),
            "tls1_2": json.loads(row["tls1_2"]),
            "tls1_3": json.loads(row["tls1_3"]),
            "moz_old": json.loads(row["mozilla_old"]),
            "moz_intermediate": json.loads(row["mozilla_intermediate"]),
            "moz_modern": json.loads(row["mozilla_modern"]),
            "certificate_serial_number": json.loads(row["certificate_serial_number"]),
            "certificate_fingerprint": json.loads(row["fingerprintSHA256"]),
        }
        hosts.append(host)
    return jsonify(
        {
            "status": "success",
            "certificate": certificate,
            "hosts": hosts,
            "other_info": f'"{cert_id}"',
        }
    )


# sanity check route
@app.route("/api/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


def sanize_input(input_str):
    # Simple sanitization keep only ascii aplhabetic, numeric, dot and dash characters
    res = input_str.encode("ascii", "ignore").decode("ascii")
    res = re.sub(r"[^0-9A-Za-z.-]", "", res)
    return res


def sanize_input_int(input_str):
    # Simple sanitization keep only numeric
    res = input_str.encode("ascii", "ignore").decode("ascii")
    res = re.sub(r"[^0-9]", "", res)
    return res


if __name__ == "__main__":
    app.run()
