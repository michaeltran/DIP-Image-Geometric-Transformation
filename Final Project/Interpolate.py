import math
from Interpolation import interpolation
import numpy as np


class Interpolate:
    def get_value(self, img, pt1, pt2, technique):
        interpolated_value = 0
        if technique == 'Nearest Neigbhor':
            interpolated_value = self.nearest_neighbor(img, pt1, pt2)
        elif technique == 'Bilinear':
            interpolated_value = self.bilinear(img, pt1, pt2)
        elif technique == 'Cubic':
            interpolated_value = self.cubic(img, pt1, pt2)
        elif technique == 'Lanczos4':
            interpolated_value = self.lanczos4(img, pt1, pt2)

        return interpolated_value


    def nearest_neighbor(self, img, h, w):

        height, width, ch = img.shape

        new_pt1 = int(h)
        new_pt2 = int(w)

        if new_pt1 >= height:
            new_pt1 = height - 1

        if new_pt2 >= width:
            new_pt2 = width - 1

        value = img[new_pt1][new_pt2]

        return value


    def bilinear(self, img, h, w):
        height, width, ch = img.shape

        pt1_x = math.floor(w)
        pt1_y = math.floor(h)
        pt2_x = pt1_x + 1
        pt2_y = pt1_y + 1

        if pt2_x > width - 1:
            pt2_x = width - 2
        if pt2_y > height - 1:
            pt2_y = height - 2

        pt1 = ((pt1_x, pt1_y), img[pt1_y, pt1_x])
        pt2 = ((pt2_x, pt1_y), img[pt1_y, pt2_x])
        pt3 = ((pt1_x, pt2_y), img[pt2_y, pt1_x])
        pt4 = ((pt2_x, pt2_y), img[pt2_y, pt2_x])
        unknown = (w, h)

        interpolation_ref = interpolation()
        value = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

        return value



    def cubic(self, img, h, w):

        height, width, ch = img.shape

        x = h
        y = w

        b = x - int(x)
        a = y - int(y)

        x0 = int(x) - 1
        y0 = int(y) - 1
        if x0 < 0:
            x0 = 0
        elif x0 + 3 > height - 1:
            x0 = height - 4
        if y0 < 0:
            y0 = 0
        elif y0 + 3 > width - 1:
            y0 = width - 4

        x1 = x0 + 1
        y1 = y0 + 1
        x2 = x0 + 2
        y2 = y0 + 2
        x3 = x0 + 3
        y3 = y0 + 3

        I0 = ((-1 * b) * (1 - b) ** 2) * img[x0, y0] + (1 - (2 * b ** 2) + (b ** 3)) * img[x1, y0] + (
                b * (1 + b - b ** 2)) * img[
                 x2, y0] - ((b ** 2) * (1 - b) * img[x3, y0])
        I1 = ((-1 * b) * (1 - b) ** 2) * img[x0, y1] + (1 - (2 * b ** 2) + (b ** 3)) * img[x1, y1] + (
                b * (1 + b - b ** 2)) * img[
                 x2, y1] - ((b ** 2) * (1 - b) * img[x3, y1])
        I2 = ((-1 * b) * (1 - b) ** 2) * img[x0, y2] + (1 - (2 * b ** 2) + (b ** 3)) * img[x1, y2] + (
                b * (1 + b - b ** 2)) * img[
                 x2, y2] - ((b ** 2) * (1 - b) * img[x3, y2])
        I3 = ((-1 * b) * (1 - b) ** 2) * img[x0, y3] + (1 - (2 * b ** 2) + (b ** 3)) * img[x1, y3] + (
                b * (1 + b - b ** 2)) * img[
                 x2, y3] - ((b ** 2) * (1 - b) * img[x3, y3])

        value = ((-1 * a) * (1 - a) ** 2) * I0 + (1 - (2 * a ** 2) + (a ** 3)) * I1 + (
                a * (1 + a - a ** 2)) * I2 - ((a ** 2) * (1 - a) * I3)

        return value

    def lanczos4(self, img, h, w):
        height, width, ch = img.shape

        x = h
        y = w

        x0 = int(x) - 3
        y0 = int(y) - 3
        if x0 < 0:
            x0 = 0
        elif x0 + 7 > height - 1:
            x0 = height - 8
        if y0 < 0:
            y0 = 0
        elif y0 + 7 > width - 1:
            y0 = width - 8

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

        I0 = a0 * img[x0, y0] + a1 * img[x1, y0] + a2 * img[x2, y0] + a3 * img[x3, y0] + a4 * img[x4, y0] + a5 * img[x5, y0] + a6 * img[x6, y0] + a7 * img[x7, y0]
        I1 = a0 * img[x0, y1] + a1 * img[x1, y1] + a2 * img[x2, y1] + a3 * img[x3, y1] + a4 * img[x4, y1] + a5 * img[x5, y1] + a6 * img[x6, y1] + a7 * img[x7, y1]
        I2 = a0 * img[x0, y2] + a1 * img[x1, y2] + a2 * img[x2, y2] + a3 * img[x3, y2] + a4 * img[x4, y2] + a5 * img[x5, y2] + a6 * img[x6, y2] + a7 * img[x7, y2]
        I3 = a0 * img[x0, y3] + a1 * img[x1, y3] + a2 * img[x2, y3] + a3 * img[x3, y3] + a4 * img[x4, y3] + a5 * img[x5, y3] + a6 * img[x6, y3] + a7 * img[x7, y3]
        I4 = a0 * img[x0, y4] + a1 * img[x1, y4] + a2 * img[x2, y4] + a3 * img[x3, y4] + a4 * img[x4, y4] + a5 * img[x5, y4] + a6 * img[x6, y4] + a7 * img[x7, y4]
        I5 = a0 * img[x0, y5] + a1 * img[x1, y5] + a2 * img[x2, y5] + a3 * img[x3, y5] + a4 * img[x4, y5] + a5 * img[x5, y5] + a6 * img[x6, y5] + a7 * img[x7, y5]
        I6 = a0 * img[x0, y6] + a1 * img[x1, y6] + a2 * img[x2, y6] + a3 * img[x3, y6] + a4 * img[x4, y6] + a5 * img[x5, y6] + a6 * img[x6, y6] + a7 * img[x7, y6]
        I7 = a0 * img[x0, y7] + a1 * img[x1, y7] + a2 * img[x2, y7] + a3 * img[x3, y7] + a4 * img[x4, y7] + a5 * img[x5, y7] + a6 * img[x6, y7] + a7 * img[x7, y7]

        value = b0 * I0 + b1 * I1 + b2 * I2 + b3 * I3 + b4 * I4 + b5 * I5 + b6 * I6 + b7 * I7

        return value

    def lanczoz(self, x):

        if x == 0:
            return 1
        elif (np.absolute(x)) <= 4:

            theta = math.pi * x
            return ((math.sin(theta) / theta) * (math.sin(theta / 4) / (theta / 4)))
        else:
            return 0