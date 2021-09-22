# Introduction

Cignon REST API interface provides a simple way for an external application to talk to Cignon by making HTTP requests.

## Introduction to Cignon REST APIS

Cignon API provide access to resources via URL paths. To use a REST API, your application will make a HTTP request and parse the response.

All requests and responses for Cignon endpoint are in JSON format, unless other format are expected for specific endpoint which you can find in the documentation.

Cignon REST API is based on open standards like [JSON-Schema](http://json-schema.org/) (for data validation), you can use any web developer language to work with the API. 

## Pre-requisites

Before you begin you will need to know:

* The main url path to the Cignon REST Server 
* Cignon Rest Server RSA public key
* Tenant Id 
* Application Id 
* Client/Application RSA private key

## Initial setup

Before you can do anything, you'll need to authenticate your application. 

You will need to submit the your application public key to the Cignon infrastructure administrator

The authentication relies exclusivelyy on your (application) RSA private key (only known to you).

### 1. Generate private key for your application

```shell
openssl genrsa -out my_application_private.key 4096
openssl rsa -in my_application_private.key -pubout -out my_application_public.pub
```

### 2. Cignon backend configuration

Submit your public key **my_application_public.pub** to the Cignon IT Admin, and in return you will get:
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
| `POST`      | `/api/v1/entity`           | create entity or process  |
| `PUT`       | `/api/v1/entity`           | update entity or process  |

* * *

## Authentication

The authentication is performed in two steps: 
* Application calls **getToken** providing the applicationId, tenantId, deviceId, the server creates a encrypted token using the application public key.
* Application decrypts the token using the private key and encrypts the token using the server's public key then calls **login** providing the encrypted token, applicationId, tenantId and the userId in return the server returns the authentication token to be used with further interactions requiring an authentication token.

* * *

### getToken

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
* **token** base 64 token encrypted using the application public key. You will need your private key to decrypt the token.

* * *

### login

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

### logout

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

### Create entity or process

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/entity

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
request:
```json
{
   "entity":{
      "entityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
      "organizationalUnit":"174BE6FF-4125-4EEC-8A41-6632A218752F",
      "category":"29967816-40BF-4329-A930-2696C0A1938B",
      "title":"my first process",
      "xBool1":true,
      "xDate1":"2021-05-13T00:00:00Z",
      "xDateTime1":"2021-05-21T14:12:09.658Z",
      "xDec1":"123.45",
      "xIntArray1":"1,3,5",
      "xTextArray1":"NJ,CA,TX"
   }
}
```
* **entityTypeId** Cignon process type or master entity type identifier **required** 
* **organizationalUnit** Cignon Organizational Unit identifier  **required** 
* **category** Process Type's Category identifier **required for process**
* **title** Entity or Process's title **required**
 
response:
```json
{
   "entity":{
      "id":"d9d44e75-1638-4bf4-b62f-49660c00d2f1"
   },
   "errorCode":"0"
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
   "entity":{
      "entityTypeId":"F1005057-32B1-4D9D-A543-9A6AC6D36E9C",
      "id":"d9d44e75-1638-4bf4-b62f-49660c00d2f1",
      "xDateTime1":"2021-09-22T02:54:30.8977427Z",
      "xInt1":"1"
   }
}
```
* **entityTypeId** Cignon process type or master entity type identifier **required** 
* **id** entity or process's id to be updated  **required** 

response:
```json
{
   "entity":{
      "id":"d9d44e75-1638-4bf4-b62f-49660c00d2f1",
      "versionId":"a930d94a-f9b0-47e1-ab80-54c75afa6e65",
      "version":2
   },
   "errorCode":"0"
}
```
* **id** process or entity's id 
* **versionId** identifier for the entity/process version

