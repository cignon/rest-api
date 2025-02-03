## Update Entity or Process

Update a Process or Entity based on the specified Process/Entity **Id**.

Example:

`PUT` https://foobar.cignon.com/CignonRestServer/api/v1/entity

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
Request:
```json
{
    "EntityTypeId": "ei77ZTtnODVmOGVjOGM7NTY3Y2Y7ZjYzZDQ1OTcyNzIyM2gxx3xx",
    "Id": "ZzczN2Y7YzI1aDI3MmU6OzU4ODYzNWdoaDplO2QyZWQxx3xx",
    "ModifiedTimestamp": "AAAAAAAQ0eQ=",

    "xDateTime1": "2025-01-30T06:07:08Z",
    "xInt1": 2,
    "xDec1": "719971921971921.43",
    "xDocuments1": [
            {
                "Id" : "MzY6ZmVkZTM2MzY6ZWcyZDM2YzY0YzY5NWRnZTI6O2gxx3xx",
                "xText1": "updating detail 1 using id"
            },
            {
                "xInt1": 789,
                "xText1": "add another detail"
            }
        ]
}
```
### Required Parameters:

| Name                 | Description                      |
| -------------------- | ---------------------------------|
| `EntityTypeId`       | Process Type or Master Entity Type identifier |
| `Id` | Entity identifier   |
| `ModifiedTimestamp` | Entity actual ModifiedTimestamp |

**Important** : Any other required fields (defined on CIGNON Process Type/Master Entity Type configuration) need to be sent. 

Response:
```json
{
  "Entity": {
    "Id": "ZzczN2Y7YzI1aDI3MmU6OzU4ODYzNWdoaDplO2QyZWQxx3xx",
    "Version": 2,
    "ModifiedTimestamp": "AAAAAAAQ0e8=",
    "xDocuments1": [
      {
        "Id": "ZTtlMzdlZjJoY2Y0ZDk0OzJoMjY2ZjdjOTtoYztoNjQxx3xx"
      },
      {
        "Id": "OjQzNTloaDo1Yzc0OGU1OmczZzZlNGZnOmQ3NTc6NjQxx3xx"
      },
      {
        "Id": "OjY7Zmc1Zzk2Mzc0ZjNnYzg7ZjY5NjRlNWM1Ojk3NDIxx3xx"
      }
    ]
  },
  "ErrorCode": 0
}
```
Returns:
* **Id** new process or entity's id 
* **Version** process/entity version (Starts at 1)

Note:

* Ids are returned for each detail entity. 
