import base64
from PIL import Image
import io
import os

def convert_image_to_base64(image):
    # Converts a PIL Image to a Base64 string.
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def save_base64_to_image(base64_str, username, image_type, directory="uploaded_images"):
    img_data = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_data))

    save_path = os.path.join('static', directory)
    os.makedirs(save_path, exist_ok=True)

    filename = f"{username}_{image_type}.png"
    file_path = os.path.join(save_path, filename)
    
    img.save(file_path)
    return file_path