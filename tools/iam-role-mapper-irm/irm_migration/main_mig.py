## Code for the implementation
import csv
import boto3


class MigrationUtility:
    def __init__(self, gcloud_invoke, rules_file, gcloud_output, output_folder):
        self.gcloud_invoke = gcloud_invoke
        self.rules_file = rules_file
        self.gcloud_output = gcloud_output
        self.output_folder = output_folder

    def get_aws_users_and_policies(self):
        # Initialize a new session using AWS IAM credentials from AWS CLI configuration
        session = boto3.Session()

        # Create a client for AWS Organizations
        organizations_client = session.client('organizations')

        # Fetch AWS Organization information
        try:
            accounts = []
            response = organizations_client.list_accounts()

            while True:
                accounts += response['Accounts']
                if 'NextToken' not in response:
                    break
                response = organizations_client.list_accounts(NextToken=response['NextToken'])

            # Iterate through AWS accounts
            for account in accounts:
                account_id = account['Id']
                account_name = account['Name']
                email = organizations_client.describe_account(AccountId=account_id)['Account']['Email']

                # Create a client for IAM using the session (no need to specify region)
                iam_client = session.client('iam', region_name=None)

                # Fetch IAM users for the current account
                users = iam_client.list_users()

                print(f"Account Name: {account_name}, Account ID: {account_id}, Email: {email}")

                # Iterate through IAM users
                if 'Users' in users:
                    for user in users['Users']:
                        user_name = user['UserName']
                        print(f"  IAM User: {user_name}")

                        # Fetch attached IAM policies for the current user
                        attached_policies = iam_client.list_attached_user_policies(UserName=user_name)

                        # Print attached policies
                        if 'AttachedPolicies' in attached_policies:
                            for policy in attached_policies['AttachedPolicies']:
                                policy_name = policy['PolicyName']
                                print(f"    Attached Policy: {policy_name}")

                print("\n")

    def load_rules(self):
        with open(self.rules_file,"r") as rules:
            reader = csv.reader(rules)


    def convert_to_gcp(self, aws_list):
        ## Logic
        # PARAMETERS used:
        #   1. aws_map{}, gcp_map{}, no_rules_list{}
        # The aws_list is a map of email_id as key and list of roles as value
        # For every key, get the value list out and for every element in the list compare if the value is in the first
        # column of the sheet
        # if the value exists, replace the list with the gcp value and if there is no value populate that in a separate map with
        # the key as the emailid and the unknown aws_roles as list and remove the aws_roles from the previous list.
        #
        # The unknown list can be used to generate the reports
        # The general format of gcloud commands are gcloud
        pass

    def migrate_roles(self):
        pass

def run_migration(gcloud_invoke, rules_file, gcloud_output, output_folder):
    migration_utility = MigrationUtility(gcloud_invoke=gcloud_invoke, rules_file=rules_file,
                                         gcloud_output=gcloud_output,
                                         output_folder=output_folder)
    migration_utility.load_rules()
    migration_utility.migrate_roles()
