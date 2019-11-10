"""
    https://stackoverflow.com/questions/45540069/access-ip-camera-with-opencv
"""
import urllib.request
import cv2
import numpy as np

url = "http://192.168.0.104:8080"

with urllib.request.urlopen(url) as stream:
    bytes = bytearray()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cv2.destroyAllWindows()
