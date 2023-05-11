import boto3
from PIL import Image
import io

def resize_images(event, context):
    # Retrieve the bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Download the original image from the source S3 bucket
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        image_content = response['Body'].read()

        # Resize the image
        image = Image.open(io.BytesIO(image_content))
        resized_image = image.resize((800, 600))  # Adjust the dimensions as per your requirement

        # Convert the resized image to bytes
        output = io.BytesIO()
        resized_image.save(output, format='JPEG')
        resized_image_content = output.getvalue()

        # Upload the resized image to the destination S3 bucket
        destination_bucket_name = 'your-destination-bucket-name'  # Replace with your destination bucket name
        destination_object_key = 'resized/' + object_key  # Modify the object key or path as desired
        s3_client.put_object(Body=resized_image_content, Bucket=destination_bucket_name, Key=destination_object_key)

    except Exception as e:
        print('Error:', str(e))
        raise e

    return {
        'statusCode': 200,
        'body': 'Image resized and uploaded successfully'
    }

