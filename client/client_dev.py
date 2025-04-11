
import cv2
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
    print(json.dumps(payload))
    response = requests.post(
        reg_url, data=json.dumps(payload), headers=headers)
    print(response.text)


reader = cv2.VideoCapture(0)
reader.set(3, 1280)
reader.set(4, 720)
camera = True

# Debounce tracking
last_seen = {}
cooldown_seconds = 3

while camera:
    success, frame = reader.read()

    for code in decode(frame):
        code_type = code.type
        data = code.data.decode('utf-8')

        # Bounding box
        pts = code.polygon
        if pts:
            pts = [(pt.x, pt.y) for pt in pts]
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i+1) % len(pts)], (0, 255, 0), 2)

        #  Label
        (x, y, w, h) = code.rect
        cv2.putText(frame, f'{code_type}: {data}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 16, 240), 2)

        # Debounce check
        current_time = time.time()
        if data not in last_seen or (current_time - last_seen[data]) > cooldown_seconds:
            print(code_type, data)
            timestamp = datetime.now(timezone.utc).isoformat(
                timespec='milliseconds').replace('+00:00', 'Z')
            upload(timestamp, code_type, data)
            last_seen[data] = current_time

    cv2.imshow('code-scan', frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
