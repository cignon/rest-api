import urllib.request
import urllib.parse
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

    def __init__(self, base_url, show_debug=False, authorization=None, server_public_key_file=None, app_private_key_file=None):
        if base_url is None:
            raise ValueError("base_url is required")
        
        self.request = None
        self._server_public_key = None
        self._app_private_key = None
        self._authorization = authorization
        self._http_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.show_debug = show_debug
        
        self._base_url = urllib.parse.urljoin(base_url + "/" if not base_url.endswith("/") else base_url, 'api/v1/')

        if server_public_key_file is not None and app_private_key_file is not None:
            self.load_certificates(server_public_key_file, app_private_key_file)


    def login(self, tenant_id, application_id, device_id, user_id):
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

        if self.show_debug:
            pprint (('getToken response:', resp.decode()))

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

        if self.show_debug:
            pprint(('login response:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))

        if resp_json["ErrorCode"] != 0:
            return (False, resp_json, None)

        self.authorization = resp_json["authorization"]
        return (True, resp_json, resp_json["authorization"])


    def logout(self):
        self.set_http_header_authorization()
        req = urllib.request.Request(self._base_url + "auth/logout", headers=self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()

        if self.show_debug:
            pprint(('logout response:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))
        self.authorization = None
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json)

        return (True, resp_json)


    def create_entity(self, new_entity):
        self.set_http_header_authorization()
        req_values = {
            "Entity": new_entity
        }

        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "entity", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()

        if self.show_debug:
            pprint(('post entity:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json)

        return (True, resp_json)
    

    def get_entity(self, req_json):
        self.set_http_header_authorization()

        req_json = json.dumps(req_json).encode("utf-8")
        req = urllib.request.Request(self._base_url + "entity/get", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()

        if self.show_debug:
            pprint(('post entity:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json)

        return (True, resp_json)


    def update_entity(self, update_entity):
        self.set_http_header_authorization()
        req_values = {
            "Entity": update_entity
        }
        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "entity", req_json, self._http_headers, method = "PUT")
        with urllib.request.urlopen(req) as f:
            resp = f.read()

        if self.show_debug:
            pprint(('put entity response:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json)

        return (True, resp_json)


    def upload_file(self, filename_to_upload):
        self.set_http_header_authorization()
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

        if self.show_debug:
            pprint(('upload.initialize response:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))   
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json, None)

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

                if self.show_debug:
                    print("upload.update segment:%i chunk_size:%i" % (segment_index, len(chunk)))

                req = urllib.request.Request(self._base_url + "upload/update", form_body, self._http_headers_w_content_type)
                with urllib.request.urlopen(req) as f:
                    resp = f.read()

                if self.show_debug:
                    pprint(('  upload.update:', resp.decode()))

                resp_json = json.loads(resp.decode('utf-8'))
                if resp_json["ErrorCode"] != 0:
                    return (False, resp_json, None)

        ### 3.3 - Finalize the upload 
        req_values = {
            "UploadId": upload_id,
        }
        req_json = json.dumps(req_values).encode("utf-8")
        req = urllib.request.Request(self._base_url + "upload/finalize", req_json, self._http_headers)
        with urllib.request.urlopen(req) as f:
            resp = f.read()

        if self.show_debug:
            pprint(('upload.finalize response:', resp.decode()))

        resp_json = json.loads(resp.decode('utf-8'))   
        if resp_json["ErrorCode"] != 0:
            return (False, resp_json, None)

        #obtain the documentId required for a Cignon's document field
        document_id = resp_json["DocumentId"]

        return (True, resp_json, document_id)


    def set_http_header_authorization(self):
        #add the authorization token (from login's response) to the http headers to be used in the next calls
        if self._authorization is not None:
            self._http_headers["Authorization"] = "Bearer " + self._authorization
        else:
            raise ValueError("Authorization token is required")

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
    