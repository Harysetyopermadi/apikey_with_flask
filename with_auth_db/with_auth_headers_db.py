from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)
conn_str = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=DB_Covid;UID=hary;PWD=1234'

try:
    conn = pyodbc.connect(conn_str)
    print("koneksi berhasil")
except Exception as e :
    print("koneksi gagal ",e)

def require_api_key(func):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Api-Key')
        if not api_key:
            return jsonify({'error': 'API key is missing.'}), 401

        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE key_auth = ?"
            result = cursor.execute(query, api_key).fetchone()

            if not result:
                return jsonify({'error': 'Invalid API key.'}), 401

            # Optionally, you can pass the associated user_id to the decorated function
            # kwargs['user_id'] = result.user_id

        return func(*args, **kwargs)

    return decorated_function

@app.route('/', methods=['GET'])
@require_api_key
def protected_route():
    # This route is protected and can only be accessed with a valid API key
    
    # Your SQL query to fetch the data
    query = "select * from dt_mart_kasus_covid_harian"

    # Execute the query and fetch the data
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert the data to a list of dictionaries
    data = []
    for row in rows:
        record = {
            'meninggal': row[0],
            'sembuh': row[1],
            'self_isolation': row[2],
            'masih_perawatan': row[3],
            'positif_harian': row[4],
            'batch_date': row[5],
            # Add more columns as needed
        }
        data.append(record)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True ,host='192.168.0.41',port=8080)
