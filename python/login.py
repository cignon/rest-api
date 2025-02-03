from cignon_rest_client import CignonRestClient
import dotenv 
import os
import json

dotenv.load_dotenv()

client = CignonRestClient(os.getenv("cignon_rest_server_url"))

client.load_certificates(server_public_key_file = os.getenv("cignon_rest_server_public_key_file")
                         , app_private_key_file = os.getenv("cignon_rest_app_private_key_file")
                         )

(success, login_response, authorization) = client.login(tenant_id = os.getenv("cignon_rest_tenant_id")
                 , application_id = os.getenv("cignon_rest_application_id")
                 , device_id = os.getenv("cignon_rest_device_id")
                 , user_id = os.getenv("cignon_rest_application_user_id")
                 )

if success:
    print("SUCCESS Response:\n" + json.dumps(login_response, indent=2))
    os.environ["login_response_authorization"] = authorization
    dotenv_file = dotenv.find_dotenv()
    print(f"authorization saved to file: {dotenv_file}")
    dotenv.set_key(dotenv_file, "login_response_authorization", os.environ["login_response_authorization"])
else:
    print(f">>>> ERROR Response:\n" + json.dumps(login_response, indent=2))




