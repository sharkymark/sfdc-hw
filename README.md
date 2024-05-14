# Learning Salesforce's API

Salesforce is a Customer Relationship Management "CRM" web application. This example uses the API to query the CRM.

## Programming language

This example uses Python and is a command line application

## API

Simple Salesforce is a basic Salesforce.com REST API client built for Python 3.8, 3.9, 3.10, 3.11, and 3.12. The goal is to provide a very low-level interface to the REST Resource and APEX API, returning a dictionary of the API JSON response. 

## Authentication

Credentials include username, password and token. They are read as environment variables which you place in `.zshrc` or `.bashrc`

```sh
# set SalesForce environment variables
export SALESFORCE_USERNAME=""
export SALESFORCE_PASSWORD=""
export SALESFORCE_SECURITY_TOKEN=""
```

Retrieve the security token from the Salesforce UI, View Profile -> Settings -> Reset My Security Token

## Run the app

`cd` into the repo directory and run the app

```sh
python3 accounts.py
```

## Additional columns

Using the word `describe` will show the available columns for the Account object.

After providing a query filter parameter, the user is prompted for additional column names which will be comma-delimited. e.g., `CreatedDate, Phone, Website, Type`

If the user wants to only use the default Id, Name and Description columns as output, just press enter.

## The app 

The app runs as a while loop prompting the user for a value to filter Salesforce Account records by the Name column.

## Resources

[Python Mac versions](https://www.python.org/downloads/macos/)

[simple_salesforce Python package](https://github.com/simple-salesforce/simple-salesforce)

[Salesforce APIs](https://developer.salesforce.com/docs/apis)

[Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm)