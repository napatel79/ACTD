import json
import psycopg2
import botocore
import boto3
import borneo
import uuid
import werkzeug
import psycopg2.extras


class InsertData:
    UUID = None
    Contacts = []
    Infected = None

    def setInsertData(self, data):
        try: 
            self.UUID = uuid.UUID(data['UUID'])
            UuidList = eval(data['Contacts'])
            for Uuid in UuidList:
                self.Contacts.append(uuid.UUID(Uuid))
            self.Infected = bool(data['Infected'])
        except Exception as e:
            raise e

def insertData(input_json):
    try:
        data = json.dumps(input_json)
        data = json.loads(data)
        insertData = InsertData()
        insertData.setInsertData(data)
        try:
            # Create a connection to the database
            conn = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="admin",
                password="admin125"
            )
            cur = conn.cursor()
            psycopg2.extras.register_uuid()
            print(type(insertData.UUID))
            
            print(insertData.Infected)
            cur.execute("INSERT INTO devices (UUID, Infected) VALUES(%s, %s)", (insertData.UUID, insertData.Infected))
            conn.commit() 
            cur.close()
            conn.close()

        except Exception as e:
            print(e)
            print("something went wrong")
            raise "cannot connect/make quries to DataBase"
            
    except werkzeug.exceptions.BadRequest:
        raise werkzeug.exceptions.BadRequest("Incorrect Request Parameters")
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError(e)
