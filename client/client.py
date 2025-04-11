import cv2
from pyzbar.pyzbar import decode
import requests
import time

# URL of the Flask server's video endpoint
url = 'http://localhost:5000/video'  # Change to your server's IP if remote

# Set up the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Custom generator for MJPEG streaming


def mjpeg_stream():
    while True:
        success, frame = cap.read()
        if not success:
            break

        for code in decode(frame):
            print(code.type)
            print(code.data.decode('utf-8'))

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # MJPEG format boundary + headers
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


try:
    headers = {'Content-Type': 'multipart/x-mixed-replace; boundary=frame'}
    response = requests.post(url, data=mjpeg_stream(), headers=headers)
    print("Stream posted. Server response:", response.status_code)
except KeyboardInterrupt:
    print("Streaming stopped.")
finally:
    cap.release()
