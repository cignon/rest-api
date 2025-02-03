# Create Entity or Process

Creates a Process/Entity of type **EntityTypeId** as a child of the **OrganizationalUnitId**.

Example:

`POST` https://foobar.cignon.com/CignonRestServer/api/v1/entity

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
Request:
```json
{
   "Entity":{
      "EntityTypeId": "ei77ZTtnODVmOGVjOGM7NTY3Y2Y7ZjYzZDQ1OTcyNzIyM2gxx3xx",
      "OrganizationalUnit" : "ei77aDQ3OTozNGM0NTg4MzZjOmVnZzY3NDM2aGg4Z2Q2OTMxx3xx",
      "Category": "ei77ZDo1OzNjMmU4Ozg0MjU7Yzs0NTZoZDI2ODM6OTg7OzQxx3xx",
      "Title": "my first process",
      "xBool1": true,
      "xDate1": "2021-05-13T00:00:00Z",
      "xDateTime1": "2021-07-04T01:49:23.8039368Z",
      "xDec1": "123.45",
      "xIntArray1" :[
         1,
         3,
         5
      ],
      "xTextArray1" :[
         "NJ",
         "CA",
         "TX"
      ],
      "xDocuments1" :[
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
### Required Parameters:

| Name                 | Description                      |
| -------------------- | ---------------------------------|
| `EntityTypeId`       | Process Type or Master Entity Type identifier |
| `OrganizationalUnit` | Organizational Unit identifier   |
| `Category`           | Only required for Processes  | 
| `Title`              | Title (Max. 100 characters)  |


**Important** : Any other required fields (defined on CIGNON Process Type/Master Entity Type configuration) need to be sent. 

Response:
```json
{
  "Entity": {
    "Id": "ZzczN2Y7YzI1aDI3MmU6OzU4ODYzNWdoaDplO2QyZWQxx3xx",
    "ModifiedTimestamp": "AAAAAAAQ0eQ=",
    "xDocuments1": [
      {
        "Id": "ZTtlMzdlZjJoY2Y0ZDk0OzJoMjY2ZjdjOTtoYztoNjQxx3xx"
      },
      {
        "Id": "OjQzNTloaDo1Yzc0OGU1OmczZzZlNGZnOmQ3NTc6NjQxx3xx"
      }
    ]
  },
  "ErrorCode": 0
}
```

Returns:
* **Id** new process or entity's id 
* **ModifiedTimestamp** new process ModifiedTimestamp

Note:

* Ids are returned for each detail entity created. 

* * *

