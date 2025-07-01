import base64
import urllib.parse

def copy_button_fmt(text):
    encoded = base64.b64encode(text.encode()).decode()
    return {"text": "Copy me!", "callback_data": f"clip:{encoded}"}

def decode_clip_payload(payload):
    _, b64 = payload.split(":", 1)
    return base64.b64decode(b64).decode()