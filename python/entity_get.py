import dotenv 
import os
import json
import argparse
from pprint import pprint
from cignon_rest_client import CignonRestClient

parser = argparse.ArgumentParser("entity_get")
parser.add_argument("--id", help="Entity/Process Id to get.")
parser.add_argument("--filename", help="json details to get an entity/process.")
parser.add_argument("--debug", help="show debug information")
args = parser.parse_args()

if not (args.id or args.filename):
    parser.error('At least one of --id or --filename is required.')

dotenv.load_dotenv()

client = CignonRestClient(base_url = os.getenv("cignon_rest_server_url")
                          ,server_public_key_file = os.getenv("cignon_rest_server_public_key_file")
                          ,app_private_key_file = os.getenv("cignon_rest_app_private_key_file")
                          ,authorization = os.getenv("login_response_authorization")
                          ,show_debug=args.debug
                         )

if args.filename:
    with open(args.filename) as json_file:
        json_data = json.load(json_file)
else:
    json_data = {
        "Id": args.id
    }

(success, get_response) = client.get_entity(json_data)

if success:
    print("SUCCESS Response:\n" + json.dumps(get_response, indent=2))
else:
    print(f">>>> ERROR Response:\n" + json.dumps(get_response, indent=2))