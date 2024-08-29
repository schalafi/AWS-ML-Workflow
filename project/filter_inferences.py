import json

# Define your confidence threshold
THRESHOLD = 0.93

def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event["inferences"]
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(float(inference) >= THRESHOLD for inference in inferences)
    
    # If the threshold is met, pass the data back to the Step Function
    if meets_threshold:
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
