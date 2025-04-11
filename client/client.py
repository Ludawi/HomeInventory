import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
from datetime import datetime, timezone
import json
import time

reg_url = 'http://127.0.0.1:5000/register'


def upload(timestamp, code_type, data):
    payload = {
        'timestamp': timestamp,
        'type': code_type,
        'data': data
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(
        reg_url, data=json.dumps(payload), headers=headers)
    print(response.text)


def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    threshold = cv2.adaptiveThreshold(
        sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    threshold = frame
    return threshold


reader = cv2.VideoCapture(0)
reader.set(3, 1280)
reader.set(4, 720)
camera = True

# Debounce
last_seen = {}
cooldown_seconds = 3

while camera:
    success, frame = reader.read()
    if not success:
        break

    processed = process_frame(frame)

    detected_codes = set()

    for code in decode(processed):
        code_type = code.type
        data = code.data.decode('utf-8')

        # Border
        pts = code.polygon
        if pts:
            pts = [(pt.x, pt.y) for pt in pts]
            for i in range(len(pts)):
                cv2.line(processed, pts[i], pts[(i+1) %
                         len(pts)], (0, 255, 0), 2)

        #  Label
        (x, y, w, h) = code.rect
        cv2.putText(processed, f'{code_type}: {data}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 16, 240), 2)

        detected_codes.add(data)

    # Debounce
    current_time = time.time()
    for data in detected_codes:
        if data not in last_seen or (current_time - last_seen[data]) > cooldown_seconds:
            timestamp = datetime.now(timezone.utc).isoformat(
                timespec='milliseconds').replace('+00:00', 'Z')
            upload(timestamp, 'QR', data)
            last_seen[data] = current_time

    cv2.imshow('code-scan', processed)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
