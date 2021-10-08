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

Returns:
* **Id** new process or entity's id 

Note:

* Ids are returned for each detail entity created. 

* * *

