# log_ingestor.py
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Create an SQLite database to store logs
conn = sqlite3.connect('logs.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT,
        message TEXT,
        resourceId TEXT,
        timestamp TEXT,
        traceId TEXT,
        spanId TEXT,
        commit_hash TEXT,
        parentResourceId TEXT
    )
''')
conn.commit()
conn.close()

class LogIngestor(Resource):
    def post(self):
        log_data = request.get_json()

        # Convert timestamp to ISO format
        log_data['timestamp'] = datetime.fromisoformat(log_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('logs.db')
        cursor = conn.cursor()

        # Insert log into the database
        cursor.execute('''
            INSERT INTO logs 
            (level, message, resourceId, timestamp, traceId, spanId, commit_hash, parentResourceId)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_data['level'],
            log_data['message'],
            log_data['resourceId'],
            log_data['timestamp'],
            log_data['traceId'],
            log_data['spanId'],
            log_data['commit'],
            log_data['metadata']['parentResourceId'] if 'metadata' in log_data and 'parentResourceId' in log_data['metadata'] else None
        ))
        
        conn.commit()
        conn.close()
        return {'message': 'Log ingested successfully'}, 201

api.add_resource(LogIngestor, '/ingest')

if __name__ == '__main__':
    app.run(port=3000)
