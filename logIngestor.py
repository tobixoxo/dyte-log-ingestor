# log_ingestor.py
from flask import Flask, request, render_template
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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_params = request.form.to_dict()
    print(query_params.keys)

    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    
    # Build the query based on the filters
    query = 'SELECT * FROM logs WHERE 1=1'
    params = []
    for key, value in query_params.items():
        if value and (key != "startTime") and (key != "endTime"):
            query += f' AND {key}=?'
            params.append(value)
    query += f' AND timestamp BETWEEN \'{query_params["startTime"]}\' AND \'{query_params["endTime"]}\''

    # Execute the query
    print(query)
    cursor.execute(query, params)
    result = cursor.fetchall()

    conn.close()

    return render_template('result.html', logs=result)



if __name__ == '__main__':
    app.run(port=3000)
