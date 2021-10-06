import urllib.request
import json
import base64
import io
from pprint import pprint
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime

oaep_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )

with open("app1.key", "rb") as key_file:
    app_private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

with open("server1.pub", "rb") as key_file:
    server_public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())


### change to your cignon rest server base url

baseUrl = "http://localhost/CignonRestServer/api/v1/"
http_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

try:
    ## 1 - Get AuthToken
    req_values = {
        "tenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
        "applicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
        "deviceId":"486cc674-b07f-4454-ad53-2435589228ef"
    }

    req_json = json.dumps(req_values).encode("utf-8")
    req = urllib.request.Request(baseUrl + "auth/getToken", req_json, http_headers)
    with urllib.request.urlopen(req) as f:
        resp = f.read()
    pprint(('getToken response:', resp.decode()))
    resp_json = json.loads(resp.decode('utf-8'))
    token = resp_json["token"]

    #decrypt the token using application's private key
    token_encrypted = base64.b64decode(token)
    token_original = app_private_key.decrypt(token_encrypted, oaep_padding);

    #encrypt the token using server's public key
    token_encrypted = server_public_key.encrypt(token_original, oaep_padding);
    token = base64.b64encode(token_encrypted).decode('utf-8')

    ## 2 - Login
    req_values = {
        "tenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
        "applicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
        "token": token,
        "userId": "user1"
    }

    req_json = json.dumps(req_values).encode("utf-8")
    req = urllib.request.Request(baseUrl + "auth/login", req_json, http_headers)
    with urllib.request.urlopen(req) as f:
        resp = f.read()
    pprint(('login response:', resp.decode()))
    resp_json = json.loads(resp.decode('utf-8'))

    authorization = resp_json["authorization"];

    #add the authorization token (from login's response) to the http headers to be used in the next calls
    http_headers["Authorization"] = "Bearer " + authorization;
    
    ## 3 - Create a new Entity

    new_entity = {
      "entityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
      "organizationalUnit":"174BE6FF-4125-4EEC-8A41-6632A218752F",
      "category":"29967816-40BF-4329-A930-2696C0A1938B",
      "title":"my first process",
      "xBool1":True,
      "xDate1":"2021-05-13T00:00:00Z",
      "xDateTime1":"2021-05-21T14:12:09.658Z",
      "xDec1":"123.45",
      "xIntArray1":"1,3,5",
      "xTextArray1":"NJ,CA,TX"
    }

    req_values = {
        "entity": new_entity
    }

    req_json = json.dumps(req_values).encode("utf-8")
    req = urllib.request.Request(baseUrl + "entity", req_json, http_headers)
    with urllib.request.urlopen(req) as f:
        resp = f.read()
    pprint(('post entity:', resp.decode()))
    resp_json = json.loads(resp.decode('utf-8'))

    ## 3 - Update an existing entity using the entity's id from previous call (Create Entity)

    update_entity = {
        "entityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
        "id": resp_json["entity"]["id"],
        "xDateTime1": datetime.utcnow().isoformat(),
        "xInt1": 1,
        "xDec1": 123.456
    }
    req_values = {
        "entity": update_entity
    }

    req_json = json.dumps(req_values).encode("utf-8")
    req = urllib.request.Request(baseUrl + "entity", req_json, http_headers, method = "PUT")
    with urllib.request.urlopen(req) as f:
        resp = f.read()
    pprint(('put entity response:', resp.decode()))
    resp_json = json.loads(resp.decode('utf-8'))

    ## 4 - logout

    req = urllib.request.Request(baseUrl + "auth/logout", headers=http_headers)
    with urllib.request.urlopen(req) as f:
        resp = f.read()
    pprint(('logout response:', resp.decode()))
    resp_json = json.loads(resp.decode('utf-8'))


except Exception as e:
    pprint(e)
