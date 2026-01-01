import boto3
import json
from botocore.exceptions import ClientError

def get_secrets():
    secret_name = "tadawul-secrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        raise e

    # Decrypts secret using the associated KMS key
    secret = get_secret_value_response['SecretString']
    
    # Convert the JSON string into a Python Dictionary
    secret_dict = json.loads(secret)
    
    return secret_dict

# Simple test to run locally (python aws_secrets.py)
if __name__ == "__main__":
    secrets = get_secrets()
    print("Success! Keys found:", list(secrets.keys()))