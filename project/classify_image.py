import json
import base64
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer

# Specify your deployed endpoint name here
ENDPOINT = "image-classification-2024-08-31-17-11-24-937" #"your-endpoint-name"

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