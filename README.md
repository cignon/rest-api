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

[Authentication](Authentication.md)

[Upload File](Upload%20File.md)

[Create Entity](Create%20Entity.md)

[Upload Entity](Create%20Entity.md)

[Logout](Logout.md)

[Errors](Errors.md)


