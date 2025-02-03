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
    "Id": "ZzczN2Y7YzI1aDI3MmU6OzU4ODYzNWdoaDplO2QyZWQxx3xx",
    "Fields": [ "Stage", "xBool1", "xDateTime1", "xDec1", "xIntArray1", "xDocuments1" ],
    "Details": [
        {
            "Alias": "xDocuments1",
            "Fields": [ "Id", "xDocument1" ],
            "Ids": [ "ZTtlMzdlZjJoY2Y0ZDk0OzJoMjY2ZjdjOTtoYztoNjQxx3xx" ]
        },
        {
            "Alias": "xProcesses",
            "Fields": [ "Id", "xBool1", "xInt1" ],
            "Ids": [ "MzY6ZmVkZTM2MzY6ZWcyZDM2YzY0YzY5NWRnZTI6O2gxx3xx" ]
        }
    ]
}
```
### Required Parameters:

| Name                 | Description                      |
| -------------------- | ---------------------------------|
| `Id` | Entity identifier   |

### Optional Parameters:

| Name                 | Description                      |
| -------------------- | ---------------------------------|
| `Fields` | list of master aliases to return data |
| `Details` | return definitions for each detail  |

### Detail Parameters:

| Name                 | Description                      | Required |
| -------------------- | ---------------------------------|----------|
| `Alias` | Master detail field alias | Yes |
| `Fields` | list of detail aliases to return data | No |
| `Ids` | List of Detail Identifiers  | Yes |


Response:
```json
{
  "Entity": {
    "Id": "ZzczN2Y7YzI1aDI3MmU6OzU4ODYzNWdoaDplO2QyZWQxx3xx",
    "Version": 2,
    "ModifiedOn": "2025-01-31T16:11:45.0670000",
    "ModifiedBy": "M2c1ZjQ3NjlmZTQ7ZzY6ZDQ4MzZoZDNmOzQ3Ozs6Ozsxx3xx",
    "ModifiedTimestamp": "AAAAAAAQ0fE=",
    "Stage": "NzVkNDc4ODdjOmdmZ2g4ZGg2ZzZnZmU4N2ZnNTs5ZDUxx3xx",
    "xBool1": true,
    "xDateTime1": "2025-01-30T06:07:08.0000000",
    "xDec1": "719971921971921.43000",
    "xIntArray1": [
      1,
      3,
      5
    ]
  },
  "ErrorCode": 0
}
```
Returns:
* **Id** process or entity's id 
* **ModifiedTimestamp** process/entity Modifiedtimestamp
* **Version** process or entity's version number 

Note:
* Stage, xBool1, xDateTime1, xDec1, xIntArray1 are optional data returned 
