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

def save_base64_to_image(base64_str, username, image_type):
    # Saves a Base64 string as an image file and returns the file path.
    try:
        # Ensure the base64 string is properly padded
        base64_str += '=' * (-len(base64_str) % 4)  # Pad with '=' if necessary
        img_data = base64.b64decode(base64_str, validate=True)
        img = Image.open(io.BytesIO(img_data))
    except (base64.binascii.Error, IOError) as e:
        print(f"Error decoding base64 or opening image: {e}")
        return None  # or handle the error as needed

    save_path = 'static/uploaded_images'
    os.makedirs(save_path, exist_ok=True)

    # Construct file path
    filename = f"{username}_{image_type}.png"
    file_path = os.path.join(save_path, filename)
    
    # Save the image
    img.save(file_path, "PNG")
    return file_path
