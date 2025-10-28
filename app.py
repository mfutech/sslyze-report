from flask import Flask, jsonify
from flask_cors import CORS

import configparser
from email.mime import message
import sqlite3
import argparse
import json

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
        """SELECT max(date) as last_scan, serial_number, subject, public_key_type, not_after, weak_algo  
                   FROM certificates
                   GROUP BY serial_number, subject, public_key_type, not_after, weak_algo 
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
            "weak_algo": row["weak_algo"],
        }
        certificates.append(certificate)
    return jsonify({"status": "success", "certificates": certificates})


@app.route("/api/host/<host>/<port>", methods=["GET"])
def view_host(host, port):
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()

    cursor.execute(
        """ SELECT date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, mozilla_old, mozilla_intermediate, mozilla_modern
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
        }
        scans.append(scan)
    return jsonify({"status": "success", "host": host, "port": port, "scans": scans})


@app.route("/api/hosts", methods=["GET"])
def list_hosts():
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """ SELECT date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, mozilla_old, mozilla_intermediate, mozilla_modern
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
        }
        hosts.append(host)
    return jsonify({"status": "success", "hosts": hosts})


@app.route("/api/certificate/<cert_id>", methods=["GET"])
def view_certificate(cert_id):
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """SELECT c.date as last_scan, serial_number, subject, public_key_type, not_after, weak_algo  
                   FROM certificates c INNER JOIN last_scan s ON c.scan_id = s.scan_id
                   WHERE serial_number = ?
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
        "weak_algo": row["weak_algo"],
    }
    cursor.execute(
        """SELECT h.date as last_scan, h.host, h.port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, mozilla_old, mozilla_intermediate, mozilla_modern
                   FROM hosts h 
                   WHERE certificate_serial_number like ?
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


if __name__ == "__main__":
    app.run()
