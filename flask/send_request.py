import requests
import uuid
import json


PATH = 'http://127.0.0.1:5000'

UuidList = []
for i in range(4):
    UuidList.append(str(uuid.uuid4()))


r = requests.post(PATH + '/insert', json={
  "UUID": str(uuid.uuid4()),
  "Contacts": str(UuidList),
  "Infected": True,
})
try :
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
except:
    print(f"Status Code: {r.status_code, r.content}")