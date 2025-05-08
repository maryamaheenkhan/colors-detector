import cv2
from PIL import Image
from util import get_limits

blue = [255, 0, 0]  
yellow = [0, 255, 255]  
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the camera.")
    exit()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit_yellow, upperLimit_yellow = get_limits(color=yellow)
    mask_yellow = cv2.inRange(hsvImage, lowerLimit_yellow, upperLimit_yellow)

    lowerLimit_blue, upperLimit_blue = get_limits(color=blue)
    mask_blue = cv2.inRange(hsvImage, lowerLimit_blue, upperLimit_blue)

    mask_yellow_cleaned = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)
    mask_blue_cleaned = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)

    combined_mask = cv2.bitwise_or(mask_yellow_cleaned, mask_blue_cleaned)

    cv2.imshow('Yellow Mask', mask_yellow_cleaned)
    cv2.imshow('Blue Mask', mask_blue_cleaned)
    cv2.imshow('Combined Mask', combined_mask)

    for mask, color_name, box_color in [(mask_yellow_cleaned, 'Yellow', (0, 255, 0)), (mask_blue_cleaned, 'Blue', (255, 0, 0))]:
        mask_pil = Image.fromarray(mask)
        bbox = mask_pil.getbbox()
        if bbox:
            x1, y1, x2, y2 = bbox
            padding = 5
            x1, y1 = max(0, x1 + padding), max(0, y1 + padding)
            x2, y2 = max(0, x2 - padding), max(0, y2 - padding)
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            print(f"{color_name} bounding box:", bbox)
        else:
            print(f"No {color_name} bounding box detected.")

    cv2.imshow('frame', frame)

    if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()