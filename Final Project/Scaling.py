import numpy as np
import math
from Interpolation import interpolation


class Scaling:

    def apply_nearest_neighbor(self, image, fx, fy):
        img_height = image.shape[0]
        img_width = image.shape[1]

        new_height = int(img_height * fy)
        new_width = int(img_width * fx)

        scaled_img = np.zeros((new_height,new_width,3), dtype=np.uint8)

        for row in range(new_height):
            for col in range(new_width):
                mapped_row = int(row / fy)
                mapped_col = int(col / fx)
                if mapped_row >= img_height:
                    mapped_row = img_height - 1
                if mapped_col >= img_width:
                    mapped_col = img_width - 1

                try:
                    scaled_img[row, col,:] = image[mapped_row, mapped_col,:]
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

        for row in range(new_height):
            for col in range(new_width):
                unknown_y = (row / fy)
                unknown_x = (col / fx)
                pt1_x = math.floor(unknown_x)
                pt1_y = math.floor(unknown_y)
                pt2_x = pt1_x + 1
                pt2_y = pt1_y + 1

                pt2_x, pt2_y = self.checkBoundaries_bilinear(pt2_x, pt2_y, img_width, img_height)

                pt1 = ((pt1_x, pt1_y), image[pt1_y, pt1_x])
                pt2 = ((pt2_x, pt1_y), image[pt1_y, pt2_x])
                pt3 = ((pt1_x, pt2_y), image[pt2_y, pt1_x])
                pt4 = ((pt2_x, pt2_y), image[pt2_y, pt2_x])
                unknown = (unknown_x, unknown_y)

                resultant_intensity = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

                scaled_img[row, col,:] = resultant_intensity

        image = scaled_img

        return image

    def apply_cubic(self, image, fx, fy):
        return image

    def apply_lanczos4(self, image, fx, fy):
        return image

    def checkBoundaries_bilinear(self, x, y, width, height):

        if x > width - 1:
            # print("in check boundaries")
            x = width - 2
        if y > height - 1:
            # print("in check boundaries")
            y = height - 2

        return x, y