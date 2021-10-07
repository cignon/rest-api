# Introduction

Welcome to the CIGNON platform REST API. 

This REST API is the connectivity methodology to develop integrations between CIGNON and other applications. This documents the REST resources available in CIGNON Server platform, along with expected HTTP response codes and sample requests. 

The REST API interface provides a simple way for external applications interface to Cignon by making HTTP requests.

## Introduction to Cignon REST APIS

The access to resources is provided via URL paths. To use a REST API, External applications will make HTTP requests and parse the responses.

All requests calls and responses to Cignon endpoint are made in JSON format, unless other format are expected for specific endpoint which you can find in the documentation.

Cignon REST API is based on open standards like [JSON-Schema](http://json-schema.org/) (for data validation). Any web development language can work with the API.

## Pre-requisites

Is required to have the following information up-front :

* The main url path to the Cignon REST Server 
* Cignon Rest Server RSA public key
* Tenant Id 
* Application Id 
* Client/Application RSA private key

## Initial setup

First step, is to authenticate your application. 

Is required to submit the external application public key to the Cignon infrastructure administrator

The authentication relies exclusivelyy on external (application) RSA private key (only known to by external application owner).

### 1. Generate private key for your application

```shell
openssl genrsa -out my_application_private.key 4096
openssl rsa -in my_application_private.key -pubout -out my_application_public.pub
```

### 2. Cignon backend configuration

Submit external application public key **my_application_public.pub** to the Cignon IT Admin, and in return CIGNON will provide, the following information:
* **Api base url** e.g. https://foobar.cignon.com/CignonRestServer 
* **Application Id** e.g. 26a8e742-3564-4503-af18-5445a2c0091e
* **Tenant Id** e.g. 1d1a71ac-7b18-42ec-b916-279a83854384
* list of **UserId**s that your application is authorized to use e.g. user1, user2, user3
* Cignon REST Server public key **cignon_rest_server.pub** (PEM text format)
* Cignon REST Server certificate **cignon_rest_server_no_key.pfx** (can be imported to a certificate store)

### 3. API

## Routes

| Method      | Route                      | Used for                  |
| ----------- | ---------------------------| ------------------------- |
| `POST`      | `/api/v1/auth/getToken`    | get authentication token  |
| `POST`      | `/api/v1/auth/login`       | login                     |
| `GET`       | `/api/v1/auth/logout`      | logout                    |
| `POST`      | `/api/v1/upload/initialize`| initialize a new upload   |
| `POST`      | `/api/v1/upload/update`    | upload chunk              |
| `POST`      | `/api/v1/upload/finalize`  | finalize an upload        |
| `POST`      | `/api/v1/entity`           | create entity or process  |
| `PUT`       | `/api/v1/entity`           | update entity or process  |

* * *

## Authentication

The authentication from the external application to CIGNON is performed in two steps: 
* External Application calls **getToken** providing the applicationId, tenantId, deviceId, the server creates a encrypted token using the application public key.
* Application decrypts the token using the private key and encrypts the token using the server's public key then calls **login** providing the encrypted token, applicationId, tenantId and the userId in return the server returns the authentication token to be used with further interactions requiring an authentication token.

* * *

### Get Token

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/auth/getToken

request:
```json
{
   "tenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
   "applicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
   "deviceId":"486cc674-b07f-4454-ad53-2435589228ef"
}
```
* **deviceId** is an unique identifier (GUID) representing the client machine and is meaningless for the Cignon REST server. 

response:
```json
{
   "token":"bm9cUAUlQdETTkEtLB2PQ2QRveUJz7I6DIhEIoOI+XyptMw9BVeGyOMXcsPadpW....jQuoV44sWjmuMWanJd5tHk0Ibpw4=",
   "errorCode":"0"
}
```
* **token** base 64 token encrypted using the application public key. External application needs the private key to decrypt the token.

* * *

### Login

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/auth/login

request:
```json
{
   "tenantId":"1d1a71ac-7b18-42ec-b916-279a83854384",
   "applicationId":"26a8e742-3564-4503-af18-5445a2c0091e",
   "token":"a6BQotqx0Wx8q8uLZq+5nNcc0krDPa7OgBXa+TT6WETSTlI53cPLYl9u1Gnm5vLVQ5.....ZRJirRtvYkfvaOP6nmEizm4kgaW/9McBQQV3G6WlQMuhc1rY/XlIHNXU=",
   "userId":"user1"
}
```
* **token** previous token obtained from getToken encrypted with the server's public key and encoded to based 64.

response:
```json
{
   "authorization":"AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=",
   "errorCode":"0"
}
```
* **authorization** authorization token to be used as http request header.

* * *

### Logout

`GET` https://foobar.cignon.com/CignonRestServer/api/v1/auth/logout

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
response:
```json
{
   "errorCode":"0"
}
```
* * *

### Upload Document (Initialize)

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/initialize

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
request:
```json
{
   "Name":"Hello World",
   "ContentExtension":"txt",
   "ContentLength": 18
}
```

response:
```json
{
   "UploadId":"1153EF2374-C6B659870B-10F30A6AE8-930133ED91",
   "ErrorCode":0
}
```
* * *

### Upload Document (Update/Append)

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/update

request:
```http request
POST http://nuci7/CignonRestServer/api/v1/upload/update HTTP/1.1
Accept: application/json
Authorization: Bearer AgEcAIMnP7A0idlIg9Fg/3HmOkW6b+6upXqFpEexapk=
Content-Type: multipart/form-data; boundary="21cb210a-5f60-4bf7-a458-8fe981ca3d04"
Host: nuci7
Content-Length: 592
Expect: 100-continue

--21cb210a-5f60-4bf7-a458-8fe981ca3d04
Content-Type: text/plain; charset=utf-8
Content-Disposition: form-data; name=Action

append
--21cb210a-5f60-4bf7-a458-8fe981ca3d04
Content-Type: text/plain; charset=utf-8
Content-Disposition: form-data; name=UploadId

1153EF2374-C6B659870B-10F30A6AE8-930133ED91
--21cb210a-5f60-4bf7-a458-8fe981ca3d04
Content-Type: text/plain; charset=utf-8
Content-Disposition: form-data; name=SegmentIndex

0
--21cb210a-5f60-4bf7-a458-8fe981ca3d04
Content-Disposition: form-data; name=Data

Hello World !!! 
--21cb210a-5f60-4bf7-a458-8fe981ca3d04--
```

response:
```json
{
   "ErrorCode":0
}
```

* * *

### Upload Document (Finalize)

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/finalize

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
request:
```json
{
   "UploadId":"1153EF2374-C6B659870B-10F30A6AE8-930133ED91"
}
```

response:
```json
{
   "DocumentId":"78f4ef9a-abee-429c-9352-01a56bada878",
   "ErrorCode":0
}
```

* * *

### Create entity or process

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/entity

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
request:
```json
{
   "Entity":{
      "EntityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
      "OrganizationalUnit":"174BE6FF-4125-4EEC-8A41-6632A218752F",
      "Category":"29967816-40BF-4329-A930-2696C0A1938B",
      "Title":"my first process",
      "xBool1":true,
      "xDate1":"2021-05-13T00:00:00Z",
      "xDateTime1":"2021-07-04T01:49:23.8039368Z",
      "xDec1":123.45,
      "xIntArray1":[
         1,
         3,
         5
      ],
      "xTextArray1":[
         "NJ",
         "CA",
         "TX"
      ],
      "xDocuments1":[
         {
            "xInt1":123,
            "xText1":"detail entity 1"
         },
         {
            "xInt1":456,
            "xText1":"detail entity 2"
         }
      ]
   }
}
```
* **entityTypeId** Cignon process type or master entity type identifier **required** 
* **organizationalUnit** Cignon Organizational Unit identifier  **required** 
* **category** Process Type's Category identifier **required for process**
* **title** Entity or Process's title **required**

**Important** : Any other required fields (defined on CIGNON Process Type/Master Entity Type configuration) need to be sent. 

response:
```json
{
   "Entity":{
      "Id":"8fb17ba4-cb7e-468d-8e7d-837ef94f76b9",
      "xDocuments1":[
         {
            "Id":"5eff95ba-240f-4a0e-ae76-d1f106e34e87"
         },
         {
            "Id":"87d54ee8-2a88-4393-a6b3-1eb4076c16f0"
         }
      ]
   },
   "ErrorCode":0
}
```
* **id** new process or entity's id 

* * *

### Update entity or process

`PUT` https://foobar.cignon.com/CignonRestServer/api/v1/entity

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
request:
```json
{
   "Entity":{
      "EntityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
      "Id":"8fb17ba4-cb7e-468d-8e7d-837ef94f76b9",
      "xDateTime1":"2021-07-09T01:49:25.2636807Z",
      "xInt1":"1",
      "xDocuments1":[
         {
            "Id":"5eff95ba-240f-4a0e-ae76-d1f106e34e87",
            "xDocument1":"78f4ef9a-abee-429c-9352-01a56bada878",
            "xText1":"detail 1 was updated"
         },
         {
            "xInt1":789,
            "xText1":"detail entity 3"
         }
      ]
   }
}
```
* **entityTypeId** Cignon process type or master entity type identifier **required** 
* **id** entity or process's id to be updated  **required** 

**Important** : Any other required fields (defined on CIGNON Process Type/Master Entity Type configuration) need to be sent.

response:
```json
{
   "Entity":{
      "Id":"8fb17ba4-cb7e-468d-8e7d-837ef94f76b9",
      "VersionId":"b8a41230-0625-4bbe-8e77-2e3f1871ec6d",
      "Version":2,
      "xDocuments1":[
         {
            "Id":"5eff95ba-240f-4a0e-ae76-d1f106e34e87"
         },
         {
            "Id":"87d54ee8-2a88-4393-a6b3-1eb4076c16f0"
         },
         {
            "Id":"a6ce7d35-5743-434c-9fd2-291d71f7e06e"
         }
      ]
   },
   "ErrorCode":0
}

```
* **id** process or entity's id 
* **versionId** identifier for the entity/process version

