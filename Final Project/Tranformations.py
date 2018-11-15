import cv2
from Scaling import Scaling
from Translation import Translation
from Rotation import Rotation


class Transformations:

    def scale_image(self, image_name, x_factor, y_factor, interpolation):

        input_image = cv2.imread(image_name,1)
        print(input_image.shape)
        file_name = "ReferenceImages/scaling.jpg"

        scaling = Scaling()

        if interpolation == 'Nearest Neigbhor':
            scaled_image = scaling.apply_nearest_neighbor(input_image, x_factor, y_factor)
        elif interpolation == 'Bilinear':
            scaled_image = scaling.apply_bilinear(input_image, x_factor, y_factor)
        elif interpolation == 'Cubic':
            scaled_image = scaling.apply_cubic(input_image, y_factor, x_factor)
        elif interpolation == 'Lanczos4':
            scaled_image = scaling.apply_lanczos4(input_image, y_factor, x_factor)

        cv2.imwrite(file_name,scaled_image)
        rows, cols = scaled_image.shape[0], scaled_image.shape[1]


        return file_name, rows, cols

    def translate_image(self, image_name, x_units, y_units):

        input_image = cv2.imread(image_name, 1)
        
        file_name = "ReferenceImages/translation.jpg"

        translation = Translation()
        translated_image = translation.translate(input_image, y_units, x_units)

        cv2.imwrite(file_name, translated_image)
        rows, cols = translated_image.shape[0],translated_image.shape[1]

        return file_name, rows, cols

    def rotate_image(self, image_name, degrees, direction):

        input_image = cv2.imread(image_name, 1)

        file_name = "ReferenceImages/rotation.jpg"

        rotation = Rotation()

        if direction == "Clockwise":
            direction = "clockwise"
        else:
            direction = "counterclockwise"

        rotated_image = rotation.rotate(input_image, degrees, direction)

        cv2.imwrite(file_name, rotated_image)
        rows, cols = rotated_image.shape[0], rotated_image.shape[1]

        return file_name, rows, cols
