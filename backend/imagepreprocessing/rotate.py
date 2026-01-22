import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_rotation(img):
    try:
        osd = pytesseract.image_to_osd(img)

        for line in osd.split('\n'):
            if 'Rotate' in line:
                return int(line.split(':')[-1].strip())

        return 0  # fallback if Rotate not found

    except Exception as e:
        print("Orientation detection failed:", e)
        return 0


def rotate_to_upright(img, angle):
    
    if angle == 0 or angle == 180   :
        return img
    elif angle == 90:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 270:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
