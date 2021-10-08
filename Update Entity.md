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
### Required Parameters:

| Name                 | Description                      |
| -------------------- | ---------------------------------|
| `EntityTypeId`       | Process Type or Master Entity Type identifier |
| `Id` | Entity identifier   |

**Important** : Any other required fields (defined on CIGNON Process Type/Master Entity Type configuration) need to be sent. 

Response:
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
Returns:
* **Id** new process or entity's id 
* **VersionId** process/entity version identifier
* **Version** process/entity version (Starts at 1)

Note:

* Ids are returned for each detail entity created. 
