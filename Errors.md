
Error | Description |
| ----------- | ---------------------------|
0 | Success |
1 | UncaughtServerError |
101 | ParameterNotFound |
102 | ParameterValueIsNotValid |
103 | ParameterValueIsNotAnArray |
104 | ParameterValueIsNotAnObject |
105 | ParameterValueIsNotAllowed |
1001 | GetTokenApplicationNotFound |
1002 | GetTokenApplicationNotActive |
1003 | GetTokenTenantNotFound |
2001 | LoginTokenParserError |
2002 | LoginTokenTypeIsIncorrect |
2003 | LoginTokenDecryptError |
2004 | LoginTokenNotFound |
2005 | LoginTokenAlreadyActivated |
2006 | LoginTokenExpired |
2007 | LoginTokenUnauthorized |
2008 | LoginTokenError |
2009 | LoginTenantNotFound |
2010 | LoginUserNotFound |
2011 | LoginUserNotActive |
3001 | AuthorizationHeaderMissing |
3002 | AuthorizationHeaderParserError |
3003 | AuthorizationExpired |
3004 | AuthorizationSessionInvalid |
4001 | EntityFieldNotFound |
4002 | EntityFieldValueIsNotValid |
4003 | EntityFieldValueIsNotAnArray |
4004 | EntityFieldValueIsNotAnObject |
4005 | EntityFieldValueIsNotAllowed |
5001 | UploadNoUpdate |
5002 | UploadNotFound |
5003 | UploadIsDisabledOrExpired |
5004 | UploadIsFinal |
5005 | UploadUnexpectedSegmentIndex |
5006 | UploadContentDataOverflow |
5007 | UploadIsNotComplete |
6001 | ServerGetTenantError |
6002 | ServerLoginError |
6003 | ServerGetEntityMetadataError |
6004 | ServerGetEntityError |
6005 | ServerCreateEntityError |
6006 | ServerUpdateEntityError |
6007 | ServerStreamUploadDocumentError |


Some examples:
```json
{
  "ErrorCode": 6003,
  "ErrorMessage": "EntityService.GetEntityMetadata ErrorCode=[EntityTypeNotFound]"
}
```

```json
{
  "ErrorCode": 4001,
  "ErrorMessage": "xBool11"
}
```

```json
{
  "ErrorCode": 4001,
  "ErrorMessage": "xDocuments1 (1) >> xInt12"
}
```

```json
{
  "ErrorCode": 4002,
  "ErrorMessage": "xDocuments1 (1) >> xInt1"
}
```

```json
{
  "ValidationRules": [
    {
      "ValidationId": "424f9889-baae-4aaf-8b7a-d440ee7efc8b",
      "IsConstrain": true,
      "Message": "Title is empty",
      "FieldAliases": [
        {
          "Alias": "Title",
          "Title": "Title"
        }
      ]
    }
  ],
  "ErrorCode": 6005,
  "ErrorMessage": "EntityService.CreateEntity ErrorCode=[CheckValidationRules]"
}
```

```json
{
  "ErrorDetails": [
    {
      "FieldObjectTypeName": "DetailEntityFieldValue",
      "FieldAlias": "xDocuments1",
      "FieldValueTypeName": "List`1",
      "ErrorCode": 2,
      "InnerErrors": [
        {
          "Id": "236eb92b-1fb0-44ff-8cd3-685bbe098cb9",
          "ErrorCode": 22
        }
      ]
    }
  ],
  "ErrorCode": 6006,
  "ErrorMessage": "EntityService.CreateEntity ErrorCode=[ErrorDetails] Ex=[]"
}
```