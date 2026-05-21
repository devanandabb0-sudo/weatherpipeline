import json
import boto3
from decimal import Decimal

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('WeatherData')   # your table name
BUCKET_NAME = "weather-bucket-200"        # your S3 bucket

def lambda_handler(event, context):

    for record in event['Records']:
        body = json.loads(record['body'])

        # Save to DynamoDB
        item = {
            "weatherid": body["weatherid"],
            "timestamp": body["timestamp"],
            "city": body["city"],
            "temperature": Decimal(str(body["temperature"])),
            "humidity": Decimal(str(body["humidity"])),
            "weather": body["weather"]
        }

        table.put_item(Item=item)

        # Save to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{body['weatherid']}.json",
            Body=json.dumps(body)
        )

    return {
        "statusCode": 200,
        "body": "Data saved to DynamoDB and S3"
    }