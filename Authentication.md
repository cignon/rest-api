# Authentication

The authentication from the external application to CIGNON is performed in two steps: 
* External Application calls **getToken** providing the applicationId, tenantId, deviceId, the server creates a encrypted token using the application public key.
* Application decrypts the token using the private key and encrypts the token using the server's public key then calls **login** providing the encrypted token, applicationId, tenantId and the userId in return the server returns the authentication token to be used with further interactions requiring an authentication token.

## Routes

| Method      | Route                      | Used for                  |
| ----------- | ---------------------------| ------------------------- |
| `POST`      | `/api/v1/auth/getToken`    | get authentication token  |
| `POST`      | `/api/v1/auth/login`       | login                     |

## Get Token

The **getToken** request is used to obtain an application authentication token, the token will be valid for a **specific time window** and will be **disabled** after being used in a **login** request. It returns a **Token** encrypted with the application's public key, which should be used in a **single** **login** request. 

Example:

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/auth/getToken

Request:
```json
{
   "TenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
   "ApplicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
   "DeviceId":"486cc674-b07f-4454-ad53-2435589228ef"
}
```

### Required Parameters:

| Name               | Description                      | Example          |
| ------------------ | ---------------------------------| -----------------|
| `TenantId`         | Tenant Globally Unique IDentifier      | 1d1a71ac-7b18-42ec-b916-279a83854384       |
| `ApplicationId`    | Application Globally Unique IDentifier   | 26a8e742-3564-4503-af18-5445a2c0091e              |
| `DeviceId`         | An Globally Unique IDentifier representing the client's is up to the application to provide one  | 486cc674-b07f-4454-ad53-2435589228ef          |

Response:
```json
{
   "Token":"bm9cUAUlQdETTkEtLB2PQ2QRveUJz7I6DIhEIoOI+XyptMw9BVeGyOMXcsPadpW....jQuoV44sWjmuMWanJd5tHk0Ibpw4=",
   "ErrorCode":"0"
}
```
* **Token** base 64 token encrypted using the application public key. External application needs the private key to decrypt the token.

* * *

## Login

The **login** request is used to login the application on behalf's of a **UserId**. It returns an **Authorization** header token which should be used to execute all subsequent API requests. The session token is valid for a **specific time window**.

Example:

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/auth/login

Example:

Request:
```json
{
   "TenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
   "ApplicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
   "Token":"a6BQotqx0Wx8q8uLZq+5nNcc0krDPa7OgBXa+TT6WETSTlI53cPLYl9u1Gnm5vLVQ5.....ZRJirRtvYkfvaOP6nmEizm4kgaW/9McBQQV3G6WlQMuhc1rY/XlIHNXU=",
   "UserId":"user1"
}
```

### Required Parameters:

| Name               | Description                      |
| ------------------ | ---------------------------------|
| `TenantId`         | Tenant Globally Unique IDentifier      |
| `ApplicationId`    | Application Globally Unique IDentifier   |
| `Token`         | Token obtained from **getToken** encrypted with the server's public key and encoded to based 64  |
| `UserId`    | A string identifier used to identify the Cignon User. |

Response:
```json
{
   "Authorization":"AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=",
   "ErrorCode":"0"
}
```
* **authorization** authorization token to be used as http request header.

* * *

