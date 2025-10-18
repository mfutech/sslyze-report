from flask import Flask, jsonify
from flask_cors import CORS

import configparser
from email.mime import message
import sqlite3
import argparse

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
        """SELECT date, host, port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, scan_id, certificate_serial_number, weak_algo 
                   FROM hosts
                   WHERE host = ? AND port = ?
                   ORDER BY date DESC
                   """,
        (host, port),
    )
    rows = cursor.fetchall()
    scans = []
    for row in rows:
        scan = {
            "date": row["date"],
            "sslv2": row["sslv2"],
            "sslv3": row["sslv3"],
            "tls1_0": row["tls1_0"],
            "tls1_1": row["tls1_1"],
            "tls1_2": row["tls1_2"],
            "tls1_3": row["tls1_3"],
            "scan_id": row["scan_id"],
            "certificate_serial_number": row["certificate_serial_number"],
            "weak_algo": row["weak_algo"],
        }
        scans.append(scan)
    return jsonify({"status": "success", "host": host, "port": port, "scans": scans})


@app.route("/api/certificate/<cert_id>", methods=["GET"])
def view_certificate(cert_id):
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute(
        """SELECT max(date) as last_scan, serial_number, subject, public_key_type, not_after, weak_algo  
                   FROM certificates
                   WHERE serial_number = ?
                   GROUP BY serial_number, subject, public_key_type, not_after, weak_algo 
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
        """SELECT max(date) as last_scan, host, port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, weak_algo
                   FROM hosts
                   WHERE certificate_serial_number = ?
                   GROUP by host, port, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, certificate_serial_number, weak_algo
                   """,
        (cert_id,),
    )
    rows = cursor.fetchall()
    hosts = []
    for row in rows:
        host = {
            "host": row["host"],
            "port": row["port"],
            "sslv2": row["sslv2"],
            "sslv3": row["sslv3"],
            "tls1_0": row["tls1_0"],
            "tls1_1": row["tls1_1"],
            "tls1_2": row["tls1_2"],
            "tls1_3": row["tls1_3"],
            "certificate_serial_number": row["certificate_serial_number"],
            "weak_algo": row["weak_algo"],
        }
        hosts.append(host)
    return jsonify({"status": "success", "certificate": certificate, "hosts": hosts})


# sanity check route
@app.route("/api/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


if __name__ == "__main__":
    app.run()
