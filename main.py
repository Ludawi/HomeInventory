import cv2
from pyzbar.pyzbar import decode


reader = cv2.VideoCapture(0)
reader.set(3, 1280)  # 3 = Width
reader.set(4, 720)  # 4 = Height
camera = True

registered_codes = []

while camera:
    success,  frame = reader.read()

    for code in decode(frame):
        # print(code.type)
        # print(code.data.decode('utf-8'))
        registered_codes.append(code.data.decode('utf-8'))
        print(registered_codes)

    cv2.imshow('code-scan', frame)
    cv2.waitKey(2)
