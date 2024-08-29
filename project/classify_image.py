import json
import sagemaker
import base64
from sagemaker.predictor import Predictor
from sagemaker.serializers import IdentitySerializer

# Specify your deployed endpoint name here
ENDPOINT = "image-classification-2024-08-29-03-05-20-569"#"your-endpoint-name"

def lambda_handler(event, context):

    # Decode the base64 image data
    image = base64.b64decode(event["body"]["image_data"])

    # Instantiate the SageMaker Predictor
    predictor = Predictor(endpoint_name=ENDPOINT)
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction using the SageMaker model
    inferences = predictor.predict(image)
    
    # Return the inferences in the event
    event["inferences"] = json.loads(inferences.decode('utf-8'))
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
