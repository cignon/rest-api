import dotenv 
import os
import json
import argparse
from pprint import pprint
from cignon_rest_client import CignonRestClient

parser = argparse.ArgumentParser("document_upload")
parser.add_argument("--filename", help="document file to upload")
parser.add_argument("--debug", help="show debug information")
args = parser.parse_args()

if not args.filename:
    parser.error('--filename is required.')

dotenv.load_dotenv()

client = CignonRestClient(base_url = os.getenv("cignon_rest_server_url")
                          ,server_public_key_file = os.getenv("cignon_rest_server_public_key_file")
                          ,app_private_key_file = os.getenv("cignon_rest_app_private_key_file")
                          ,authorization = os.getenv("login_response_authorization")
                          ,show_debug=args.debug
                         )

(success, upload_response, document_id) = client.upload_file(args.filename) 

if success:
    print("SUCCESS Response:\n" + json.dumps(upload_response, indent=2))
else:
    print(f">>>> ERROR Response:\n" + json.dumps(upload_response, indent=2))


