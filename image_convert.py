import base64
from PIL import Image
import io
import os

def convert_image_to_base64(image):

    # Converts a Image to a Base64 string.
   
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def save_base64_to_image(base64_str, username, image_type):
  
    # Saves a Base64 string as an image file and returns the file path.
   
    img_data = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_data))
  
    save_path = 'uploaded_images'
    os.makedirs(save_path, exist_ok=True)

    #  file path
    filename = f"{username}_{image_type}.png"
    file_path = os.path.join(save_path, filename)
    
    # Save the image
    img.save(file_path, "PNG")
    return file_path


