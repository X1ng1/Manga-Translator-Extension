import cv2
import numpy as np
from components.detect_bubble import detect_bubbles

def clear_bubble(image, bbox):
    x1, y1, x2, y2 = bbox

    roi = image[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return image

    largest = max(contours, key=cv2.contourArea)

    mask = np.zeros(gray.shape, dtype=np.uint8)
    cv2.drawContours(mask, [largest], -1, 255, cv2.FILLED)

    roi[mask == 255] = (255, 255, 255)

    return image

def test_clear_all_bubbles(image_path, output_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not load image: {image_path}")

    boxes = detect_bubbles(image_path)

    for box in boxes:
        img = clear_bubble(img, box)

    cv2.imwrite(output_path, img)

    return img

if __name__ == "__main__":
    test_clear_all_bubbles("./test-images/image02.jpg", "./test-images/clear_output.jpg")

