import simple_salesforce
import os
import datetime
from datetime import datetime
import calendar
import requests

def set_default_settings():
    global preferences
    preferences = {
        'account_additional_columns': '',
        'show_contacts': True,
        'contact_additional_columns': '',
        'max_delete_records': 10
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
    preferences['max_delete_records'] = int(input("\nEnter the maximum number of records to delete at one time (e.g., 10): ")) 

def validate_date(date_string):
  """Validates a date string in the format YYYY-MM-DD.

  Args:
    date_string: The date string to validate.

  Returns:
    True if the date is valid, False otherwise.
  """

  try:
    datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return True
  except ValueError:
    return False

def display_account(account_id,account):

    print(f"\nCreated account {account_id}\n")
    print(f"Account Id: {account_id}\nName: {name}\nIndustry: {industry_value}\nType: {type_value}\nDescription: {description}\nWebsite: {website}")

def update_account(sf, account_id):
    account = sf.Account.get(account_id)
    print(f"\nUpdating account {account['Name']}:")

    new_name = input(f"Enter new name ({account['Name']}): ")
    new_website = input(f"Enter new website ({account['Website']}): ")
    new_description = input(f"Enter new description ({account['Description']}): ")

    print(f"Industry picklist values ({account['Industry']}):")
    for i, option in enumerate(industry_options):
        print(f"{i+1}. {option['value']}")

    try:
        industry_choice = int(input("Enter the number for the Industry (0 to skip): "))

        if industry_choice > 0 and industry_choice <= len(industry_options):
            new_industry_value = industry_options[industry_choice - 1]['value']
        else:
            new_industry_value = ''
    except ValueError:
        new_industry_value = ''

    print("Account Type picklist values:")
    for i, option in enumerate(type_options):
        print(f"{i+1}. {option['value']}")
    
    try:
        type_choice = int(input("Enter the number for the Account Type (0 to skip): "))
        
        if type_choice > 0 and type_choice <= len(type_options):
            new_type_value = type_options[type_choice - 1]['value']
        else:
            new_type_value = ''
    except ValueError:
        new_type_value = ''

    if new_name:
        account['Name'] = new_name
    if new_website:
        account['Website'] = new_website
    if new_description:
        account['Description'] = new_description
    if new_industry_value:
        account['Industry'] = new_industry_value
    if new_type_value:
        account['Type'] = new_type_value

    sf.Account.update(account_id, {'Name': account['Name'], 'Website': account['Website'], 'Description': account['Description'], 'Industry': account['Industry'], 'Type': account['Type']})
    print(f"\nUpdated account")

    print(f"Account Id: {account_id}\nName: {account['Name']}\nIndustry: {account['Industry']}\nType: {account['Type']}\nDescription: {account['Description']}\nWebsite: {account.get('Website')}")

def update_contact(sf, contact_id):
    contact = sf.Contact.get(contact_id)
    print(f"\nUpdating contact {contact['FirstName']} {contact['LastName']}:")
    new_first_name = input(f"Enter new first name ({contact['FirstName']}): ")
    new_last_name = input(f"Enter new last name ({contact['LastName']}): ")
    new_email = input(f"Enter new email ({contact['Email']}): ")
    new_title = input(f"Enter new title ({contact['Title']}): ")

    print(f"Lead Source picklist values: ({contact['LeadSource']})")
    for i, option in enumerate(lead_source_options):
        print(f"{i+1}. {option['value']}")

    try:
        lead_source_choice = int(input("Enter the number for the Lead Source: "))

        if lead_source_choice > 0 and lead_source_choice <= len(lead_source_options):
            new_lead_source_value = lead_source_options[lead_source_choice - 1]['value']
        else:
            new_lead_source_value = ''
    except ValueError:
        new_lead_source_value = ''

    new_description = input(f"Enter new description ({contact['Description']}): ")

    if new_first_name:
        contact['FirstName'] = new_first_name
    if new_last_name:
        contact['LastName'] = new_last_name
    if new_email:
        contact['Email'] = new_email
    if new_title:
        contact['Title'] = new_title
    if new_lead_source_value:
        contact['LeadSource'] = new_lead_source_value
    if new_description:
        contact['Description'] = new_description


    sf.Contact.update(contact_id, {'FirstName': contact['FirstName'], 'LastName': contact['LastName'], 'Email': contact['Email'], 'Title': contact['Title'], 'LeadSource': contact['LeadSource'], 'Description': new_description})
    print(f"\nUpdated contact")
    print(f"Contact Id: {contact_id}\nFirst Name: {contact['FirstName']}\nLast Name: {contact['LastName']}\nEmail: {contact['Email']}\nTitle: {contact['Title']}\nLead Source: {contact['LeadSource']}\nDescription: {contact['Description']}")

def delete_accounts(sf, query):
    try:
        accounts = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        accounts = sf.query(query)

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
            if accounts['totalSize'] > preferences['max_delete_records']:
                print(f"\nError: Cannot delete more than {preferences['max_delete_records']} records at one time. Please refine your query or change your preferences from the main menu.")
                return
            delete_all = input("\nAre you sure you want to delete all accounts? (yes/no): ")
            if delete_all.lower() == 'yes':
                account_ids = [account['Id'] for account in accounts['records']]
                for account_id in account_ids:
                    sf.Account.delete(account_id)
                    print(f"\nDeleted account {account_id}")
                print(f"\nDeleted {accounts['totalSize']} accounts")
            else:
                print("\nDeletion cancelled")
        elif option == 3:
            print("\nNo accounts deleted")
        else:
            print("\nInvalid option")
    else:
        print("\nNo accounts found")


def delete_contacts(sf, query):
    try:
        contacts = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        contacts = sf.query(query)

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
            if contacts['totalSize'] > preferences['max_delete_records']:
                print(f"\nError: Cannot delete more than {preferences['max_delete_records']} records at one time. Please refine your query or change your preferences from the main menu.")
                return
            delete_all = input("\nAre you sure you want to delete all contacts? (yes/no): ")
            if delete_all.lower() == 'yes':
                contact_ids = [contact['Id'] for contact in contacts['records']]
                for contact_id in contact_ids:
                    sf.Contact.delete(contact_id)
                    print(f"\nDeleted contact {contact_id}")
                print(f"\nDeleted {contacts['totalSize']} contacts")
            else:
                print("\nDeletion cancelled")
        elif option == 3:
            print("\nNo contacts deleted")
        else:
            print("\nInvalid option")
    else:
        print("No contacts found")


def get_contacts_for_account(sf, account_id):

    account = get_accountdetails(sf, account_id)

    print(f"\nAccount: {account['Name']}")
    print(f"Industry: {account['Industry']}")
    print(f"Type: {account['Type']}")
    print(f"Website: {account['Website']}")
    print(f"Account Id: {account_id}\n")
    print(f"Description: {account.get('Description')}\n")



    # Get contacts for the account
    if preferences['show_contacts']:
        contact_query = f"SELECT Id, AccountId, FirstName, LastName, Email, Title, Phone, Description"
        if preferences['contact_additional_columns']:
            contact_query += ", " + preferences['contact_additional_columns']
        contact_query += f" FROM Contact WHERE AccountId = '{account_id}' ORDER BY LastName"

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
                print("2. Return to account menu")
                print("3. Create a task for a specific contact in the list")
                print("4. List tasks for a specific contact in the list")
                print("5. Exit to main menu\n")

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

                elif option == 3:
                    try:
                        contact_index = int(input("\nEnter the number of the contact to create an activity for: "))
                        if contact_index > 0 and contact_index <= contacts['totalSize']:
                            contact_id = contacts['records'][contact_index-1]['Id']
                            account_id = contacts['records'][contact_index-1]['AccountId']
                            opp_id = ""
                            create_task(sf, contact_id, account_id, opp_id)
                            exit_loop = False
                        else:
                            print("\nInvalid contact index")
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                elif option == 4:
                    try:
                        contact_index = int(input("\nEnter the number of the contact to list tasks for: "))
                        if contact_index > 0 and contact_index <= contacts['totalSize']:
                            contact_id = contacts['records'][contact_index-1]['Id']
                            opp_id = ""
                            get_tasks(sf, contact_id, opp_id)
                            exit_loop = False
                        else:
                            print("\nInvalid contact index")
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                elif option == 5:
                    exit_loop = True

                if exit_loop:
                    exit_loop = False  # Reset exit_loop to False
                    break

        else:
            print("No contacts found")

def get_contactdetails(sf, contact_id):

    # Fetch contact information
    contact_query = f"SELECT Id, AccountId, FirstName, LastName, Title, Email FROM Contact WHERE Id = '{contact_id}' ORDER BY LastName"
    contact_result = sf.query(contact_query)

    if contact_result['totalSize'] > 0:
        return contact_result['records'][0]
    else:
        print(f"\tContact {i+1}: Contact not found")

def get_accountdetails(sf, account_id):

    # Fetch account information
    account_query = f"SELECT Id, Name, Type, Industry, Description, Website FROM Account WHERE Id = '{account_id}' ORDER BY Name"
    account_result = sf.query(account_query)

    if account_result['totalSize'] > 0:
        return account_result['records'][0]
    else:
        print(f"\tAccount {i+1}: Account not found")

def get_contacts(sf):

    search_term = input("\nEnter a search term (first name, last name, email, or title): ")

    try:
        contacts = sf.query(f"SELECT Id, FirstName, LastName, Title, Department, Email, Phone, MailingAddress, Description, LeadSource FROM Contact WHERE FirstName LIKE '%{search_term}%' OR LastName LIKE '%{search_term}%' OR Email LIKE '%{search_term}%' OR Title LIKE '%{search_term}%' ORDER BY LastName")
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        contacts = sf.query(f"SELECT Id, FirstName, LastName, Title, Department, Email, Phone, MailingAddress, Description, LeadSource FROM Contact WHERE FirstName LIKE '%{search_term}%' OR LastName LIKE '%{search_term}%' OR Email LIKE '%{search_term}%' OR Title LIKE '%{search_term}%' ORDER BY LastName")

    if contacts['totalSize'] > 0:
        print("\nContacts:")
        print("#", "Id", "First Name", "Last Name", "Title", "Lead Source", "Email", "Description", sep='\t')
        for i, contact in enumerate(contacts['records']):
            print(f"{i+1}.", contact['Id'], contact['FirstName'], contact['LastName'], contact['Title'], contact['LeadSource'], contact['Email'], contact['Description'])

        return contacts

    else:
        print("No contacts found")  

def delete_contact_roles(sf):
    try:
        contacts = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        contacts = sf.query(query)

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
            if contacts['totalSize'] > preferences['max_delete_records']:
                print(f"\nError: Cannot delete more than {preferences['max_delete_records']} records at one time. Please refine your query or change your preferences from the main menu.")
                return
            delete_all = input("\nAre you sure you want to delete all contacts? (yes/no): ")
            if delete_all.lower() == 'yes':
                contact_ids = [contact['Id'] for contact in contacts['records']]
                for contact_id in contact_ids:
                    sf.Contact.delete(contact_id)
                    print(f"\nDeleted contact {contact_id}")
                print(f"\nDeleted {contacts['totalSize']} contacts")
            else:
                print("\nDeletion cancelled")
        elif option == 3:
            print("\nNo contacts deleted")
        else:
            print("\nInvalid option")
    else:
        print("No contacts found")

def add_contactrole(sf,opp):

    contacts = get_contacts(sf)

    while True:

        print("\nOptions:")
        print("1. Add a specific contact role by number in the list")
        print("2. Cancel\n")
    
        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("\nInvalid entry. Please enter a valid number.")
            continue

        if option == 1:
            try:
                contact_index = int(input("\nEnter the number of the contact to add as a contact role: "))
                if contact_index > 0 and contact_index <= contacts['totalSize']:
                    contact_id = contacts['records'][contact_index-1]['Id']
                    contact_name = contacts['records'][contact_index-1]['FirstName'] + " " + contacts['records'][contact_index-1]['LastName']
                    break
                else:
                    print("\nInvalid contact index")
            except ValueError:
                print("\nInvalid entry. Please enter a valid number.")

        elif option == 2:
            print("\nUpdate cancelled")
            break
        else:
            print("\nInvalid contact index")                    
            continue   

    if 'contact_id' in locals():

        print(f"\nYou selected: {contact_name}\n")

        print("Contact Role picklist values:")
        for i, option in enumerate(opp_contact_role_options):
            print(f"{i+1}. {option['value']}")

        try:
            opp_contact_role_choice = int(input("\nEnter the number for the Contact Role (0 to skip): "))
            if opp_contact_role_choice > 0 and opp_contact_role_choice <= len(opp_contact_role_options):
                opp_contact_role_value = opp_contact_role_options[opp_contact_role_choice - 1]['value']
            else:
                opp_contact_role_value = ''
        except ValueError:
            opp_contact_role_value = ''

        # Get the primary status for the contact
        is_primary = input("\nIs the contact the primary contact? (yes/no): ").lower() == 'yes'

        try:
            contactrole = sf.OpportunityContactRole.create({'OpportunityId': opp['Id'], 'ContactId': contact_id, 'Role': opp_contact_role_value, 'IsPrimary': is_primary})
        except requests.exceptions.ConnectionError:
            sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
            print(reconn)
            contactrole = sf.OpportunityContactRole.create({'OpportunityId': opp['Id'], 'ContactId': contact_id, 'Role': role, 'IsPrimary': is_primary})

        contactrole_id = contactrole.get('id')
        print(f"\nCreated contact role for {contact_name} on opportunity {opp['Name']}\n")    

def get_contactroles(sf, opp):

    # Query contact roles
    query = f"SELECT Id, ContactId, Role, IsPrimary FROM OpportunityContactRole WHERE OpportunityId = '{opp['Id']}'"

    print("\nContact Roles query: ", query)

    print("\nContact Roles:\n")

    try:
        contactroles = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        contactroles = sf.query(query)

    if contactroles['totalSize'] > 0:

        # Print column headers
        print(' ','First Name', 'Last Name', 'Title', 'Account', 'Role', 'IsPrimary', sep='\t')

        # Print results
        for i, contactrole in enumerate(contactroles['records']):
            contact = get_contactdetails(sf, contactrole['ContactId'])
            account = get_accountdetails(sf, contact['AccountId'])
            print(f"{i+1}.", contact['FirstName'], contact['LastName'], contact['Title'], contact['Email'], account['Name'], contactrole['Role'], contactrole['IsPrimary'])

        return contactroles

    else:
        print("No contact roles found")

def update_contactrole(sf,contactrole_id,opp):

    contactrole = sf.OpportunityContactRole.get(contactrole_id)
    contact = get_contactdetails(sf, contactrole['ContactId'])
    account = get_accountdetails(sf, contact['AccountId'])

    print(f"\nUpdating contact role for {contact['FirstName']} {contact['LastName']} on opportunity {opp['Name']}:")

    print(f"\nContact: {contact['FirstName']} {contact['LastName']}")
    print(f"Account: {account['Name']}")
    print(f"Role: {contactrole['Role']}")
    print(f"Is Primary: {contactrole['IsPrimary']}")

    print("\nContact Role picklist values:")
    for i, option in enumerate(opp_contact_role_options):
        print(f"{i+1}. {option['value']}")

    try:
        opp_contact_role_choice = int(input("\nEnter the number for the Contact Role (0 to skip): "))
        if opp_contact_role_choice > 0 and opp_contact_role_choice <= len(opp_contact_role_options):
            opp_contact_role_value = opp_contact_role_options[opp_contact_role_choice - 1]['value']
        else:
            opp_contact_role_value = ''
    except ValueError:
        opp_contact_role_value = ''

    # Get the primary status for the contact
    is_primary = input("\nIs the contact the primary contact? (yes/no): ").lower() == 'yes'

    if opp_contact_role_value:
        contactrole['Role'] = opp_contact_role_value
    if is_primary:
        contactrole['IsPrimary'] = is_primary

    sf.OpportunityContactRole.update(contactrole_id, {'Role': contactrole['Role'], 'IsPrimary': contactrole['IsPrimary']})
    print(f"\nUpdated contact role for {contact['FirstName']} {contact['LastName']} on opportunity {opp['Name']}\n")


def manage_contactroles(sf, opp):

    contactroles = get_contactroles(sf, opp)

    while True:

        print("\nOptions:")
        print("1. Add a contact role in the list")
        print("2. Update a specific contact role in the list")
        print("3. Deassociate a specific contact role in the list")
        print("4. Cancel and return to main menu\n")
    
        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("\nInvalid entry. Please enter a valid number.")
            continue
    
        if option == 1:
            add_contactrole(sf,opp)
            contactroles = get_contactroles(sf, opp)
        elif option == 2:
            try:
                contactrole_index = int(input("\nEnter the number of the contact role to update: "))
                if contactrole_index > 0 and contactrole_index <= contactroles['totalSize']:
                    contactrole_id = contactroles['records'][contactrole_index-1]['Id']
                    update_contactrole(sf,contactrole_id,opp)
                    contactroles = get_contactroles(sf, opp)
                else:
                    print("\nInvalid contact role index")
            except ValueError:
                print("\nInvalid entry. Please enter a valid number.")
        elif option == 3:
            try:
                contactrole_index = int(input("\nEnter the number of the contact role to deassociate: "))
                if contactrole_index > 0 and contactrole_index <= contactroles['totalSize']:
                    contactrole_id = contactroles['records'][contactrole_index-1]['Id']
                    contact_id = contactroles['records'][contactrole_index-1]['ContactId']
                    role = contactroles['records'][contactrole_index-1]['Role']
                    contact = get_contactdetails(sf, contact_id)
                    contact_name = contact['FirstName'] + " " + contact['LastName'] 
                    sf.OpportunityContactRole.delete(contactrole_id)
                    print(f"\nDeleted contact {contact_name} with role {role} from opportunity {opp['Name']}")
                    contactroles = get_contactroles(sf, opp)
                else:
                    print("\nInvalid contact role index")
            except ValueError:
                print("\nInvalid entry. Please enter a valid index.")
        elif option == 4:
            print("\nContact Role action cancelled")
            break
        else:
            print("\nInvalid contact role index")
            break


def update_opportunity(sf, opp):

    account = get_accountdetails(sf, opp['AccountId'])

    print(f"\nUpdating opportunity {opp['Name']} for account {account['Name']}:")

    new_name = input(f"\nEnter new name ({opp['Name']}): ")

    while True:
        new_close_date = input(f"Enter a new close date in format YYYY-MM-DD ({opp['CloseDate']}): ")
        if not new_close_date:  # Check if input is empty
            break  # Exit the loop if empty

        try:
            datetime.strptime(new_close_date, '%Y-%m-%d')
            break  # Valid date, exit the loop
        except ValueError:
            print("Invalid close date format. Please enter in YYYY-MM-DD format.")


    new_amount = input(f"Enter new amount ({opp['Amount']}): ")


    print(f"\nSales Stage picklist values ({opp['StageName']}):")
    for i, option in enumerate(stage_options):
        print(f"{i+1}. {option['value']}")

    try:
        stage_choice = int(input("Enter the number for the Sales Stage (0 to skip): "))
        if stage_choice > 0 and stage_choice <= len(stage_options):
            new_stage_value = stage_options[stage_choice - 1]['value']
        else:
            new_stage_value = ''
    except ValueError:
        new_stage_value = ''


    new_description = input(f"Enter new description ({opp['Description']}): ")
    new_next_step = input(f"Enter new next step ({opp['NextStep']}): ")

    print(f"\nType picklist values ({opp['Type']}):")
    for i, option in enumerate(opp_type_options):
        print(f"{i+1}. {option['value']}")

    try:
        type_choice = int(input("Enter the number for the Type (0 to skip): "))
        if type_choice > 0 and type_choice <= len(opp_type_options):
            new_type_value = opp_type_options[type_choice - 1]['value']
        else:
            new_type_value = ''
    except ValueError:
        new_type_value = ''

    print(f"\nLead Source picklist values ({opp['LeadSource']}):")
    for i, option in enumerate(opp_lead_source_options):
        print(f"{i+1}. {option['value']}")

    try:
        lead_source_choice = int(input("Enter the number for the Lead Source (0 to skip): "))
        if lead_source_choice > 0 and lead_source_choice <= len(opp_lead_source_options):
            new_lead_source_value = opp_lead_source_options[lead_source_choice - 1]['value']
        else:
            new_lead_source_value = ''
    except ValueError:
        new_lead_source_value = ''

    if new_name:
        opp['Name'] = new_name
    if new_close_date:
        opp['CloseDate'] = new_close_date
    if new_amount:
        opp['Amount'] = new_amount
    if new_description:
        opp['Description'] = new_description
    if new_next_step:
        opp['NextStep'] = new_next_step
    if new_type_value:
        opp['Type'] = new_type_value
    if new_lead_source_value:
        opp['LeadSource'] = new_lead_source_value
    if new_stage_value:
        opp['StageName'] = new_stage_value
    
    sf.Opportunity.update(opp['Id'], {'Name': opp['Name'], 'CloseDate': opp['CloseDate'], 'Amount': opp['Amount'], 'Description': opp['Description'], 'NextStep': opp['NextStep'], 'Type': opp['Type'], 'LeadSource': opp['LeadSource'], 'StageName': opp['StageName']})

def build_filter_clause(filter_type):
  """Builds the WHERE clause for the SQL query based on the filter type."""
  now = datetime.now()
  current_year = now.year
  next_year = current_year + 1
  current_quarter = (now.month - 1) // 3 + 1

  # Use date literals for comparisons within WHERE clause
  if filter_type == 1:  # Current Quarter
    start_date = datetime.date(current_year, (current_quarter - 1) * 3 + 1, 1).strftime('%Y-%m-%d')
    end_date = datetime.date(current_year, current_quarter * 3, calendar.monthrange(current_year, current_quarter * 3)[1]).strftime('%Y-%m-%d')
    filter_clause = f"AND CloseDate >= {start_date} AND CloseDate <= {end_date}"
  elif filter_type == 2:  # Next Quarter
    next_quarter = current_quarter + 1 if current_quarter < 4 else 1
    next_year = current_year + 1 if next_quarter == 1 else current_year
    start_date = datetime.date(next_year, (next_quarter - 1) * 3 + 1, 1).strftime('%Y-%m-%d')
    end_date = datetime.date(next_year, next_quarter * 3, calendar.monthrange(next_year, next_quarter * 3)[1]).strftime('%Y-%m-%d')
    filter_clause = f"AND CloseDate >= {start_date} AND CloseDate <= {end_date}"
  elif filter_type == 3:  # Current Calendar Year
    filter_clause = f"AND CloseDate >= {current_year}-01-01 AND CloseDate < {current_year+1}-01-01"  # Use YEAR function for year comparison
  elif filter_type == 4:  # Next Calendar Year
    filter_clause = f"AND CloseDate >= {next_year}-01-01 AND CloseDate < {next_year+1}-01-01"
  elif filter_type == 5:
    filter_clause = "None" # No filter
  else:
    filter_clause = ""  # No filter

  return filter_clause



def get_opportunities(sf, opp_name, stagename, sort, datefilter):

    if not stagename:
        print("\nOpportunity filter options:")
        print("1. Open")
        print("2. Closed won")
        print("3. Closed lost\n")

        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("\nInvalid entry. Will filter open opportunities only.")
            option = 1

        stagename = ""

        if option == 1:
            stagename = " AND (StageName <> 'Closed Won' OR StageName <> 'Closed Lost')"
        elif option == 2:
            stagename = " AND StageName = 'Closed Won'"
        elif option == 3:
            stagename = " AND StageName = 'Closed Lost'"
    

    if not sort:
        print("\nSort options:")
        print("1. Close Date")
        print("2. Opportunity Name A-Z")
        print("3. Revenue Amount descending\n")

        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("\nInvalid entry. Will sort by Amount descending.")
            option = 1

        if option == 1:
            sort = "CloseDate"
        elif option == 2:
            sort = "Name"
        elif option == 3:
            sort = "Amount DESC"

    if not datefilter:
        print("\nDate period options:")
        print("1. Current quarter")
        print("2. Next quarter")
        print("3. Current calendar year")
        print("4. Next calendar year")
        print("5. No date filter\n")

        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("\nInvalid entry. Will not filter by date.")
            option = 5

        datefilter = build_filter_clause(option)

    # Query opps
    query = f"SELECT Id, AccountId, Name, Type, LeadSource, StageName, CloseDate, Amount, Description, NextStep"

    if datefilter == "None":
        finaldatefilter = ""
    else:
        finaldatefilter = datefilter

    query += f" FROM OPPORTUNITY WHERE Name LIKE '%{opp_name}%' {finaldatefilter} {stagename} ORDER BY {sort}"

    print("\nOpportunities query: ", query)

    print("\nOpportunities:\n")

    try:
        opps = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        opps = sf.query(query)

    total_amount = 0

    if opps['totalSize'] > 0:

        # Print column headers
        print(' ', 'Account', 'Opportunity', 'Type', 'Lead Source', 'Sales Stage', 'Close Date', 'Amount', sep='\t')

        # Print results
        for i, opp in enumerate(opps['records']):
            amount_value = opp.get("Amount", 0)
            total_amount += amount_value
            account = get_accountdetails(sf, opp['AccountId'])
            print(f"{i+1}.", account['Name'], opp['Name'], opp['Type'], opp['LeadSource'], opp['StageName'], opp['CloseDate'], opp['Amount'])

        # Print the total amount after iterating through opportunities
        print(f"\nTotal amount: {total_amount}")

        print("\nFilters:")
        print(f"Sales stages: {stagename}")
        print(f"Sort: {sort}")
        print(f"Date filter: {datefilter or 'None'}")

        return opps, stagename, sort, datefilter

    else:
        print("No opportunities found") 


def search_opportunities(sf):


    opp_name = ""
    stagename = ""
    sort = ""
    datefilter = ""

    while True:

        # Get the opportunity name to filter by from the user
        opp_name = input("\nEnter the opportunity name to filter by or 'quit' to exit): ")

        if opp_name.lower() == 'quit':
            break

        while True:

            opps, stagename, sort, datefilter = get_opportunities(sf, opp_name, stagename, sort, datefilter)

            if opps is None:
                return

            print("\nOptions:")
            print("1. Retrieve details by a specific opportunity in the list")
            print("2. Update a specific opportunity in the list")
            print("3. Create a task for a specific opportunity in the list")
            print("4. List tasks for a specific opportunity in the list")
            print("5. Change search and reuse other filters")
            print("6. Cancel and return to main menu\n")
        
            try:
                option = int(input("Enter your option: "))
            except ValueError:
                print("\nInvalid entry. Please enter a valid number.")
                continue
        
            if option == 1:
                try:
                    opp_index = int(input("\nEnter the number of the opportunity to retrieve details: "))
                    if opp_index > 0 and opp_index <= opps['totalSize']:
                        opp_id = opps['records'][opp_index-1]['Id']
                        opp_name = opps['records'][opp_index-1]['Name']
                        opp = opps['records'][opp_index-1]
                        get_opp_details(opp)
                        manage_contactroles(sf, opp)
                    else:
                        print("\nInvalid opp index")
                except ValueError:
                    print("\nInvalid entry. Please enter a valid number.")
            elif option == 2:
                try:
                    opp_index = int(input("\nEnter the number of the opportunity to update: "))
                    if opp_index > 0 and opp_index <= opps['totalSize']:
                        opp_id = opps['records'][opp_index-1]['Id']
                        opp_name = opps['records'][opp_index-1]['Name']
                        opp = opps['records'][opp_index-1]
                        update_opportunity(sf, opp)
                    else:
                        print("\nInvalid opp index")
                except ValueError:
                    print("\nInvalid entry. Please enter a valid number.")
            elif option == 3:
                try:
                    opp_index = int(input("\nEnter the number of the opportunity to create a task for: "))
                    if opp_index > 0 and opp_index <= opps['totalSize']:
                        opp_id = opps['records'][opp_index-1]['Id']
                        account_id = ""
                        contact_id = ""
                        create_task(sf, contact_id, account_id, opp_id)
                    else:
                        print("\nInvalid opp index")
                except ValueError:
                    print("\nInvalid entry. Please enter a valid number.")
            elif option == 4:
                try:
                    opp_index = int(input("\nEnter the number of the opportunity to list tasks for: "))
                    if opp_index > 0 and opp_index <= opps['totalSize']:
                        opp_id = opps['records'][opp_index-1]['Id']
                        account_id = ""
                        contact_id = ""
                        get_tasks(sf, contact_id, opp_id)
                        break
                    else:
                        print("\nInvalid opp index")
                except ValueError:
                    print("\nInvalid entry. Please enter a valid number.")
            elif option == 5:
                print("\nOpportunity action cancelled")
                break
            elif option == 6:
                print("\nOpportunity action cancelled")
                return
            else:
                print("\nInvalid opportunity index")
                break
                    

def get_opp_details(opp):
    print(f"\nOpportunity Details:") 

    print(f"\nName: {opp['Name']}")
    print(f"Sales Stage: {opp['StageName']}")
    print(f"Close Date: {opp['CloseDate']}")
    print(f"Amount: {opp['Amount']}")

    print(f"\nType: {opp['Type']}")
    print(f"Lead Source: {opp['LeadSource']}")

    print(f"\nDescription:\n{opp['Description']}")
    print(f"\nNext Step:\n{opp['NextStep']}\n")
    print(f"\nAccount Id: {opp['AccountId']}")
    print(f"Opportunity Id: {opp['Id']}")

def create_task(sf, contact_id, account_id, opp_id):

    print("\nSubject picklist values:\n")
    for i, option in enumerate(subject_options):
        print(f"{i+1}. {option['value']}")
    print(f"{len(subject_options)+1}. Other (enter a custom value)")

    try:
        subject_choice = int(input("\nEnter the number for the task type: "))

        if subject_choice > 0 and subject_choice <= len(subject_options):
            subject_value = subject_options[subject_choice - 1]['value']
        elif subject_choice == len(subject_options) + 1:
            subject_value = input("\nEnter a custom task type: ")
        else:
            subject_value = ''
    except ValueError:
        subject_value = ''

    description = input("\nEnter the description of the task: ")

    if account_id:
        what = "Account"
        what_id = account_id
    elif opp_id:
        what = "Opportunity"
        what_id = opp_id
    else:
        what = ""
        what_id = ""

    associate_with_what = input(f"\nAssociate with {what}? (y/n): ")

    try:
        sf.Task.create({
            'Subject': subject_value,
            'Description': description,
            'Status': 'Completed',
            'Priority': 'Normal',
            'WhoId': contact_id,
            'WhatId': what_id
        })
        print("\nTask record created successfully!\n")
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        sf.Task.create({
            'Subject': subject,
            'Description': description,
            'Status': 'Completed',
            'Priority': 'Normal',
            'WhoId': contact_id,
            'WhatId': what_id
        })
        print("\nTask record created successfully!\n")

def print_contacts(query, contacts):

    print("\nFiltered contacts:\n")
    for i, contact in enumerate(contacts['records']):
        print(f"{i+1}.")
        print(f"Contact Id: {contact['Id']}")
        print(f"Account: {contact['Account']['Name']}")
        print(f"Account Id: {contact['AccountId']}")
        print(f"First Name: {contact['FirstName']}")
        print(f"Last Name: {contact['LastName']}")
        print(f"Title: {contact['Title']}")
        print(f"Lead Source: {contact['LeadSource']}")
        print(f"Department: {contact['Department']}")
        print(f"Email: {contact['Email']}")
        print(f"Phone: {contact['Phone']}")
        print(f"Mailing Address: {contact['MailingAddress']}")
        print(f"Description: {contact['Description']}\n")

def format_datetime(dt_str):
    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt.strftime("%Y-%m-%d %I:%M %p")

def get_tasks(sf, contact_id, opp_id):

    if contact_id:
        who_what_query = f", Who.FirstName, Who.LastName, WhoId FROM Task WHERE WhoId = '{contact_id}'"
    elif opp_id:
        who_what_query = f", WhatId FROM Task WHERE WhatId = '{opp_id}'"
     
    query = f"SELECT Id, Subject, Description, Status, Priority, CreatedDate, CreatedById, Account.Name, CreatedBy.Name{who_what_query} ORDER BY CreatedDate DESC"

    print("\nTasks query: ", query)

    print("\nTasks:\n")

    try:
        tasks = sf.query(query)
    except requests.exceptions.ConnectionError:
        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
        print(reconn)
        tasks = sf.query(query)

    if tasks['totalSize'] > 0:

        # Print results
        for i, task in enumerate(tasks['records']):
            print(f"\n{i+1}.")
            print(f"{format_datetime(task['CreatedDate'])}")
            if contact_id:
                print(f"To: {task['Who']['FirstName']} {task['Who']['LastName']}")
            print(f"Created by: {task['CreatedBy']['Name']}")
            print(f"Subject: ", task['Subject'])
            print(f"Description: ", task['Description'])
            print(f"Status: ", task['Status'])
            print(f"Priority: ", task['Priority'])

    else:
        print("No tasks found")

def search_contacts(sf):

    exit_sc = False
    while not exit_sc:

        search_term = input("\nEnter a search term (account name, first name, last name, email, or title) or 'quit' to exit: ")

        if search_term.lower() == 'quit':
            break

        query = f"""
        SELECT Contact.Id, Account.Name, Contact.AccountId, Contact.FirstName, Contact.LastName, Contact.Title, Contact.Department, Contact.Email, Contact.Phone, Contact.MailingAddress, Contact.Description, Contact.LeadSource FROM Contact 
        WHERE (FirstName LIKE '%{search_term}%' OR LastName LIKE '%{search_term}%' OR Email LIKE '%{search_term}%' OR Title LIKE '%{search_term}%' OR Account.Name LIKE '%{search_term}%')
        AND Contact.AccountId != NULL
        ORDER BY LastName
        """

        try:
            contacts = sf.query(query)
        except requests.exceptions.ConnectionError:
            sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
            print(reconn)
            contacts = sf.query(query)
            print(f"Contact query: ", query)
        
        if contacts['totalSize'] > 0:
        
            print_contacts(query, contacts)

            while True:
                

                print("\nOptions:")
                print("1. Update a specific contact by number in the list")
                print("2. Re-enter search criteria")
                print("3. Create a task for a specific contact in the list")
                print("4. List tasks for a specific contact in the list")
                print("5. Exit to main menu\n")
            
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
                            account_id = contacts['records'][contact_index-1]['AccountId']
                            update_contact(sf, contact_id)
                            break
                        else:
                            print("\nInvalid contact index")
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")

                elif option == 2:
                    break
                elif option == 3:
                    try:
                        contact_index = int(input("\nEnter the number of the contact to create an activity for: "))
                        if contact_index > 0 and contact_index <= contacts['totalSize']:
                            contact_id = contacts['records'][contact_index-1]['Id']
                            account_id = contacts['records'][contact_index-1]['AccountId']
                            opp_id = ""
                            create_task(sf, contact_id, account_id, opp_id)
                        else:
                            print("\nInvalid contact index")
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                elif option == 4:
                    try:
                        contact_index = int(input("\nEnter the number of the contact to list tasks for: "))
                        if contact_index > 0 and contact_index <= contacts['totalSize']:
                            contact_id = contacts['records'][contact_index-1]['Id']
                            opp_id = ""
                            get_tasks(sf, contact_id, opp_id)
                        else:
                            print("\nInvalid contact index")
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                elif option == 5:
                    exit_sc = True
                    break
                else:
                    print("\nInvalid contact index")                    
                    continue   

        else:
            print("No contacts found")


def get_account_picklists(sf):
    account_fields = sf.Account.describe()
    picklists = {}
    for field in account_fields['fields']:
        if field['type'] == 'picklist':
            picklists[field['name']] = field['picklistValues']
    return picklists

def get_contact_picklists(sf):
    contact_fields = sf.Contact.describe()
    picklists = {}
    for field in contact_fields['fields']:
        if field['type'] == 'picklist':
            picklists[field['name']] = field['picklistValues']
    return picklists

def get_opp_picklists(sf):
    opp_fields = sf.Opportunity.describe()
    picklists = {}
    for field in opp_fields['fields']:
        if field['type'] == 'picklist':
            picklists[field['name']] = field['picklistValues']
    return picklists

def get_opp_contact_role_picklists(sf):
    ocr_fields = sf.OpportunityContactRole.describe()
    picklists = {}
    for field in ocr_fields['fields']:
        if field['type'] == 'picklist':
            picklists[field['name']] = field['picklistValues']
    return picklists

def get_task_picklists(sf):
    task_fields = sf.Task.describe()
    picklists = {}
    for field in task_fields['fields']:
        if field['type'] == 'picklist':
            picklists[field['name']] = field['picklistValues']

    return picklists

def main():

    global username
    global password
    global security_token
    global lead_source_options
    global industry_options
    global type_options
    global opp_type_options
    global stage_options
    global opp_lead_source_options
    global opp_contact_role_options
    global subject_options

    username = os.environ['SALESFORCE_USERNAME']
    password = os.environ['SALESFORCE_PASSWORD']
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']
    firstconn = "\nConnected to Salesforce - first time\n"
    reconn = "\nReconnected to Salesforce\n"


    exit_loop = False

    # Set default settings when the program starts
    set_default_settings()

    # Create a Salesforce connection
    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
    print(firstconn)

    account_picklists = get_account_picklists(sf)
    contact_picklists = get_contact_picklists(sf)
    opp_picklists = get_opp_picklists(sf)
    opp_contact_role_picklists = get_opp_contact_role_picklists(sf)
    task_picklists = get_task_picklists(sf)

    # Access picklist values for a specific field
    lead_source_options = contact_picklists.get('LeadSource', [])
    industry_options = account_picklists.get('Industry', [])
    type_options = account_picklists.get('Type', [])
    opp_type_options = opp_picklists.get('Type', [])
    stage_options = opp_picklists.get('StageName', [])
    opp_lead_source_options = opp_picklists.get('LeadSource', [])
    opp_contact_role_options = opp_contact_role_picklists.get('Role', [])
    subject_options = task_picklists.get('TaskSubtype', [])

    while True:
        try:

            print("\x1b[5 q")

            print("\n==============================================================================")
            print("**Warning:** Admin users or those with elevated rights, proceed with caution!")
            print("==============================================================================\n")

            action = input("""Enter:
            'sa' to search or update accounts (and contacts),
            'sc' to search or update contacts,
            'so' to search or update opportunities,
            'ca' to create an account,
            'cc' to create a contact,
            'co' to create an opportunity,
            'da' to delete an account,
            'dc' to delete a contact,
            'd' to describe object schemas,
            'pl' to show opportunity, account, contact, contact role picklists,
            'p' for global preferences,
            'q' to exit:
            
            """)

            if action.lower() == 'q':
                break

            elif action.lower() == 'pl':                 
                print("\nAccount Picklists:\n")
                account_picklists = sf.Account.describe()['fields']
                for field in account_picklists:
                    if field['picklistValues']:
                        print(f"{field['name']}:")
                        for value in field['picklistValues']:
                            print(f"  {value['value']}")                
                print("\nContact Picklists:\n")
                contact_picklists = sf.Contact.describe()['fields']
                for field in contact_picklists:
                    if field['picklistValues']:
                        print(f"{field['name']}:")
                        for value in field['picklistValues']:
                            print(f"  {value['value']}")
                print("\nOpportunity Picklists:\n")
                opportunity_picklists = sf.Opportunity.describe()['fields']
                for field in opportunity_picklists:
                    if field['picklistValues']:
                        print(f"{field['name']}:")
                        for value in field['picklistValues']:
                            print(f"  {value['value']}")  
                print("\nOpportunity Contact Role Picklists:\n")
                opportunity_contact_role_picklists = sf.OpportunityContactRole.describe()['fields']
                for field in opportunity_contact_role_picklists:
                    if field['picklistValues']:
                        print(f"{field['name']}:")
                        for value in field['picklistValues']:
                            print(f"  {value['value']}") 
                print("\nTask Picklists:\n")
                task_picklists = sf.Task.describe()['fields']
                for field in task_picklists:
                    if field['picklistValues']:
                        print(f"{field['name']}:")
                        for value in field['picklistValues']:
                            print(f"  {value['value']}") 

            elif action.lower() == 'co':

                account_name = input("\nAn account must already exist to create an opportunity. Enter account name to lookup id: ")

                try:
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%' ORDER BY Name")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%' ORDER BY Name")


                if account_results['totalSize'] == 0:
                    print("\nNo accounts found")
                elif account_results['totalSize'] == 1:
                    account_id = account_results['records'][0]['Id']
                    full_account_name = account_results['records'][0]['Name']
                    print(f"\nFound account: {account_results['records'][0]['Name']} with Id: {account_id}\n")
                else:
                    print("\nMultiple accounts\n")
                    for i, account in enumerate(account_results['records']):
                        print(f"{i+1}. {account['Name']}")
                    try:
                        selection = int(input(f"Select the correct account (1-{account_results['totalSize']}): "))
                        account_id = account_results['records'][selection-1]['Id']
                        full_account_name = account_results['records'][selection-1]['Name']
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                        continue

                if 'account_id' in locals():

                    name = input("Enter opportunity name: ")
                    while True:
                        close_date = input("Enter close date (YYYY-MM-DD): ")
                        try:
                            datetime.datetime.strptime(close_date, '%Y-%m-%d')
                            break  # Valid date, exit the loop
                        except ValueError:
                            print("Invalid close date format. Please enter in YYYY-MM-DD format.")

                    amount = input("Enter amount: ")

                    print("Opportunity Type picklist values:")
                    for i, option in enumerate(opp_type_options):
                        print(f"{i+1}. {option['value']}")

                    try:
                        type_choice = int(input("Enter the number for the Opportunity Type (0 to skip): "))
                        if type_choice > 0 and type_choice <= len(type_options):
                            type_value = type_options[type_choice - 1]['value']
                        else:
                            type_value = ''
                    except ValueError:
                        type_value = ''

                    print("Sales Stage picklist values:")
                    for i, option in enumerate(stage_options):
                        print(f"{i+1}. {option['value']}")

                    try:
                        stage_choice = int(input("Enter the number for the Sales Stage (0 to skip): "))
                        if stage_choice > 0 and stage_choice <= len(stage_options):
                            stage_value = stage_options[stage_choice - 1]['value']
                        else:
                            stage_value = ''
                    except ValueError:
                        stage_value = ''

                    print("Lead Source picklist values:")
                    for i, option in enumerate(opp_lead_source_options):
                        print(f"{i+1}. {option['value']}")

                    try:
                        source_choice = int(input("Enter the number for the Lead Source (0 to skip): "))
                        if source_choice > 0 and source_choice <= len(opp_lead_source_options):
                            source_value = opp_lead_source_options[source_choice - 1]['value']
                        else:
                            source_value = ''
                    except ValueError:
                        source_value = ''


                    description = input("Enter opportunity description: ")
                    next_step = input("Enter next step: (MM 7/26: 2nd demo to broader audience) ")

                    try:
                        opportunity = sf.Opportunity.create({'AccountId': account_id, 'Name': name,  'Type': type_value, 'StageName': stage_value,  'LeadSource': source_value, 'CloseDate': close_date, 'Amount': amount, 'Description': description, 'NextStep': next_step})
                    except requests.exceptions.ConnectionError:
                        sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                        print(reconn)
                        opportunity = sf.Opportunity.create({'AccountId': account_id, 'Name': name,  'Type': type_value, 'StageName': stage_value,  'LeadSource': source_value, 'CloseDate': close_date, 'Amount': amount, 'Description': description, 'NextStep': next_step})

                    opportunity_id = opportunity.get('id')
                    print(f"\nCreated opportunity {opportunity_id}\n")
                    print(f"Opportunity Id: {opportunity_id}\nAccount Name: {full_account_name}\nName: {name}\nType: {type_value}\nStage: {stage_value}\nLead Source: {source_value}\nClose Date: {close_date}\nAmount: {amount}\nDescription: {description}\nNext Step: {next_step}\n")





            elif action.lower() == 'ca':
                name = input("Enter account name: ")
                website = input("Enter account website: ")
                description = input("Enter account description: ")

                print("Industry picklist values:")
                for i, option in enumerate(industry_options):
                    print(f"{i+1}. {option['value']}")
                
                try:
                    industry_choice = int(input("Enter the number for the Industry (0 to skip): "))
                    if industry_choice > 0 and industry_choice <= len(industry_options):
                        industry_value = industry_options[industry_choice - 1]['value']
                    else:
                        industry_value = ''
                except ValueError:
                    industry_value = ''

                print("Account Type picklist values:")
                for i, option in enumerate(type_options):
                    print(f"{i+1}. {option['value']}")
                
                try:
                    type_choice = int(input("Enter the number for the Account Type (0 to skip): "))
                
                    if type_choice > 0 and type_choice <= len(type_options):
                        type_value = type_options[type_choice - 1]['value']
                    else:
                        type_value = ''
                except ValueError:
                    type_value = ''

                try:
                    account = sf.Account.create({'Name': name, 'Website': website, 'Description': description, 'Industry': industry_value, 'Type': type_value})
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    account = sf.Account.create({'Name': name, 'Website': website, 'Description': description, 'Industry': industry_value, 'Type': type_value})

                
                account_id = account.get('id')  # Get the account ID from the response
                print(f"\nCreated account {account_id}\n")
                print(f"Account Id: {account_id}\nName: {name}\nIndustry: {industry_value}\nType: {type_value}\nDescription: {description}\nWebsite: {website}")

            elif action.lower() == 'cc':


                account_name = input("\nAn account must already exist to create a contact. Enter account name to lookup id: ")

                try:
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%' ORDER BY Name")
                except requests.exceptions.ConnectionError:
                    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)
                    print(reconn)
                    account_results = sf.query(f"SELECT Id, Name FROM Account WHERE Name LIKE '%{account_name}%' ORDER BY Name")


                if account_results['totalSize'] == 0:
                    print("\nNo accounts found")
                elif account_results['totalSize'] == 1:
                    account_id = account_results['records'][0]['Id']
                    print(f"\nFound account: {account_results['records'][0]['Name']} with Id: {account_id}\n")
                else:
                    print("\nMultiple accounts found:\n")
                    for i, account in enumerate(account_results['records']):
                        print(f"{i+1}. {account['Name']}")
                    try:
                        selection = int(input(f"Select the correct account (1-{account_results['totalSize']}): "))
                        account_id = account_results['records'][selection-1]['Id']
                    except ValueError:
                        print("\nInvalid entry. Please enter a valid number.")
                        continue

                if 'account_id' in locals():
                    # rest of the code remains the same

                    first_name = input("Enter contact first name: ")
                    last_name = input("Enter contact last name: ")
                    email = input("Enter contact email: ")
                    phone = input("Enter contact phone: ")
                    title = input("Enter contact title: ")
                    description = input("Enter contact description: ")
                    print("Lead Source picklist values:")
                    for i, option in enumerate(lead_source_options):
                        print(f"{i+1}. {option['value']}")

                    try:
                        lead_source_choice = int(input("Enter the number for the Lead Source: "))

                        if lead_source_choice > 0 and lead_source_choice <= len(lead_source_options):
                            lead_source_value = lead_source_options[lead_source_choice - 1]['value']
                        else:
                            lead_source_value = ''
                    except ValueError:
                        lead_source_value = ''

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
                        'LeadSource': lead_source_value,
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

            elif action.lower() == 'so':

                search_opportunities(sf)

            elif action.lower() == 'sa':

                # Get the account name to filter by from the user
                account_name = input("\nEnter the account name to filter by or 'quit' to exit): ")

                if account_name.lower() == 'quit':
                    break

                else:

                    # Query accounts
                    query = f"SELECT Id, Name, Type, Website, Industry"
                    
                    if preferences['account_additional_columns']:
                        query += ", " + preferences['account_additional_columns']
                    else:
                        query += " "

                    query += f" FROM ACCOUNT WHERE Name LIKE '%{account_name}%' ORDER BY Name"

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
                            columns = ['Id', 'Name', 'Type', 'Industry', 'Website'] + [column.strip() for column in preferences['account_additional_columns'].split(', ')]
                            print(*columns, sep='\t')  # Print column names
                        else:
                            print('Id', 'Name', 'Type', 'Industry', 'Website', sep='\t')  # Print default column names

                        # Print results
                        for i, account in enumerate(accounts['records']):
                            print(f"{i+1}.", account['Id'], account['Name'], account['Type'], account['Industry'], account.get('Website', ''), *[
                                account[column] for column in preferences['account_additional_columns'].split(', ') if column.strip() != ''
                            ])

                        exit_loop = False

                        while True:

                            print("\nOptions:")
                            print("1. Update a specific account by number in the list")
                            print("2. Retrieve account details and contacts by a specific account in the list")
                            print("3. Cancel and return to main menu\n")
                        
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
                                account_index = int(input("\nEnter the number of the account to retrieve contacts: "))
                                if account_index > 0 and account_index <= accounts['totalSize']:
                                    account_id = accounts['records'][account_index-1]['Id']
                                    get_contacts_for_account(sf, account_id)
                                else:
                                    print("\nInvalid account index")
                            elif option == 3:
                                print("\nUpdate or Retrieve Contacts cancelled")
                                break
                            else:
                                print("\nInvalid account index")
                                break

                    else:
                        print("No accounts found")                     
                    
            elif action.lower() == 'sc':

                search_contacts(sf)

            elif action.lower() == 'da':
                account_name = input("\nEnter a partial account name to lookup accounts to delete: ")

                if account_name.lower() == 'quit':
                    break
                else:
                    query = f"SELECT Id, CreatedDate, Name FROM Account WHERE Name LIKE '%{account_name}%' ORDER BY Name"
                    delete_accounts(sf, query)

            elif action.lower() == 'dc':
                contact_name = input("\nEnter a partial name or email to lookup contacts to delete: ")
                query = f"SELECT Id, CreatedDate, FirstName, LastName, Email, Title, Department, Phone FROM Contact WHERE FirstName LIKE '%{contact_name}%' OR LastName LIKE '%{contact_name}%' OR Email LIKE '%{contact_name}%' ORDER BY LastName"
                delete_contacts(sf, query)

            elif action.lower() == 'd':
                print("\nDescribe the account object:\n")
                account_fields = sf.Account.describe()
                for field in account_fields['fields']:
                    print(field['name'])
                print("\nDescribe the contact object:\n")
                contact_fields = sf.Contact.describe()
                for field in contact_fields['fields']:
                    print(field['name'])
                print("\nDescribe the opportunity object:\n")
                opp_fields = sf.Opportunity.describe()
                for field in opp_fields['fields']:
                    print(field['name'])  
                print("\nDescribe the opportunity contact role object:\n")
                cr_fields = sf.OpportunityContactRole.describe()
                for field in cr_fields['fields']:
                    print(field['name'])
                print("\nDescribe the Task object:\n")
                cr_fields = sf.Task.describe()
                for field in cr_fields['fields']:
                    print(field['name'])

            elif action.lower() == 'p':
                change_settings()

        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()