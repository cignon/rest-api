# Logout

Logout an authenticated session.

## Routes

| Method      | Route                      | Used for                  |
| ----------- | ---------------------------| ------------------------- |
| `GET`       | `/api/v1/auth/logout`      | logout                    |

Example:

`GET` https://foobar.cignon.com/CignonRestServer/api/v1/auth/logout

http header:
```
Authorization: Bearer AgEcAGFCHUt0fdlIiRSw1i8RTUKQI/xMEoOmNdJbjXs=
```
Response:
```json
{
   "ErrorCode":"0"
}
```
* * *