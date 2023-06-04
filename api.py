from flask import Flask, jsonify,request
import pyodbc

server = 'localhost'
database = 'DB_Covid'
username = 'hary'
password = '1234'

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(connection_string)
    print("koneksi berhasil")
except Exception as e :
    print("koneksi gagal ",e)
    
    
#create end point
app = Flask(__name__)


valid_keys = {
    'hary': 'user1',
    'key2': 'user2'
}

@app.route('/', methods=['GET'])

def get_data():
    
    
    # Check if the 'api_key' parameter exists in the request
    if 'api_key' not in request.args:
        return jsonify({'message': 'API key is missing'}), 401

    api_key = request.args['api_key']

    # Validate the API key
    if api_key not in valid_keys:
        return jsonify({'message': 'Invalid API key'}), 401
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