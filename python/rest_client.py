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
from multipart_formdata_encoder import MultipartFormdataEncoder
import os
import pathlib

class CignonRestClient:

    def __init__(self, base_url):
        self._server_public_key = None
        self._app_private_key = None
        self._base_url = base_url
        self._authorization = None
        self._http_headers = {}

    def load_certificates(self, server_public_key_file, app_private_key_file):
        with open(server_public_key_file, "rb") as key_file:
            self._server_public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
        with open(app_private_key_file, "rb") as key_file:
            self._app_private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

    def read_file_chunks(self, file, chunk_size):
        index = -1
        while True:
            index += 1
            bytes = file.read(chunk_size)
            if not bytes:
                break
            yield (index, bytes)


    def logout(self):
        req = urllib.request.Request(self._base_url + "auth/logout", headers=self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('logout response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))
        return True;


    def login(self, tenant_id, application_id, device_id, user_id):
        self._http_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.authorization = None

        ## 1 - Get AuthToken

        req_values = {
            "TenantId": tenant_id,
            "ApplicationId": application_id,
            "DeviceId": device_id
        }

        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "auth/getToken", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('getToken response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))

        if resp_json["ErrorCode"] != 0:
            return False

        token = resp_json["Token"]

        oaep_padding = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None)

        #decrypt the token using application's private key
        token_encrypted = base64.b64decode(token)
        token_original = self._app_private_key.decrypt(token_encrypted, oaep_padding);

        #encrypt the token using server's public key
        token_encrypted = self._server_public_key.encrypt(token_original, oaep_padding);
        token = base64.b64encode(token_encrypted).decode('utf-8')

        ## 2 - Login
        req_values = {
            "TenantId": tenant_id,
            "ApplicationId": application_id,
            "Token": token,
            "UserId": user_id
        }

        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "auth/login", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('login response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return False

        self.authorization = resp_json["authorization"];

        #add the authorization token (from login's response) to the http headers to be used in the next calls
        self._http_headers["Authorization"] = "Bearer " + self.authorization;
        
        return True


    def upload_file(self, filename_to_upload):
        ## 1 - Initialize a new upload 
        req_values = {
            "Name": pathlib.Path(filename_to_upload).stem,
            "ContentExtension": pathlib.Path(filename_to_upload).suffix[1:], # extension without "."
            "ContentLength": os.path.getsize(filename_to_upload)
        }
        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "upload/initialize", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('upload.initialize response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))   
        if resp_json["ErrorCode"] != 0:
            return False

        #obtain the UploadId required for upload.update and upload.finalize
        upload_id = resp_json["UploadId"]

        ### 3.2 - Start uploading file chunks, max chunk size is 1 MB (1024 * 1024)

        with open("the_official_github_training_manual.pdf", "rb") as file:
            for (segment_index, chunk) in self.read_file_chunks(file, 1024 * 1024):
                form_fields = {
                    "Action": "append",
                    "UploadId": upload_id,
                    "SegmentIndex": segment_index,
                    "Data": chunk
                }

                content_type, form_body = MultipartFormdataEncoder().encode(form_fields, [])
                self._http_headers_w_content_type = dict(self._http_headers)
                self._http_headers_w_content_type["Content-Type"] = content_type;

                print("upload.update segment:%i chunk_size:%i" % (segment_index, len(chunk)))

                req = urllib.request.Request(self._base_url + "upload/update", form_body, self._http_headers_w_content_type)
                with urllib.request.urlopen(req) as f:
                    resp = f.read()
                pprint(('  upload.update:', resp.decode()))
                resp_json = json.loads(resp.decode('utf-8'))
                if resp_json["ErrorCode"] != 0:
                    return False

        ### 3.3 - Finalize the upload 
        req_values = {
            "UploadId": upload_id,
        }
        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "upload/finalize", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('upload.finalize response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))   
        if resp_json["ErrorCode"] != 0:
            return False

        #obtain the documentId required for a Cignon's document field
        document_id = resp_json["DocumentId"]

        return (True, document_id)


    def create_entity(self, new_entity):
        req_values = {
            "Entity": new_entity
        }

        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "entity", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('post entity:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return False

        return (True, resp_json["Entity"])


    def update_entity(self, update_entity):
        req_values = {
            "Entity": update_entity
        }
        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "entity", req_json, self._http_headers, method = "PUT")
        with urllib.request.urlopen(req) as f:
            resp = f.read()
        pprint(('put entity response:', resp.decode()))
        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return False

        return (True, resp_json["Entity"])


try:
    # change to your cignon rest server base url
    client = CignonRestClient("http://localhost/CignonRestServer/api/v1/")

    client.load_certificates(server_public_key_file = "server1.pub", 
                             app_private_key_file = "app1.key")

    success = client.login(tenant_id = "1d1a71ac-7b18-42ec-b916-279a83854384",
                 application_id = "26a8e742-3564-4503-af18-5445a2c0091e",
                 device_id = "486cc674-b07f-4454-ad53-2435589228ef",
                 user_id = "user1")

    (success, document_id) = client.upload_file("the_official_github_training_manual.pdf") 

    entity_to_create = {
        "EntityTypeId" : "F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
        "OrganizationalUnit" : "174BE6FF-4125-4EEC-8A41-6632A218752F",
        "Category": "29967816-40BF-4329-A930-2696C0A1938B",
        "Title": "my first process",
        "xBool1": True,
        "xDate1": "2021-05-13T00:00:00Z",
        "xDateTime1": "2021-05-21T14:12:09.658Z",
        "xDec1": "123.45",
        "xIntArray1": [ "1", "3", "5"],
        "xTextArray1": [ "NJ", "CA", "TX"],

        #add 2 detail entities
        "xDocuments1": [
            {
                "xInt1": 123,
                "xText1": "detail entity 1",
            },
            {
                "xInt1": 456,
                "xText1": "detail entity 2",
            }
        ]
    }

    (success, new_entity) = client.create_entity(entity_to_create)

    entity_to_update1 = {
            "EntityTypeId": entity_to_create["EntityTypeId"],
            "Id": new_entity["Id"],
            "xDateTime1": datetime.utcnow().isoformat(),
            "xInt1": 1,
            "xDec1": 123.456,
            "xDocuments1": [
                    {
                        #to update a detail entity we need to use the id returned 
                        "Id" : new_entity["xDocuments1"][0]["Id"],
                        "xDocument1": document_id,
                        "xText1": "detail 1 was updated"
                    },
                    {
                        "xInt1": 789,
                        "xText1": "detail entity 3 (new)",
                    }
                ]
        }
    (success, updated_entity1) = client.update_entity(entity_to_update1)

    entity_to_update2 = {
            "EntityTypeId": entity_to_create["EntityTypeId"],
            "Id": new_entity["Id"],
            "xDocuments1": [
                    {
                        #to update a detail entity we need to use the id returned 
                        "Id" : updated_entity1["xDocuments1"][-1]["Id"],
                        "xDocument1": document_id,
                        "xText1": "detail 3 was updated"
                    },
                ]
        }
    (success, updated_entity2) = client.update_entity(entity_to_update2)


except Exception as e:
    pprint(e)





        
