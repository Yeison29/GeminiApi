import base64
from io import BytesIO
from PIL import Image


def upload_image(img_base64: str):
    image_data = base64.b64decode(img_base64)
    image_io = BytesIO(image_data)
    return Image.open(image_io)
