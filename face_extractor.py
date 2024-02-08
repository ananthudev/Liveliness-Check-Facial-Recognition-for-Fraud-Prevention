import cv2
from PIL import Image
import os

def extract_face_and_save(image_path, username, expand_margin=0.7):
    # Load the pre-trained model (haarcascade_frontalface_default.xml)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Load the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None  # No faces detected

    # Use the first detected face
    x, y, w, h = faces[0]

    # Calculate expanded dimensions
    expand_w = int(w * expand_margin)
    expand_h = int(h * expand_margin)

    # Adjust the bounding box to include the expanded dimensions
    x = max(0, x - expand_w // 2)
    y = max(0, y - expand_h // 2)
    w = w + expand_w
    h = h + expand_h

    # Ensure the expanded dimensions do not exceed image boundaries
    x_end = min(img.shape[1], x + w)
    y_end = min(img.shape[0], y + h)

    # Extract the face with expanded dimensions
    face = img[y:y_end, x:x_end]
    face_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))

    # Save to PNG
    save_path = 'uploaded_images'
    os.makedirs(save_path, exist_ok=True)
    filename = f"{username}_profile.png"
    file_path = os.path.join(save_path, filename)
    face_image.save(file_path, "PNG")

    return file_path