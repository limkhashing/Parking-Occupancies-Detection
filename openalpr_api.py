import requests
import base64
import json

# Needed Malaysia car plate localization to work

IMAGE_PATH = 'test_plate\\pic_004.jpg'
SECRET_KEY = 'sk_cf01e969c42c97bde2ea8dbb'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

print(json.dumps(r.json(), indent=2))