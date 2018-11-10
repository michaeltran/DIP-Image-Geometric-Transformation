import cv2
from Scaling import Scaling


class Transformations:

    def scale_image(self, image, x_factor, y_factor, interpolation):
        input_image = cv2.imread(image,0)
        file_name = "ReferenceImages/scaling.jpg"
        scaling = Scaling()
        if interpolation == 'Nearest Neigbhor':
            scaled_image = scaling.apply_nearest_neighbor(input_image, x_factor, y_factor)
        elif interpolation == 'Bilinear':
            scaled_image = scaling.apply_bilinear(input_image, x_factor, y_factor)
        elif interpolation == 'Cubic':
            scaled_image = scaling.apply_cubic(input_image, x_factor, y_factor)
        elif interpolation == 'Lanczos4':
            scaled_image = scaling.apply_lanczos4(input_image, x_factor, y_factor)

        cv2.imwrite(file_name,scaled_image)
        rows, cols = scaled_image.shape
        return file_name, rows, cols

