import base64

def copy_button_fmt(text):
    encoded = base64.b64encode(text.encode()).decode()
    return {"text": "Copy me!", "callback_data": f"clip:{encoded}"}

def decode_clip_payload(payload):
    try:
        prefix, b64 = payload.split(":", 1)
        if prefix != "clip":
            raise ValueError("Invalid payload prefix")
        return base64.b64decode(b64).decode()
    except Exception as e:
        # Could log or handle error as needed
        return None
