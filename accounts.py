import simple_salesforce
import os
import requests

def main():
    username = os.environ['SALESFORCE_USERNAME']
    password = os.environ['SALESFORCE_PASSWORD']
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']

    # Create a Salesforce connection
    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)

    print("\nConnected to Salesforce - first time\n")

    while True:
        try:

            # Get the account name to filter by from the user
            account_name = input("\nEnter the account name to filter by, or 'describe' to show object schemas, or 'quit' to exit): ")

            if account_name.lower() == 'quit':
                break

            if account_name.lower() == 'describe':
                print("\nDescribe the account object:\n")
                account_fields = sf.Account.describe()
                for field in account_fields['fields']:
                    print(field['name'])
                print("\nDescribe the contact object:\n")
                contact_fields = sf.Contact.describe()
                for field in contact_fields['fields']:
                    print(field['name'])

            else:

                # Query accounts
                query = f"SELECT Id, Name, Description"
                
                additional_columns = input("\nEnter additional column names comma-separated besides Id, Name, Description which are in the default query e.g., CreatedDate, Phone, Website, Type - see columns with input parameter `describe` on next query: ")
                if additional_columns:
                    query += ", " + additional_columns
                else:
                    query += " "

                # Ask if user wants to show contacts
                show_contacts = input("\nShow contacts for each account? (yes/no): ").lower() == 'yes'

                query += f" FROM ACCOUNT WHERE Name LIKE '%{account_name}%'"

                print("\nAccounts query: ", query)

                try:
                    accounts = sf.query(query)
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print("\nReconnected to Salesforce\n")
                    accounts = sf.query(query)

                # Print column headers
                if additional_columns:
                    columns = ['Id', 'Name', 'Description'] + [column.strip() for column in additional_columns.split(', ')]
                    print(*columns, sep='\t')  # Print column names
                else:
                    print('Id', 'Name', 'Description', sep='\t')  # Print default column names

                # Print results
                for account in accounts['records']:
                    print(account['Id'], account['Name'], account['Description'], *[

                        account[column] for column in additional_columns.split(', ') if column.strip() != ''

                    ])

                    # Get contacts for the account
                    if show_contacts:
                        contact_query = f"SELECT Id, FirstName, LastName, Email, Title, Phone, Description FROM Contact WHERE AccountId = '{account['Id']}'"
                        contacts = sf.query(contact_query)
                        print("\nContacts query: ", contact_query)
                        print("\nContacts:")
                        print("Id", "FirstName", "LastName", "Email","Title","Phone","Description", sep='\t')
                        for contact in contacts['records']:
                            print(contact['Id'], contact['FirstName'], contact['LastName'], contact['Email'], contact['Title'], contact['Phone'], contact['Description'], sep='\t')



        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()