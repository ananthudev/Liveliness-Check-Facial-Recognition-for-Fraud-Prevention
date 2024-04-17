
import requests

url = 'https://app.nanonets.com/api/v2/OCR/Model/137b2087-8d17-4391-ab22-6474607c2bb7/LabelFile/?async=false'

data = {'file': open('static/liveness/otp.jpg', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('cc0673f8-f896-11ee-8bd8-26d1380d02d0', ''), files=data)

print(response.text)
        