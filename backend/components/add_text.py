from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import cv2

def add_text(image, translation, font_path, bbox):
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)

    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1

    line_height = 16
    font_size = 14
    wrapping_ratio = 0.075

    wrapped_text = textwrap.fill(translation, width= max(1, int(w * wrapping_ratio)),
                                 break_long_words=True)
    
    font = ImageFont.truetype(font_path, size=font_size)

    lines = wrapped_text.split('\n')
    total_text_height = (len(lines)) * line_height
    
    while total_text_height > h and font_size > 8:
        line_height -= 2
        font_size -= 2
        wrapping_ratio += 0.025

        wrapped_text = textwrap.fill(translation, width= max(1, int(w * wrapping_ratio)),
                                     break_long_words=True)
        
        font = ImageFont.truetype(font_path, size=font_size)

        lines = wrapped_text.split('\n')
        total_text_height = (len(lines)) * line_height

    text_y = y1 + (h - total_text_height) // 2

    for line in lines:
        text_length = draw.textlength(line, font=font)

        text_x = x1 + (w - text_length) // 2

        draw.text((text_x, text_y), line, font=font, fill=(0,0,0))

        text_y += line_height

    image[:,:,:] = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return image