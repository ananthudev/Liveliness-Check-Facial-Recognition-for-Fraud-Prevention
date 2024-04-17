from google.cloud import vision
from google.cloud.vision import types

# Authenticate with Google Cloud
client = vision.ImageAnnotatorClient.from_service_account_json('static/key/liveliness-420109-bdcd84f0f93c.json')

# Load the image
with open('static/liveness/otp.jpg', 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Perform handwriting detection
response = client.document_text_detection(image=image)

# Extract text
texts = response.full_text_annotation.text
print(texts)
