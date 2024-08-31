import json

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
