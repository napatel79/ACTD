from flask import Flask, render_template, request, url_for, jsonify, abort
import psycopg2
import requests
import DeviceService
import botocore
import boto3
import borneo
import json
import werkzeug



app = Flask(__name__)

# Create a connection to the database
conn = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="admin",
    password="admin125"
)

def handleException(e):
    try :
        raise e
    except werkzeug.exceptions.BadRequest as e:
        print(e)
        return abort(400, e)
    except werkzeug.exceptions.InternalServerError as e:
        print(e)
        return abort(500, e)

@app.route('/insert', methods=['post'])
def insert_data():
    try :
        input_json = request.get_json(force=True) 
        DeviceService.insertData(input_json)
        return jsonify("good")
    except Exception as e:
        handleException(e)


# @app.route('/data')
# def get_data():
#     # Open a cursor to perform database operations
#     cur = conn.cursor()

#     # Execute a query
#     cur.execute("SELECT * users")

#     # Fetch all rows as a list of tuples
#     data = cur.fetchall()

#     # Close the cursor and connection
#     cur.close()
#     conn.close()

#     # Convert the data to a JSON response
#     return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
