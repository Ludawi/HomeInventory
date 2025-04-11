import cv2
from pyzbar.pyzbar import decode
import requests
from datetime import datetime, timezone
import json
import time

reg_url = 'http://127.0.0.1:5000/register'
unreg_url = 'http://127.0.0.1:5000/unregister'


def upload(timestamp, code_type, data):
    payload = {
        'timestamp': timestamp,
        'type': code_type,
        'data': data
    }
    headers = {'content-type': 'application/json'}
    print(json.dumps(payload))

    lol = requests.post(reg_url, data=json.dumps(payload), headers=headers)
    print(lol.text)


reader = cv2.VideoCapture(0)
reader.set(3, 1280)  # 3 = Width
reader.set(4, 720)  # 4 = Height
camera = True

registered_codes = []

while camera:
    success,  frame = reader.read()

    for code in decode(frame):
        print(code.type)
        print(code.data.decode('utf-8'))

        timestamp = datetime.now(timezone.utc).isoformat(
            timespec='milliseconds').replace('+00:00', 'Z')
        code_type = code.type
        data = code.data.decode('utf-8')
        upload(timestamp, code_type, data)
        time.sleep(4)
        # registered_codes.append(code.data.decode('utf-8'))
        # print(registered_codes)

    cv2.imshow('code-scan', frame)
    cv2.waitKey(2)
