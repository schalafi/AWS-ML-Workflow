import json
import base64
import sagemaker
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer

# Specify your deployed endpoint name here
ENDPOINT = "image-classification-2024-08-31-17-11-24-937" #"your-endpoint-name"

def lambda_handler(event, context):
    
    # Decode the image data
    image_data = base64.b64decode(event["body"]["image_data"])
    
    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(endpoint_name=ENDPOINT)
    
    # For this model, the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction
    inferences = predictor.predict(image_data)
    
    # Convert inferences to a string if needed
    inferences_str = inferences.decode('utf-8')
    
    # Extract the inferences from the response
    inferences_data = json.loads(inferences_str)

    # Return only the inferences
    return {
        'statusCode': 200,
        'body': json.dumps({
            'inferences': inferences_data
        })
    }



import boto3
import base64

s3 = boto3.client('s3')

# we need our function to have AmazonS3FullAccess

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"]
    bucket = event["s3_bucket"]
    
    # Download the data from S3 to /tmp/image.png
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # Read the data from the file and encode it in base64
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')  # Convert to string

    # Pass the data back to the Step Function
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# Define your confidence threshold
THRESHOLD = 0.93

def lambda_handler(event, context):
    
    
   # Parse the body from the event if it's a JSON string
    body = event.get("body")
    if isinstance(body, str):
        body = json.loads(body)  # Convert the string to a dictionary
    
    # Grab the inferences from the parsed body
    inferences = body.get("inferences", [])
    
    
    # Check if any values in our inferences are above the THRESHOLD
    meets_threshold = any(float(inference) >= THRESHOLD for inference in inferences)
    
    # Extract the inferences from the response
    inferences_data = json.loads(str(inferences))

    
    # If the threshold is met, pass the data back to the Step Function
    if meets_threshold:
        return {
            'statusCode': 200,
            'body': json.dumps({
                            'inferences': inferences_data
                        }),
            'threshold_met': True
        }
    else:
        # Return a custom response indicating no inferences above the threshold
        return {
            'statusCode': 400,
            'errorMessage': "THRESHOLD_CONFIDENCE_NOT_MET",
            'threshold_met': False
        }
