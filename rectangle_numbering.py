import cv2 as cv

image = cv.imread("fft.jpg")
gray = cv.cvtColor(image,cv.COLOR_BGR2BGRA)
edge = cv.Canny(gray,50,150)
contours,_= cv.findContours(edge,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(image, contours, -1, (0, 255, 0), 3)
clipped_images = []
child_contours = []

#  clip the rectangle
for i, contour in enumerate(contours):
    x, y, w, h = cv.boundingRect(contour)
    # Ensure the coordinates are within the image bounds
    x = max(0, x)
    y = max(0, y)
    w = min(w, image.shape[1] - x)
    h = min(h, image.shape[0] - y)
    # Clip the rectangle
    clipped_rectangle = image[y:y + h, x:x + w]
    # Save each clipped rectangle as a separate image
    seprate = cv.imwrite(f"clip/clipped_image_{i}.jpg", clipped_rectangle)
    # Read the saved image back and append to the list
    saved_image = cv.imread(f"clip/clipped_image_{i}.jpg")
    clipped_images.append(saved_image)
    

    
for i, clipp in enumerate(clipped_images):
    gray_clip = cv.cvtColor(clipp, cv.COLOR_BGR2BGRA)
    edge_clip = cv.Canny(gray_clip,50, 200)
    # Find contours with hierarchy
    contours2, hierarchy = cv.findContours(edge_clip, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    total_length = 0
    tleng=[]
    # Draw only the parent
    for j, hier in enumerate(hierarchy[0]):
        if hier[3] != -1:
            # Draw the parent contours
            # cv.drawContours(gray_clip, contours2, j, (0, 0, 255), 3)
            # Iterate through sub-child contours (children of the current child)
            for k, sub_child_hier in enumerate(hierarchy[0]):
                # Check if the contour is a child of the current parent
                if sub_child_hier[3] == j:
                    cv.drawContours(gray_clip, contours2, k, (0, 255, 0), 2)
                    length = cv.arcLength(contours2[k], True)
                    total_length += length
             
                    # print(f"Length of sub-child contour {k} in parent Contour {i}: {length}")
                
    # print(f"Total length of sub-child contours in image {j}: {total_length}")
    tleng.append(total_length)
    print(f"LENGTH OF LINE IN PARENT IMAGE {j}:", tleng)
    
    
    # cv.namedWindow("SClipped image",cv.WINDOW_NORMAL)
    # cv.imshow("SClipped image",gray_clip)
    # cv.waitKey(0)
    cv.destroyAllWindows()
    