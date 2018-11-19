import numpy as np
import math
from Interpolation import interpolation
from Interpolate import  Interpolate

class Scaling:

    def apply_nearest_neighbor(self, image, fx, fy):
        img_height = image.shape[0]
        img_width = image.shape[1]

        new_height = int(img_height * fy)
        new_width = int(img_width * fx)

        scaled_img = np.zeros((new_height,new_width,3), dtype=np.uint8)

        interpolate_ref = Interpolate()

        for row in range(new_height):
            for col in range(new_width):
                mapped_row = int(row / fy)
                mapped_col = int(col / fx)


                try:
                    scaled_img[row, col] = interpolate_ref.get_value(image, mapped_row, mapped_col, 'Nearest Neigbhor')
                except Exception as exp:
                    #print("Exception",exp, mapped_row, mapped_col)
                    pass

        image = scaled_img

        return image

    def apply_bilinear(self, image, fx, fy):
        img_height = image.shape[0]
        img_width = image.shape[1]

        new_height = int(img_height * fy)
        new_width = int(img_width * fx)

        scaled_img = np.zeros((new_height, new_width,3), dtype=np.uint8)

        interpolation_ref = interpolation()
        interpolate_ref = Interpolate()

        for row in range(new_height):
            for col in range(new_width):
                unknown_y = (row / fy)
                unknown_x = (col / fx)

                scaled_img[row, col] = interpolate_ref.get_value(image, unknown_y, unknown_x, 'Bilinear')

        image = scaled_img

        return image

    def apply_cubic(self, image, fx, fy):
        w, h = image.shape[0],image.shape[1]

        # shrink or expand width and height based on fx, fy values
        nw = int(w * float(fx))

        nh = int(h * float(fy))
        Image1 = np.zeros([nw, nh,3], np.uint8)

        interpolate_ref = Interpolate()

        for i in range(nw):
            print(i)
            for j in range(nh):
                x = i / fx
                y = j / fy

                Image1[i, j,:] = interpolate_ref.get_value(image, x, y, 'Cubic')

        image = Image1

        return image

    def apply_lanczos4(self, image, fx, fy):
        w, h = image.shape[0],image.shape[1]

        # shrink or expand width and height based on fx, fy values
        nw = int(w * float(fx))

        nh = int(h * float(fy))
        Image1 = np.zeros([nw, nh, 3], np.uint8)

        interpolate_ref = Interpolate()

        for i in range(nw):
            print(i)
            for j in range(nh):
                x = i / fx
                y = j / fy

                Image1[i, j,:] = interpolate_ref.get_value(image, x, y, 'Lanczos4')
                
        image = Image1

        return image

    def lanczoz(self, x):

        if x == 0:
            return 1
        elif (np.absolute(x)) <= 4:

            theta = math.pi * x
            return ((math.sin(theta) / theta) * (math.sin(theta / 4) / (theta / 4)))
        else:
            return 0

    def checkBoundaries_bilinear(self, x, y, width, height):

        if x > width - 1:
            # print("in check boundaries")
            x = width - 2
        if y > height - 1:
            # print("in check boundaries")
            y = height - 2

        return x, y