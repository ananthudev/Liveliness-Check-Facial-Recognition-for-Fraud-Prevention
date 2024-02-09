import cv2
from PIL import Image
import os
import io
import base64

def extract_face_and_return_filepath(image_path, expand_margin=0.7):
    # Load the pre-trained model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale for the face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None  # Return None if no faces are detected

    # Extract the first detected face
    x, y, w, h = faces[0]
    expand_w = int(w * expand_margin)
    expand_h = int(h * expand_margin)
    x = max(0, x - expand_w // 2)
    y = max(0, y - expand_h // 2)
    w += expand_w
    h += expand_h

    x_end = min(img.shape[1], x + w)
    y_end = min(img.shape[0], y + h)

    # Crop the expanded face region from the image
    face = img[y:y_end, x:x_end]

    # Convert the face region to a PIL Image
    face_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
    
    # Convert the PIL Image to a base64 string
    buffered = io.BytesIO()
    face_image.save(buffered, format="PNG")
    base64_face = base64.b64encode(buffered.getvalue()).decode()

    return base64_face

# Optionally, you can keep the function to save a base64 string as an image file
def save_base64_to_image(base64_str, username, image_type='profile'):
    img_data = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_data))
    save_path = 'uploaded_images'
    os.makedirs(save_path, exist_ok=True)
    filename = f"{username}_{image_type}.png"
    file_path = os.path.join(save_path, filename)
    img.save(file_path, "PNG")
    return file_path
