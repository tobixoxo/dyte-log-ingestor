from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query_params = request.form.to_dict()

    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()

    # Build the query based on the filters
    query = 'SELECT * FROM logs WHERE 1=1'
    params = []
    for key, value in query_params.items():
        if value:
            query += f' AND {key}=?'
            params.append(value)

    # Execute the query
    cursor.execute(query, params)
    result = cursor.fetchall()

    conn.close()

    return render_template('result.html', logs=result)

if __name__ == '__main__':
    app.run(port=5000)
