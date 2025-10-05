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
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# list certifcates

@app.route('/certificates', methods=['GET'])
def list_certificates():
    db = sqlite3.connect(db_filename)

    cursor = db.cursor()
    cursor.execute("SELECT date, hostname, port, serial_number, subject, public_key_type, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, not_after, weak_algo  FROM certificates")
    rows = cursor.fetchall()
    certificates = []
    for row in rows:
        certificate = {
            'date': row[0],
            'hostname': row[1], 
            'port': row[2],
            'serial_number': row[3],
            'subject': row[4],
            'public_key_type': row[5],
            'sslv2': row[6], 
            'sslv3': row[7],
            'tls1_0': row[8],
            'tls1_1': row[9],
            'tls1_2': row[10],
            'tls1_3': row[11],
            'not_after': row[12],
            'weak_algo': row[13]

        }
        certificates.append(certificate)
    return jsonify({
        'status': 'success',
        'certificates': certificates}
        )

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')




if __name__ == '__main__':

    app.run()
