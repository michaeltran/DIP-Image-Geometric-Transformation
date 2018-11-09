import cv2


class Transformations:

    def scale(self, image, x_factor, y_factor, interpolation, show_full_image):
        input_image = cv2.imread(image,0)
        print("input image shape ", input_image.shape,interpolation)
        file_name = "ReferenceImages/scaling.jpg"
        scaled_image = cv2.resize(input_image,None,fx=x_factor, fy=y_factor, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(file_name,scaled_image)
        rows,cols = scaled_image.shape
        return file_name, rows, cols
