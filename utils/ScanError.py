class ScanError():
    def __init__(self, database):
        self.db = database

    def log(self, message, host = None, port = None):


        self.db.execute(
            "INSERT INTO scan_errors (hostname, port, error_message) VALUES (?, ?, ?)",
            (
                host,
                port, 
                message,
            ),
        )
        self.db.commit()