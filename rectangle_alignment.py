import cv2
import numpy as np

# Read the image
original_image = cv2.imread("fft.jpg", cv2.IMREAD_COLOR)
image = original_image[10:-10, 10:-10]
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)[..., 0]
ret, thresh = cv2.threshold(imgray, 20, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
mask = 255 - thresh
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


# Create a copy of the original image to draw rectangles on
result_image = original_image.copy()

# Draw rectangles for all detected contours
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:  # You can adjust the minimum area threshold as needed
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(result_image, [box], 0, (0, 255, 0), 2)

        scale = 1  # cropping margin, 1 == no margin
        W = rect[1][0]
        H = rect[1][1]
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        angle = rect[2]
        # print('Angle:',angle)
        rotated = False
        if angle < -45 :
            angle += 90
            rotated = True
        elif angle >= 45:
          angle -= 90
          rotated = True
        
        center = (int((x1+x2)/2), int((y1+y2)/2))
        size = (int(scale*(x2-x1)), int(scale*(y2-y1)))
        M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)
        cropped = cv2.getRectSubPix(image, size, center)
        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = W if not rotated else H
        croppedH = H if not rotated else W
        result_image = cv2.getRectSubPix(
            cropped, (int(croppedW*scale), int(croppedH*scale)), (size[0]/2, size[1]/2))

        # Show the result image with the rectangle
        cv2.imshow("Straight Align", result_image)
        cv2.waitKey(0)
        
cv2.destroyAllWindows()
