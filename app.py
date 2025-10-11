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
app = Flask(__name__,
            static_url_path='/', 
            static_folder='./client/dist',
)

app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# list certifcates

@app.route('/api/certificates', methods=['GET'])
def list_certificates():
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute("""SELECT max(date) as last_scan, hostname, port, serial_number, subject, public_key_type, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, not_after, weak_algo  
                   FROM certificates
                   GROUP BY hostname, port, serial_number, subject, public_key_type, sslv2, sslv3, tls1_0, tls1_1, tls1_2, tls1_3, not_after, weak_algo 
                   """)
    rows = cursor.fetchall()
    certificates = []
    for row in rows:
        certificate = {
            'date': row['last_scan'],
            'hostname': row['hostname'], 
            'port': row['port'],
            'serial_number': row['serial_number'],
            'subject': row['subject'],
            'public_key_type': row['public_key_type'],
            'sslv2': row['sslv2'],
            'sslv3': row['sslv3'],
            'tls1_0': row['tls1_0'],
            'tls1_1': row['tls1_1'],
            'tls1_2': row['tls1_2'],
            'tls1_3': row['tls1_3'],
            'not_after': row['not_after'],
            'weak_algo': row['weak_algo']
        }
        certificates.append(certificate)
    return jsonify({
        'status': 'success',
        'certificates': certificates}
        )



@app.route('/api/host/<host>/<port>', methods=['GET'])
def view_host(host, port):
    db = sqlite3.connect(db_filename)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute("""SELECT date, host, port, scan_started, scan_completed, scan_result_json, scan_id
                   FROM host_details
                   WHERE host = ? AND port = ?
                   """, (host, port))
    row = cursor.fetchone()
    host_details = {
            'date': row['date'],
            'host': row['host'],
            'port': row['port'],
            'scan_started': row['scan_started'],
            'scan_completed': row['scan_completed'],
            'scan_result_json': row['scan_result_json'],
            'scan_id': row['scan_id']
        }
    return jsonify({
        'status': 'success',
        'hostDetails': host_details}
    )



# sanity check route
@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')




if __name__ == '__main__':
    app.run()
