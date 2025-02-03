# Upload File

Using the upload routes requires an adjusted workflow, you must:
* Requires authentication 
* Initialize the upload using the **Initialize** route
* Upload each chunk of bytes using the **Update** route
* Complete the upload using the **Finalize** route

## Routes

| Method      | Route                      | Used for                  |
| ----------- | ---------------------------| ------------------------- |
| `POST`      | `/api/v1/upload/initialize`| initialize a new upload   |
| `POST`      | `/api/v1/upload/update`    | update an upload          |
| `POST`      | `/api/v1/upload/finalize`  | finalize an upload        |

## Upload (Initialize)

The **initialize** request is used to initialize a file upload session. It returns an **UploadId** which should be used to execute all subsequent requests. The next step after a successful response is the **update** request. 

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/initialize

Example:

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
Request:
```json
{
   "Name":"Hello World",
   "ContentExtension":"txt",
   "ContentLength": 18
}
```

### Required Parameters:

| Name               | Description                      | Example          |
| ------------------ | ---------------------------------| -----------------|
| `Name`             | File name without extension      | User Guide       |
| `ContentExtension` | File extension without the "."   | pdf              |
| `ContentLength`    | The size of the upload in bytes  | 2097152          |


Response:
```json
{
   "UploadId":"1153EF2374-C6B659870B-10F30A6AE8-930133ED91",
   "ErrorCode":0
}
```

* * *

### Upload (Update)

The **update** request is used to upload a chuck (consecutive byte range) of the upload file. For example for a 2.5 MB file could be split into 3 chunks of 1 MB size, and uploaded using 3 **update** requests. After the entire file is uploaded the next step is to request the **finalize** request. 

Notes:
* The max size of a chunk is 1 MB
* The requests should be **multipart/form-data** POST format.

Example:

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/update

Request:
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

| Name               | Description                      |
| ------------------ | ---------------------------------|
| `Action`           | Must be set to **append**        |
| `UploadId`         | The **UploadId** returned from the **initialize** request   |
| `SegmentIndex`     | An ordered index of the file chunk. The first segment has index 0, second segment has index 1, and so on.  |
| `Data`             | The raw binary file content being uploaded. It must be less or equal to 1 MB.        |

Response:
```json
{
   "ErrorCode":0
}
```

* * *

### Upload (Finalize)

The **finalize** request should be called after the entire media is uploaded using **update** requests. It returns an **DocumentId** which can be used with Cignon's **document field**.  

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/upload/finalize

Example:

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
Request:
```json
{
   "UploadId":"1153EF2374-C6B659870B-10F30A6AE8-930133ED91"
}
```

Response:
```json
{
  "DocumentId": "NWY1NTo2NTk7NjRoNmc0OzU0OjZmZTY3OTg1ODlmNzIxx3xx",
  "ErrorCode": 0
}
```

* * *

