from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Load the image
image_path = 'static/liveness/otp.jpg'
image = Image.open(image_path)

# Use Pytesseract to perform OCR on the image
text = pytesseract.image_to_string(image)

# Display the output
print("Extracted Text:")
print(text)
