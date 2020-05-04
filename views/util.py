import base64
from PIL import Image
from io import BytesIO


def get_button_img() -> str:
    buf = BytesIO()
    img = Image.open(open('img/button.png', 'rb'))
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue())