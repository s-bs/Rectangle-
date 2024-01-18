import cv2 as cv

def process_length_and_display_contours(image_path, num_contours_to_display=4):
    image = cv.imread(image_path)

    if image is None:
        print(f"Error: Image not loaded. Check the file path: {image_path}")
        return

    gray_image = cv.cvtColor(image, cv.COLOR_BGR2BGRA)

    edge = cv.Canny(gray_image, 50, 150)

    contours, hierarchy = cv.findContours(edge, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    contour_image = image.copy()

    tleng = [(cv.arcLength(contour, True), i) for i, contour in enumerate(contours) if hierarchy[0][i][3] != -1]
    tleng.sort()

    line_numbers = {length_index[1]: i + 1 for i, length_index in enumerate(tleng)}

    for len, index in tleng[:num_contours_to_display]:
        contour = contours[index]
        cv.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
        number = line_numbers[index]
        cv.putText(contour_image, str(number), tuple(contour[0][0]), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv.namedWindow("Contour Image", cv.WINDOW_NORMAL)
    cv.imshow("Contour Image", contour_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

image_path = 'fft.png'

process_length_and_display_contours(image_path, num_contours_to_display=4)