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

def update_account(sf, account_id):
    account = sf.Account.get(account_id)
    print(f"\nUpdating account {account['Name']}:")

    new_name = input(f"Enter new name ({account['Name']}): ")
    new_website = input(f"Enter new website ({account['Website']}): ")
    new_description = input(f"Enter new description ({account['Description']}): ")

    if new_name.strip():
        account['Name'] = new_name
    if new_website.strip():
        account['Website'] = new_website
    if new_description.strip():
        account['Description'] = new_description

    sf.Account.update(account_id, {'Name': account['Name'], 'Website': account['Website'], 'Description': account['Description']})
    print(f"\nUpdated account {account_id}")

def update_contact(sf, contact_id):
    contact = sf.Contact.get(contact_id)
    print(f"\nUpdating contact {contact['FirstName']} {contact['LastName']}:")
    new_first_name = input(f"Enter new first name ({contact['FirstName']}): ")
    new_last_name = input(f"Enter new last name ({contact['LastName']}): ")
    new_email = input(f"Enter new email ({contact['Email']}): ")
    new_title = input(f"Enter new title ({contact['Title']}): ")

    if new_first_name.strip():
        contact['FirstName'] = new_first_name
    if new_last_name.strip():
        contact['LastName'] = new_last_name
    if new_email.strip():
        contact['Email'] = new_email
    if new_title.strip():
        contact['Title'] = new_title

    # Remove the Id field from the contact dictionary
    #contact.pop('Id')

    sf.Contact.update(contact_id, {'FirstName': contact['FirstName'], 'LastName': contact['LastName'], 'Email': contact['Email'], 'Title': contact['Title']})
    print(f"\nUpdated contact {contact_id}")

def main():

    firstconn = "\nConnected to Salesforce - first time\n"
    reconn = "\Reconnected to Salesforce\n"

    username = os.environ['SALESFORCE_USERNAME']
    password = os.environ['SALESFORCE_PASSWORD']
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']

    # Set default settings when the program starts
    set_default_settings()

    # Create a Salesforce connection
    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
    print(firstconn)

    while True:
        try:

            print("\x1b[5 q")

            print("\n==============================================================================")
            print("**Warning:** Admin users or those with elevated rights, proceed with caution!")
            print("==============================================================================\n")

            action = input("""Enter:
            'sa' to search or update accounts (and contacts),
            'sc' to search contacts,
            'ca' to create an account,
            'cc' to create a contact,
            'da' to delete an account,
            'dc' to delete a contact,
            'd' to describe object schemas,
            's' for global settings,
            'q' to exit:
            
            """)

            if action.lower() == 'q':
                break

            elif action.lower() == 'ca':
                name = input("Enter account name: ")
                website = input("Enter account website: ")
                description = input("Enter account description: ")

                try:
                    account = sf.Account.create({'Name': name, 'Website': website, 'Description': description})
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    account = sf.Account.create({'Name': name, 'Website': website, 'Description': description})

                
                account_id = account.get('id')  # Get the account ID from the response
                print(f"\nCreated account {account_id}\n")

            elif action.lower() == 'cc':


                account_name = input("\nAn account must already exist to create a contact. Enter account name to lookup id: ")

                try:
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%'")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%'")


                if account_results['totalSize'] == 0:
                    print("\nNo accounts found")
                elif account_results['totalSize'] == 1:
                    account_id = account_results['records'][0]['Id']
                    print(f"\nFound account: {account_results['records'][0]['Name']} with Id: {account_id}\n")
                else:
                    print("\nMultiple accounts found:")
                    for i, account in enumerate(account_results['records']):
                        print(f"{i+1}. {account['Name']}")
                    selection = int(input("Select the correct account (1-{account_results['totalSize']}): "))
                    account_id = account_results['records'][selection-1]['Id']

                if 'account_id' in locals():
                    # rest of the code remains the same

                    first_name = input("Enter contact first name: ")
                    last_name = input("Enter contact last name: ")
                    email = input("Enter contact email: ")
                    phone = input("Enter contact phone: ")
                    title = input("Enter contact title: ")
                    description = input("Enter contact description: ")
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
                        print(reconn)
                        accounts = sf.query(query)

                    if accounts['totalSize'] > 0:

                        # Print column headers
                        if preferences['account_additional_columns']:
                            columns = ['Id', 'Name', 'Description', 'Website'] + [column.strip() for column in preferences['account_additional_columns'].split(', ')]
                            print(*columns, sep='\t')  # Print column names
                        else:
                            print('Id', 'Name', 'Description', 'Website', sep='\t')  # Print default column names

                        # Print results
                        for i, account in enumerate(accounts['records']):
                            print(f"{i+1}.", account['Id'], account['Name'], account['Description'], account.get('Website', ''), *[
                                account[column] for column in preferences['account_additional_columns'].split(', ') if column.strip() != ''
                            ])

                        exit_loop = False

                        while True:

                            print("\nOptions:")
                            print("1. Update a specific account by number in the list")
                            print("2. Cancel\n")
                        
                            try:
                                option = int(input("Enter your option: "))
                            except ValueError:
                                print("\nInvalid entry. Please enter a valid number.")
                                continue
                        
                            if option == 1:
                                account_index = int(input("\nEnter the number of the account to update: "))
                                if account_index > 0 and account_index <= accounts['totalSize']:
                                    account_id = accounts['records'][account_index-1]['Id']
                                    update_account(sf, account_id)
                            elif option == 2:
                                print("\nUpdate cancelled")
                            else:
                                print("\nInvalid account index")
                                break

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

                                if contacts['totalSize'] > 0:
                                    for i, contact in enumerate(contacts['records']):
                                        print(f"{i+1}.", contact['Id'], contact['FirstName'], contact['LastName'], contact['Email'], contact['Title'], contact['Phone'], contact['Description'], *[
                                            contact.get(column) for column in preferences['contact_additional_columns'].split(', ') if column.strip() != ''
                                        ])

                                    while True:

                                        print("\nOptions:")
                                        print("1. Update a specific contact by number in the list")
                                        print("2. Cancel\n")

                                        try:
                                            option = int(input("Enter your option: "))
                                        except ValueError:
                                            print("\nInvalid entry. Please enter a valid number.")
                                            continue

                                        if option == 1:
                                            try:
                                                contact_index = int(input("\nEnter the number of the contact to update: "))
                                                if contact_index > 0 and contact_index <= contacts['totalSize']:
                                                    contact_id = contacts['records'][contact_index-1]['Id']
                                                    update_contact(sf, contact_id)
                                                    exit_loop = True
                                                    break
                                                else:
                                                    print("\nInvalid contact index")
                                            except ValueError:
                                                print("\nInvalid entry. Please enter a valid number.")
                                            break
                                        elif option == 2:
                                            print("\nUpdate cancelled")
                                            exit_loop = True
                                            break

                                    if exit_loop:
                                        exit_loop = False  # Reset exit_loop to False
                                        break

                                else:
                                    print("No contacts found")
                            exit_loop = True
                            break

                    else:
                        print("No accounts found")
                    
            elif action.lower() == 'sc':
                search_term = input("\nEnter a search term (first name, last name, email, or title): ")

                try:
                    contacts = sf.query(f"SELECT Id, FirstName, LastName, Title, Department, Email, Phone, MailingAddress, Description FROM Contact WHERE FirstName LIKE '%{search_term}%' OR LastName LIKE '%{search_term}%' OR Email LIKE '%{search_term}%' OR Title LIKE '%{search_term}%'")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
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

                try:
                    accounts = sf.query(f"SELECT Id, CreatedDate, Name FROM Account WHERE Name LIKE '%{account_name}%'")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    accounts = sf.query(f"SELECT Id, CreatedDate, Name FROM Account WHERE Name LIKE '%{account_name}%'")
                

                if accounts['totalSize'] > 0:
                    print("\nAccounts: (Id, Name, CreatedDate)")
                    for i, account in enumerate(accounts['records']):
                        print(f"{i+1}. {account['Id']}: {account['Name']} {account['CreatedDate']} ")

                    print("\nOptions:")
                    print("1. Delete a specific account by number in the list")
                    print("2. Delete all accounts in the list")
                    print("3. Cancel\n")

                    option = int(input("Enter your option: "))

                    if option == 1:
                        account_index = int(input("\nEnter the number of the account to delete: "))
                        if account_index > 0 and account_index <= accounts['totalSize']:
                            account_id = accounts['records'][account_index-1]['Id']
                            sf.Account.delete(account_id)
                            print(f"\nDeleted account {account_id}")
                        else:
                            print("\nInvalid account index")
                    elif option == 2:
                        delete_all = input("\nAre you sure you want to delete all accounts? (yes/no): ")
                        if delete_all.lower() == 'yes':
                            account_ids = [account['Id'] for account in accounts['records']]
                            for account_id in account_ids:
                                sf.Account.delete(account_id)
                                print(f"\nDeleted account {account_id}")
                        else:
                            print("\nDeletion cancelled")
                    elif option == 3:
                        print("\nNo accounts deleted")
                    else:
                        print("\nInvalid option")
                else:
                    print("\nNo accounts found")

            elif action.lower() == 'dc':
                contact_name = input("\nEnter a keyword to lookup contacts: ")

                try:
                    contacts = sf.query(f"SELECT Id, CreatedDate, FirstName, LastName, Email, Title, Department, Phone FROM Contact WHERE FirstName LIKE '%{contact_name}%' OR LastName LIKE '%{contact_name}%' OR Email LIKE '%{contact_name}%'")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    contacts = sf.query(f"SELECT Id, CreatedDate, FirstName, LastName, Email, Title, Department, Phone FROM Contact WHERE FirstName LIKE '%{contact_name}%' OR LastName LIKE '%{contact_name}%' OR Email LIKE '%{contact_name}%'")

                if contacts['totalSize'] > 0:
                    print("\nContacts: (Id, FirstName, LastName, Email, CreatedDate)")
                    for i, contact in enumerate(contacts['records']):
                        print(f"{i+1}. {contact['Id']}: {contact['FirstName']} {contact['LastName']} {contact['Email']} {contact['CreatedDate']}")

                    print("\nOptions:")
                    print("1. Delete a specific contact by number in the list")
                    print("2. Delete all contacts in the list")
                    print("3. Cancel\n")

                    option = int(input("\nEnter your option: "))

                    if option == 1:
                        contact_index = int(input("\nEnter the number of the contact to delete: "))
                        if contact_index > 0 and contact_index <= contacts['totalSize']:
                            contact_id = contacts['records'][contact_index-1]['Id']
                            sf.Contact.delete(contact_id)
                            print(f"\nDeleted contact {contact_id}")
                        else:
                            print("\nInvalid contact index")
                    elif option == 2:
                        delete_all = input("\nAre you sure you want to delete all contacts? (yes/no): ")
                        if delete_all.lower() == 'yes':
                            contact_ids = [contact['Id'] for contact in contacts['records']]
                            for contact_id in contact_ids:
                                sf.Contact.delete(contact_id)
                                print(f"\nDeleted contact {contact_id}")
                        else:
                            print("\nDeletion cancelled")
                    elif option == 3:
                        print("\nNo contacts deleted")
                    else:
                        print("\nInvalid option")
                else:
                    print("No contacts found")

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