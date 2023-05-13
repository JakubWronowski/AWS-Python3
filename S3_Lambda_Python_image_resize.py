import boto3
from PIL import Image
import io

def resize_images(event, context):
    
    #get bucket name and object key 
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    
    s3_client = boto3.client('s3')

    try:
       
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key) 
        image_content = response['Body'].read()

        get t
        image = Image.open(io.BytesIO(image_content))  #resizing image
        resized_image = image.resize((800, 600))  #insert desired values by you

        
        output = io.BytesIO() #Convert into bytes 
        resized_image.save(output, format='JPEG') #save in JPEG
        resized_image_content = output.getvalue()

        # saving resized image to another bucket 
        
        destination_bucket_name = 'your-destination-bucket-name'  
        destination_object_key = 'resized/' + object_key 
        s3_client.put_object(Body=resized_image_content, Bucket=destination_bucket_name, Key=destination_object_key)

    except Exception as e:
        print('Error:', str(e))
        raise e                          # outputs 

    return {
        'statusCode': 200,
        'body': 'Image resized and uploaded successfully'
    }

