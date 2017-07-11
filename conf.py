import os

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "image")
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
QRCode_PATH = os.path.join(IMAGE_DIR, "v.png")
