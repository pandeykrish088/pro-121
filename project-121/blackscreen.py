import cv2
import time
import numpy as np

image = cv2.VideoWriter_fourcc(*'XVID')
file = cv2.VideoWriter('output.avi', image, 20.0, (640, 480))

cap = cv2.VideoCapture(0)

time.sleep(5)
bg = 0


for i in range(100):
    tip, bg = cap.read()

bg = np.flip(bg, axis = 1)


while (cap.isOpened()):
    tip, img = cap.read()

    if not tip:
        break
    

    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


    low_black = np.array([30, 30, 0])
    up_black = np.array([104, 153, 70])
    mask_1 = cv2.inRange(hsv, low_black, up_black)


    low_black = np.array([60, 60, 0])
    up_black = np.array([120, 150, 70])
    mask_2 = cv2.inRange(hsv, low_black, up_black)

    mask_1 = mask_1 + mask_2


    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)


    res_1 = cv2.bitwise_and(img, img, mask = mask_2)
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)


    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    file.write(final_output)

    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()