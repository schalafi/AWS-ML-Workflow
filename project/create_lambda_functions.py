import boto3
from sagemaker import get_execution_role
from zipfile import ZipFile

import os
import zipfile
import subprocess

# Get the SageMaker execution role
#role = get_execution_role()

# Create a Lambda client using Boto3
#client = boto3.client('lambda')

# Function to create Lambda function from a Python file
def create_lambda_function(client,function_name, file_name, role_arn,timeout):
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
        Timeout=timeout,
        MemorySize=1024,
        Publish=True,
        Role=role_arn
    )
    
    print(f'Created Lambda function: {function_name}')
    return response




def create_deployment_package(source_dir, output_file, dependencies= None):
    # Create the 'package' directory inside source_dir
    package_dir = os.path.join(source_dir, 'package')
    
    # Clean up any previous package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    if dependencies:
        # Install dependencies for the specific platform and Python version
        for dependency in dependencies:
            subprocess.run(
                f"pip install --platform manylinux2014_x86_64 --target={package_dir} "
                f"--implementation cp --python-version 3.8 --only-binary=:all: --upgrade {dependency}",
                shell=True,
                check=True
            )

    # Create the deployment package zip file
    subprocess.run(f"cd {package_dir} && zip -r ../{output_file} .", shell=True, check=True)
    
    # Add the lambda_function.py to the root of the zip file
    subprocess.run(f"cd {source_dir} && zip {output_file} lambda_function.py", shell=True, check=True)

    print(f"Deployment package {output_file} created successfully!")

# Call the function to create the deployment package
source_dir = 'my_function'
output_file = 'package.zip'
dependencies = ['boto3', 'urllib3<2.0']  # Adjust dependencies as needed

create_deployment_package(source_dir, output_file, dependencies)

### USAGE

# Define role ARN
#role_arn = 'arn:aws:iam::565094796913:role/lambda_full_access'

# Create 3 Lambda functions
#create_lambda_function('serializeImageData', 'serialize_image_data', role_arn)
#create_lambda_function('classifyImage', 'classify_image', role_arn)
#create_lambda_function('filterInferences', 'filter_inferences', role_arn)
