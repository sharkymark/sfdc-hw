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

    # Get additional columns for accounts
    account_additional_columns = input("\nEnter additional column names comma-separated for accounts besides Id, Name, Description:\n e.g., Industry, Phone, Website, TickerSymbol ")

    # Ask if user wants to show contacts
    show_contacts = input("\nShow contacts for each account? (yes/no): ").lower() == 'no'

    if show_contacts:
        # Only ask for additional contact fields if show_contacts is True
        contact_additional_columns = input("\nEnter additional column names comma-separated for contacts besides Id, FirstName, LastName, Email, Title, Phone, Description:\ne.g., MobilePhone, CreatedDate, LastModifiedDate, LeadSource ")
    else:
        # If show_contacts is False, set contact_additional_columns to an empty string
        contact_additional_columns = ""

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
                
                if account_additional_columns:
                    query += ", " + account_additional_columns
                else:
                    query += " "

                query += f" FROM ACCOUNT WHERE Name LIKE '%{account_name}%'"

                print("\nAccounts query: ", query)

                try:
                    accounts = sf.query(query)
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print("\nReconnected to Salesforce\n")
                    accounts = sf.query(query)

                # Print column headers
                if account_additional_columns:
                    columns = ['Id', 'Name', 'Description'] + [column.strip() for column in account_additional_columns.split(', ')]
                    print(*columns, sep='\t')  # Print column names
                else:
                    print('Id', 'Name', 'Description', sep='\t')  # Print default column names

                # Print results
                for account in accounts['records']:
                    print(account['Id'], account['Name'], account['Description'], *[

                        account[column] for column in account_additional_columns.split(', ') if column.strip() != ''

                    ])

                # bulk delete accounts, with logic for 1 or multiple accounts

                if accounts['totalSize'] > 0:
                    if input("\nDelete accounts? (yes/no): ").lower() != 'no':

                        if accounts['totalSize'] > 10:
                            confirm = input(f"Warning: Deleting {accounts['totalSize']} accounts. Are you sure? (yes/no): ").lower()
                            if confirm != 'yes':
                                print("Deletion cancelled")
                                return

                        account_ids = [account['Id'] for account in accounts['records']]
                        for account_id in account_ids:
                            sf.Account.delete(account_id)
                            print(f"Deleted account {account_id}")
                    else:
                        print("No accounts deleted")
                else:
                    print("No accounts returned")

                # Get contacts for the account
                if show_contacts:
                    contact_query = f"SELECT Id, FirstName, LastName, Email, Title, Phone, Description"
                    if contact_additional_columns:
                        contact_query += ", " + contact_additional_columns
                    contact_query += f" FROM Contact WHERE AccountId = '{account['Id']}'"

                    contacts = sf.query(contact_query)
                    print("\nContacts query: ", contact_query)
                    print("\nContacts:")

                    if contact_additional_columns:
                        contact_columns = ['Id', 'FirstName', 'LastName', 'Email', 'Title', 'Phone', 'Description'] + [column.strip() for column in contact_additional_columns.split(', ')]
                        print(*contact_columns, sep='\t')
                    else:
                        print("Id", "FirstName", "LastName", "Email","Title","Phone","Description", sep='\t')

                    for contact in contacts['records']:
                        print(contact.__dict__)
                        print(contact['Id'], contact['FirstName'], contact['LastName'], contact['Email'], contact['Title'], contact['Phone'], contact['Description'], *[
                            contact.get(column) for column in contact_additional_columns.split(', ') if column.strip() != ''
                        ])



        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()