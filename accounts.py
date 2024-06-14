import simple_salesforce
import os
import requests

def set_default_settings():
    global preferences
    preferences = {
        'account_additional_columns': '',
        'show_contacts': True,
        'contact_additional_columns': ''
    }

def change_settings():
    global preferences
    print("Change settings:")
    preferences['account_additional_columns'] = input("\nEnter additional column names comma-separated for accounts besides Id, Name, Description, Website :\n e.g., Industry, Phone, TickerSymbol ")
    preferences['show_contacts'] = input("\nShow contacts for each account? (yes/no): ").lower() != 'no'
    if preferences['show_contacts']:
        preferences['contact_additional_columns'] = input("\nEnter additional column names comma-separated for contacts besides Id, FirstName, LastName, Email, Title, Phone, Description:\ne.g., MobilePhone, CreatedDate, LastModifiedDate, LeadSource ")
    else:
        preferences['contact_additional_columns'] = ""

def main():
    username = os.environ['SALESFORCE_USERNAME']
    password = os.environ['SALESFORCE_PASSWORD']
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']

    # Set default settings when the program starts
    set_default_settings()

    # Create a Salesforce connection
    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)

    print("\nConnected to Salesforce - first time\n")

    while True:
        try:

            action = input("\nEnter 'sa' to search accounts, 'sc' to search contacts, 'ca' to create an account, 'cc' to create a contact, 'da' to delete an account, 'd' to describe object schemas, 's' for global settings, or 'q' to exit: ")

            if action.lower() == 'q':
                break

            elif action.lower() == 'create account':
                name = input("Enter account name: ")
                website = input("Enter account website: ")
                description = input("Enter account description: ")
                account = sf.Account.create({'Name': name, 'Website': website, 'Description': description})
                account_id = account.get('id')  # Get the account ID from the response
                print(f"\nCreated account {account_id}\n")

            elif action.lower() == 'cc':


                account_name = input("\nAn account must already exist  to create a contact. Enter account name to lookup id: ")
                account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%'")

                if account_results['totalSize'] > 1:
                    print("Multiple accounts found:")
                    for i, account in enumerate(account_results['records']):
                        print(f"{i+1}. {account['Name']}")
                    selection = int(input("Select the correct account (1-{account_results['totalSize']}): "))
                    account_id = account_results['records'][selection-1]['Id']
                else:
                    print(f"Found account: {account_results['records'][0]['Name']} with Id: {account_results['records'][0]['Id']}\n")
                    account_id = account_results['records'][0]['Id']

                first_name = input("Enter contact first name: ")
                last_name = input("Enter contact last name: ")
                email = input("Enter contact email: ")
                description = input("Enter contact description: ")
                phone = input("Enter contact phone: ")
                title = input("Enter contact title: ")
                department = input("Enter contact department: ")
                address = input("Enter contact mailing address: ")
                city = input("Enter contact city: ")
                state = input("Enter contact state: ")
                postalcode = input("Enter contact zip code: ")
                country = input("Enter contact country: ")
                contact = sf.Contact.create({
                    'AccountId': account_id,
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': email,
                    'Description': description,
                    'Phone': phone,
                    'Title': title,
                    'Department': department,
                    'MailingStreet': address,
                    'MailingCity': city,
                    'MailingState': state,
                    'MailingPostalcode': postalcode,
                    'MailingCountry': country   
                })
                contact_id = contact.get('id')  # Get the account ID from the response
                print(f"\nCreated contact {contact_id}\n")

            elif action.lower() == 'sa':

                # Get the account name to filter by from the user
                account_name = input("\nEnter the account name to filter by or 'quit' to exit): ")

                if account_name.lower() == 'quit':
                    break

                else:

                    # Query accounts
                    query = f"SELECT Id, Name, Description, Website"
                    
                    if preferences['account_additional_columns']:
                        query += ", " + preferences['account_additional_columns']
                    else:
                        query += " "

                    query += f" FROM ACCOUNT WHERE Name LIKE '%{account_name}%'"

                    print("\nAccounts query: ", query)
                    print("\nAccounts:\n")

                    try:
                        accounts = sf.query(query)
                    except requests.exceptions.ConnectionError:
                        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                        print("\nReconnected to Salesforce\n")
                        accounts = sf.query(query)

                    # Print column headers
                    if preferences['account_additional_columns']:
                        columns = ['Id', 'Name', 'Description', 'Website'] + [column.strip() for column in preferences['account_additional_columns'].split(', ')]
                        print(*columns, sep='\t')  # Print column names
                    else:
                        print('Id', 'Name', 'Description', 'Website', sep='\t')  # Print default column names

                    # Print results
                    for account in accounts['records']:
                        print(account['Id'], account['Name'], account['Description'], account.get('Website', ''), *[

                            account[column] for column in preferences['account_additional_columns'].split(', ') if column.strip() != ''

                        ])

                    # Get contacts for the account
                    if preferences['show_contacts']:
                        contact_query = f"SELECT Id, FirstName, LastName, Email, Title, Phone, Description"
                        if preferences['contact_additional_columns']:
                            contact_query += ", " + preferences['contact_additional_columns']
                        contact_query += f" FROM Contact WHERE AccountId = '{account['Id']}'"

                        contacts = sf.query(contact_query)
                        print("\nContacts query: ", contact_query)
                        print("\nContacts:\n")

                        if preferences['contact_additional_columns']:
                            contact_columns = ['Id', 'FirstName', 'LastName', 'Email', 'Title', 'Phone', 'Description'] + [column.strip() for column in preferences['contact_additional_columns'].split(', ')]
                            print(*contact_columns, sep='\t')
                        else:
                            print("Id", "FirstName", "LastName", "Email","Title","Phone","Description", sep='\t')

                        for contact in contacts['records']:
                            print(contact.__dict__)
                            print(contact['Id'], contact['FirstName'], contact['LastName'], contact['Email'], contact['Title'], contact['Phone'], contact['Description'], *[
                                contact.get(column) for column in preferences['contact_additional_columns'].split(', ') if column.strip() != ''
                            ])


                    

            elif action.lower() == 'sc':
                search_term = input("\nEnter a search term (first name, last name, email, or title): ")
                contacts = sf.query(f"SELECT Id, FirstName, LastName, Title, Department, Email, Phone, MailingAddress, Description FROM Contact WHERE FirstName LIKE '%{search_term}%' OR LastName LIKE '%{search_term}%' OR Email LIKE '%{search_term}%' OR Title LIKE '%{search_term}%'")

                if contacts['totalSize'] > 0:
                    print("\nContacts:")
                    for contact in contacts['records']:
                        print(f"Id: {contact['Id']}")
                        print(f"First Name: {contact['FirstName']}")
                        print(f"Last Name: {contact['LastName']}")
                        print(f"Title: {contact['Title']}")
                        print(f"Department: {contact['Department']}")
                        print(f"Email: {contact['Email']}")
                        print(f"Phone: {contact['Phone']}")
                        print(f"Mailing Address: {contact['MailingAddress']}")
                        print(f"Description: {contact['Description']}\n")
                else:
                    print("No contacts found")

            elif action.lower() == 'da':
                account_name = input("\nEnter a keyword to lookup accounts: ")
                accounts = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%'")

                if accounts['totalSize'] > 0:
                    print("\nAccounts:")
                    for i, account in enumerate(accounts['records']):
                        print(f"{i+1}. {account['Id']}: {account['Name']}")

                    print("\nOptions:")
                    print("1. Delete a specific account by number in the list")
                    print("2. Delete all accounts in the list")
                    print("3. Cancel")

                    option = int(input("Enter your option: "))

                    if option == 1:
                        account_index = int(input("Enter the number of the account to delete: "))
                        if account_index > 0 and account_index <= accounts['totalSize']:
                            account_id = accounts['records'][account_index-1]['Id']
                            sf.Account.delete(account_id)
                            print(f"Deleted account {account_id}")
                        else:
                            print("Invalid account index")
                    elif option == 2:
                        delete_all = input("Are you sure you want to delete all accounts? (yes/no): ")
                        if delete_all.lower() == 'yes':
                            account_ids = [account['Id'] for account in accounts['records']]
                            for account_id in account_ids:
                                sf.Account.delete(account_id)
                                print(f"Deleted account {account_id}")
                        else:
                            print("Deletion cancelled")
                    elif option == 3:
                        print("No accounts deleted")
                    else:
                        print("Invalid option")
                else:
                    print("No accounts found")

            elif action.lower() == 'd':
                print("\nDescribe the account object:\n")
                account_fields = sf.Account.describe()
                for field in account_fields['fields']:
                    print(field['name'])
                print("\nDescribe the contact object:\n")
                contact_fields = sf.Contact.describe()
                for field in contact_fields['fields']:
                    print(field['name'])

            elif action.lower() == 's':
                change_settings()

        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()