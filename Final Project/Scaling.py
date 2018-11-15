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
                    scaled_img[row, col] = image[mapped_row, mapped_col]
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

                scaled_img[row, col] = resultant_intensity

        image = scaled_img

        return image

    def apply_cubic(self, image, fx, fy):
        w, h = image.shape[0],image.shape[1]

        # shrink or expand width and height based on fx, fy values
        nw = int(w * float(fx))

        nh = int(h * float(fy))
        Image1 = np.zeros([nw, nh,3], np.uint8)

        for i in range(nw):
            print(i)
            for j in range(nh):
                x = i / fx
                y = j / fy

                b = x - int(x)
                a = y - int(y)

                x0 = int(x) - 1
                y0 = int(y) - 1
                if (x0 < 0):
                    x0 = 0
                elif (x0 + 3 > w - 1):
                    x0 = w - 4
                if (y0 < 0):
                    y0 = 0
                elif (y0 + 3 > h - 1):
                    y0 = h - 4
                x1 = x0 + 1
                y1 = y0 + 1
                x2 = x0 + 2
                y2 = y0 + 2
                x3 = x0 + 3
                y3 = y0 + 3

                I0 = ((-1 * b) * (1 - b) ** 2) * image[x0, y0] + (1 - (2 * b ** 2) + (b ** 3)) * image[x1, y0] + (
                        b * (1 + b - b ** 2)) * image[
                         x2, y0] - ((b ** 2) * (1 - b) * image[x3, y0])
                I1 = ((-1 * b) * (1 - b) ** 2) * image[x0, y1] + (1 - (2 * b ** 2) + (b ** 3)) * image[x1, y1] + (
                        b * (1 + b - b ** 2)) * image[
                         x2, y1] - ((b ** 2) * (1 - b) * image[x3, y1])
                I2 = ((-1 * b) * (1 - b) ** 2) * image[x0, y2] + (1 - (2 * b ** 2) + (b ** 3)) * image[x1, y2] + (
                        b * (1 + b - b ** 2)) * image[
                         x2, y2] - ((b ** 2) * (1 - b) * image[x3, y2])
                I3 = ((-1 * b) * (1 - b) ** 2) * image[x0, y3] + (1 - (2 * b ** 2) + (b ** 3)) * image[x1, y3] + (
                        b * (1 + b - b ** 2)) * image[
                         x2, y3] - ((b ** 2) * (1 - b) * image[x3, y3])

                I = ((-1 * a) * (1 - a) ** 2) * I0 + (1 - (2 * a ** 2) + (a ** 3)) * I1 + (
                        a * (1 + a - a ** 2)) * I2 - ((a ** 2) * (1 - a) * I3)

                Image1[i, j,:] = I

        image = Image1

        return image

    def apply_lanczos4(self, image, fx, fy):
        w, h = image.shape[0],image.shape[1]

        # shrink or expand width and height based on fx, fy values
        nw = int(w * float(fx))

        nh = int(h * float(fy))
        Image1 = np.zeros([nw, nh, 3], np.uint8)

        for i in range(nw):
            print(i)
            for j in range(nh):
                x = i / fx
                y = j / fy

                x0 = int(x) - 3
                y0 = int(y) - 3
                if (x0 < 0):
                    x0 = 0
                elif (x0 + 7 > w - 1):
                    x0 = w - 8
                if (y0 < 0):
                    y0 = 0
                elif (y0 + 7 > h - 1):
                    y0 = h - 8
                x1 = x0 + 1
                y1 = y0 + 1
                x2 = x0 + 2
                y2 = y0 + 2
                x3 = x0 + 3
                y3 = y0 + 3
                x4 = x0 + 4
                y4 = y0 + 4
                x5 = x0 + 5
                y5 = y0 + 5
                x6 = x0 + 6
                y6 = y0 + 6
                x7 = x0 + 7
                y7 = y0 + 7

                a0 = self.lanczoz(x - x0)
                a1 = self.lanczoz(x - x1)
                a2 = self.lanczoz(x - x2)
                a3 = self.lanczoz(x - x3)
                a4 = self.lanczoz(x - x4)
                a5 = self.lanczoz(x - x5)
                a6 = self.lanczoz(x - x6)
                a7 = self.lanczoz(x - x7)

                b0 = self.lanczoz(y - y0)
                b1 = self.lanczoz(y - y1)
                b2 = self.lanczoz(y - y2)
                b3 = self.lanczoz(y - y3)
                b4 = self.lanczoz(y - y4)
                b5 = self.lanczoz(y - y5)
                b6 = self.lanczoz(y - y6)
                b7 = self.lanczoz(y - y7)

                I0 = a0 * image[x0, y0] + a1 * image[x1, y0] + a2 * image[x2, y0] + a3 * image[x3, y0] + a4 * image[
                    x4, y0] + a5 * image[x5, y0] + a6 * image[x6, y0] + a7 * image[x7, y0]
                I1 = a0 * image[x0, y1] + a1 * image[x1, y1] + a2 * image[x2, y1] + a3 * image[x3, y1] + a4 * image[
                    x4, y1] + a5 * image[x5, y1] + a6 * image[x6, y1] + a7 * image[x7, y1]
                I2 = a0 * image[x0, y2] + a1 * image[x1, y2] + a2 * image[x2, y2] + a3 * image[x3, y2] + a4 * image[
                    x4, y2] + a5 * image[x5, y2] + a6 * image[x6, y2] + a7 * image[x7, y2]
                I3 = a0 * image[x0, y3] + a1 * image[x1, y3] + a2 * image[x2, y3] + a3 * image[x3, y3] + a4 * image[
                    x4, y3] + a5 * image[x5, y3] + a6 * image[x6, y3] + a7 * image[x7, y3]
                I4 = a0 * image[x0, y4] + a1 * image[x1, y4] + a2 * image[x2, y4] + a3 * image[x3, y4] + a4 * image[
                    x4, y4] + a5 * image[x5, y4] + a6 * image[x6, y4] + a7 * image[x7, y4]
                I5 = a0 * image[x0, y5] + a1 * image[x1, y5] + a2 * image[x2, y5] + a3 * image[x3, y5] + a4 * image[
                    x4, y5] + a5 * image[x5, y5] + a6 * image[x6, y5] + a7 * image[x7, y5]
                I6 = a0 * image[x0, y6] + a1 * image[x1, y6] + a2 * image[x2, y6] + a3 * image[x3, y6] + a4 * image[
                    x4, y6] + a5 * image[x5, y6] + a6 * image[x6, y6] + a7 * image[x7, y6]
                I7 = a0 * image[x0, y7] + a1 * image[x1, y7] + a2 * image[x2, y7] + a3 * image[x3, y7] + a4 * image[
                    x4, y7] + a5 * image[x5, y7] + a6 * image[x6, y7] + a7 * image[x7, y7]

                Image1[i, j,:] = b0 * I0 + b1 * I1 + b2 * I2 + b3 * I3 + b4 * I4 + b5 * I5 + b6 * I6 + b7 * I7

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