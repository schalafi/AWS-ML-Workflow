import boto3
from sagemaker import get_execution_role
from zipfile import ZipFile

# Get the SageMaker execution role
role = get_execution_role()

# Create a Lambda client using Boto3
client = boto3.client('lambda')

# Function to create Lambda function from a Python file
def create_lambda_function(function_name, file_name, role_arn):
    # Zip the lambda_function.py file
    with ZipFile(f'{file_name}.zip', 'w') as z:
        z.write(f'{file_name}.py')
    
    # Read the zipped file content
    with open(f'{file_name}.zip', 'rb') as f:
        b_code = f.read()

    # Create the Lambda function
    response = client.create_function(
        FunctionName=function_name,
        Runtime='python3.9',
        Handler=f'{file_name}.lambda_handler',  # lambda handler entry point
        Code={'ZipFile': b_code},
        Description=f'{function_name} for image classification workflow',
        Timeout=30,
        MemorySize=1024,
        Publish=True,
        Role=role_arn
    )
    
    print(f'Created Lambda function: {function_name}')
    return response

# Define role ARN
role_arn = 'arn:aws:iam::565094796913:role/lambda_full_access'

# Create 3 Lambda functions
create_lambda_function('serializeImageData', 'serialize_image_data', role_arn)
create_lambda_function('classifyImage', 'classify_image', role_arn)
create_lambda_function('filterInferences', 'filter_inferences', role_arn)
