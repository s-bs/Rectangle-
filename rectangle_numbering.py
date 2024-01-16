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
    
tleng=[]

for i, clipp in enumerate(clipped_images):
    gray_clip = cv.cvtColor(clipp, cv.COLOR_BGR2BGRA)
    edge_clip = cv.Canny(gray_clip,50, 200)
    # Find contours with hierarchy
    contours2, hierarchy = cv.findContours(edge_clip, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    total_length = 0
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
    tleng.append({'length':total_length,
                  'parent':j
                  })
    # sort_length = sorted(tleng)
    # print(f"LENGTH OF LINE IN PARENT IMAGE {j}:", tleng)
# print('data:',tleng)
sorted_data = sorted(tleng, key=lambda x: x['length'])
# print("sorted_data:",sorted_data)

for i, clipp in enumerate(clipped_images):
    gray_clipp = cv.cvtColor(clipp, cv.COLOR_BGR2BGRA)
    edge_clipp = cv.Canny(gray_clipp,50, 200)
    # Find contours with hierarchy
    contours3, hierarchy1 = cv.findContours(edge_clipp, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    total_length = 0
    # Draw only the parent
    for j, hier in enumerate(hierarchy1[0]):
        if hier[3] != -1:
            # Draw the parent contours
            # cv.drawContours(gray_clip, contours2, j, (0, 0, 255), 3)
            # Iterate through sub-child contours (children of the current child)
            for k, sub_child_hier in enumerate(hierarchy1[0]):
                # Check if the contour is a child of the current parent
                if sub_child_hier[3] == j:
                    # cv.drawContours(gray_clipp, contours3, k, (0, 255, 0), 2)
                    length = cv.arcLength(contours3[k], True)
                    total_length += length
    
    # print('Length',total_length)
    # print('sort',sorted_data)
    position = next((i for i, data in enumerate(sorted_data) if data['length'] == total_length), None)
    cv.putText(gray_clipp,str(position + 1), (250,150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
    # if position is not None:
    #     print(f"The position of total_length {total_length} in the sorted data is {position + 1}.")
    # else:
    #     print(f"Total_length {total_length} not found in the sorted data.")
    
    # cv.drawContours(image, contours3, parent_index, (0, 255, 0), 2)
    cv.namedWindow("Clipped image Numbering",cv.WINDOW_NORMAL)
    cv.resizeWindow("Clipped image Numbering", 400, 300)
    cv.imshow("Clipped image Numbering",gray_clipp)
    cv.waitKey(0)
    cv.destroyAllWindows()
    

    