import dotenv 
import os
import json
import argparse
from pprint import pprint
from cignon_rest_client import CignonRestClient

parser = argparse.ArgumentParser("entity_update")
parser.add_argument("--filename", help="A filename containing the json to update an entity/process.")
parser.add_argument("--debug", help="show debug information")
parser.add_argument("--ModifiedTimestamp", help="Modified Timestamp to replace the json file's ModifiedTimestamp.") 
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

with open(args.filename) as json_file:
    json_data = json.load(json_file)

if args.ModifiedTimestamp:
    json_data["ModifiedTimestamp"] = args.ModifiedTimestamp

(success, update_response) = client.update_entity(json_data)

if success:
    print("SUCCESS Response:\n" + json.dumps(update_response, indent=2))
else:
    print(f">>>> ERROR Response:\n" + json.dumps(update_response, indent=2))
