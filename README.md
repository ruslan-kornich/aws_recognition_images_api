### API for recognition of images. 
API have 2 endpoints:
POST /blobs - should accept callback_url for receiving callback when recognition will be ended, and return upload_url for uploading pictures
GET /blobs/{blob_id} - Should return information about recognition results for specified blob



### Deploy
- Clone repository
```bash
git clone https://github.com/ruslan-kornich/aws_recognition_images_api.git
```
- Go to the folder where it is serverless.yml file
```bash
cd recognition-images-api
```
- Run
```bash
serverless deploy
```
## API Endpoints: 

```
- POST /blobs
```
When use POST endpoint, the request body must contain a callback url where you expect the result of the service
Examples:
```bash
{"callback_url": "https://webhook.site/example"}
```
Response API for POST request
```bash
{
  "blob_id": "fae955d4-0247-4152-ab17-9a851a745cea",
  "callback_url": "https://webhook.site/example",
  "upload_url": "https://recognition-images-api-blobs-bucket.s3.amazonaws.com/fae955d4-0247-4152-ab17-9a851a745cea..."
}



```
>```"blob_id"```: id records in the DynamoDB database where the result of the work will be recorded images recognition  
```"callback_url"```: url for callback when the result of image recognition is ready    
```"upload_url"```: the link where the client uploaded image for recognition. Put request type.  

```
- PUT <upload_url>
```
You can send a picture for recognition


```
- GET /blobs/{blobs_id}
```
Response API for GET requests
```bash
{
    "blob_id": "fae955d4-0247-4152-ab17-9a851a745cea",
    "labels": [
        {
            "label": "Animal",
            "confidence": 99.9940185546875,
            "parents": []
        }, ...
        ]
}
```
> ```"blob_id"```: id of the requested entry in the database  
>```"labels"```: image recognition results




