import cv2

def median_blur(image, kernel_size=5):
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    blurred = cv2.medianBlur(image, kernel_size)
    return blurred

