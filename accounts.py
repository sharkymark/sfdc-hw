import simple_salesforce
import os

def main():
    username = os.environ['SALESFORCE_USERNAME']
    password = os.environ['SALESFORCE_PASSWORD']
    security_token = os.environ['SALESFORCE_SECURITY_TOKEN']

    # Create a Salesforce connection
    sf = simple_salesforce.Salesforce(username=username, password=password, security_token=security_token)

    while True:
        try:

            # Get the account name to filter by from the user
            account_name = input("Enter the account name to filter by or 'quit' to exit): ")

            if account_name.lower() == 'quit':
                break

            if account_name.lower() == 'describe':
                account_fields = sf.Account.describe()
                for field in account_fields['fields']:
                    print(field['name'])

            else:
                # Query accounts
                query = f"SELECT Id, Name, Description"
                
                additional_columns = input("Enter additional column names besides Id, Name, Description which are in the default query (comma-separated): ")
                if additional_columns:
                    query += ", " + additional_columns
                else:
                    query += " "

                query += f" FROM ACCOUNT WHERE Name LIKE '%{account_name}%'"

                print("query: ", query)

                accounts = sf.query(query)

                # Print column headers
                if additional_columns:
                    columns = ['Id', 'Name', 'Description'] + [column.strip() for column in additional_columns.split(', ')]
                    print(*columns, sep='\t')  # Print column names

                # Print results
                for account in accounts['records']:
                    print(account['Id'], account['Name'], account['Description'], *[

                        account[column] for column in additional_columns.split(', ')

                    ])

        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()