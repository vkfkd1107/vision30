# import easyocr

# reader = easyocr.Reader(['ko'])

# result = reader.readtext('10443599_50093904922407222.jpg', detail=0)

# print(result)

import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2

cap = cv2.VideoCapture('inputs/test1.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    b,g,r,a = 0,0,0,0
    fontpath = "fonts/gulim.ttc"
    font = ImageFont.truetype(fontpath, 20)
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.rectangle(((0,50), (300,100)), fill='white')
    draw.text((60, 70),  "테스트123456789", font=font, fill=(b, g, r, a))
    # cv2.rectangle(gray, (0,0), (100,100), (255, 255, 255), cv2.FILLED)
    image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_BGR2RGB)
    
    # Display the resulting frame
    cv2.imshow('frame', image)
    if cv2.waitKey(1) == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


# img = np.zeros((200,400,3),np.uint8)
# b,g,r,a = 255,255,255,0
# fontpath = "fonts/gulim.ttc"
# font = ImageFont.truetype(fontpath, 20)
# img_pil = Image.fromarray(img)
# draw = ImageDraw.Draw(img_pil)
# draw.text((60, 70),  "김형준ABC123#GISDeveloper", font=font, fill=(b,g,r,a))
# img = np.array(img_pil)

# cv2.putText(img,  "한글by Dip2K", (250,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (b,g,r), 1, cv2.LINE_AA)
# cv2.imshow("res", img)
# cv2.waitKey()
# cv2.destroyAllWindows()
