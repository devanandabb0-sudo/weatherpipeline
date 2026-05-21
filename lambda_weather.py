import json
import urllib.request
import boto3
import uuid
from decimal import Decimal
from datetime import datetime

# AWS services
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weatherData1')

s3 = boto3.client('s3')
BUCKET_NAME = "weather-bucket-200"   # 👈 replace with your S3 bucket

API_KEY = "b2bab0e80087bf244798527721cf88b6"

def lambda_handler(event, context):

    city = "Kozhikode"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    temperature = Decimal(str(data['main']['temp']))
    humidity = Decimal(str(data['main']['humidity']))
    weather = data['weather'][0]['description']

    item = {
        "weatherid": str(uuid.uuid4()),
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "weather": weather,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 🔹 Save to DynamoDB
    table.put_item(Item=item)

    # 🔹 Prepare data for S3 (Decimal → float)
    s3_data = {
        "weatherid": item["weatherid"],
        "city": item["city"],
        "temperature": float(item["temperature"]),
        "humidity": float(item["humidity"]),
        "weather": item["weather"],
        "timestamp": item["timestamp"]
    }

    # 🔹 Save to S3
    file_name = f"weather-data/{item['weatherid']}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(s3_data)
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Data saved to DynamoDB and S3")
    }