import cv2
import numpy as np
from Interpolation import interpolation
from Scaling import Scaling

class Affine:

    def affine_transform(self, image_name, pts1, pts2):
        input_image = cv2.imread(image_name, 1)
        file_name = "ReferenceImages/affine.jpg"
        rows, cols, ch = input_image.shape

        ##SHEAR
        #M[0][0] = 1
        #M[0][1] = 0
        #M[1][0] = 2
        #M[1][1] = 1

        ##SCALE
        #M[0][0] = 3
        #M[0][1] = 0
        #M[1][0] = 0
        #M[1][1] = 3

        ##Rotation
        #M[0][0] = np.cos(45)
        #M[0][1] = np.sin(45)
        #M[1][0] = -np.sin(45)
        #M[1][1] = np.cos(45)

        #M = cv2.getAffineTransform(pts1, pts2)
        M = self.getAffineMatrix(pts1, pts2)

        #dst = cv2.warpAffine(input_image, M, (cols,rows))
        dst = self.warpAffine(input_image, M, 1, 1)

        cv2.imwrite(file_name, dst)

        return file_name, rows, cols

    def shear_transform(self, image_name, shear_x, shear_y):
        input_image = cv2.imread(image_name, 1)
        file_name = "ReferenceImages/shear.jpg"
        rows, cols, ch = input_image.shape

        M = np.empty((0,3))
        M = np.append(M, [[1, shear_x, 0]], axis = 0)
        M = np.append(M, [[shear_y, 1, 0]], axis = 0)

        dst = self.warpAffine(input_image, M, 1 + shear_x, 1 + shear_y)
        cv2.imwrite(file_name, dst)

        return file_name, rows, cols

    def getAffineMatrix(self, pt1, pt2):
        #pt1 = og coords
        #pt2 = target coords

        X = np.empty((0,6))

        X = np.append(X, [[pt1[0][0], pt1[0][1], 1, 0, 0, 0]], axis = 0)
        X = np.append(X, [[0, 0, 0, pt1[0][0], pt1[0][1], 1]], axis = 0)
        X = np.append(X, [[pt1[1][0], pt1[1][1], 1, 0, 0, 0]], axis = 0)
        X = np.append(X, [[0, 0, 0, pt1[1][0], pt1[1][1], 1]], axis = 0)
        X = np.append(X, [[pt1[2][0], pt1[2][1], 1, 0, 0, 0]], axis = 0)
        X = np.append(X, [[0, 0, 0, pt1[2][0], pt1[2][1], 1]], axis = 0)

        XP = np.empty((0,1))
        XP = np.append(XP, [[pt2[0][0]]], axis = 0)
        XP = np.append(XP, [[pt2[0][1]]], axis = 0)
        XP = np.append(XP, [[pt2[1][0]]], axis = 0)
        XP = np.append(XP, [[pt2[1][1]]], axis = 0)
        XP = np.append(XP, [[pt2[2][0]]], axis = 0)
        XP = np.append(XP, [[pt2[2][1]]], axis = 0)

        X_inverse = np.linalg.inv(X)
        M_deconstructed = np.matmul(X_inverse, XP)

        M = np.empty((0,3))
        M = np.append(M, [[M_deconstructed[0][0], M_deconstructed[1][0], M_deconstructed[2][0]]], axis = 0)
        M = np.append(M, [[M_deconstructed[3][0], M_deconstructed[4][0], M_deconstructed[5][0]]], axis = 0)

        return M

    def warpAffine(self, img, M, image_size_factor_x, image_size_factor_y):
        rows, cols, ch = img.shape
        result_image = np.zeros(shape=(int(rows * image_size_factor_y), int(cols * image_size_factor_x), ch))
        #img_size = np.zeros(shape=(rows, cols, ch))

        def GetBilinearPixel(image, posX, posY):
            interpolation_ref = interpolation()

            x1 = int(np.floor(posX))
            x2 = int(x1 + 1)
            y1 = int(np.floor(posY))
            y2 = int(y1 + 1)

            if (x2 >= rows):
                x2 = x1
            if (y2 >= cols):
                y2 = y1

            pt1 = ((x1, y1), image[y1][x1][0])
            pt2 = ((x2, y1), image[y1][x2][0])
            pt3 = ((x1, y2), image[y2][x1][0])
            pt4 = ((x2, y2), image[y2][x2][0])
            unknown = (posX, posY)
            resultant_intensity_r = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            pt1 = ((x1, y1), image[y1, x1][1])
            pt2 = ((x2, y1), image[y1, x2][1])
            pt3 = ((x1, y2), image[y2, x1][1])
            pt4 = ((x2, y2), image[y2, x2][1])
            unknown = (posX, posY)
            resultant_intensity_g = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            pt1 = ((x1, y1), image[y1, x1][2])
            pt2 = ((x2, y1), image[y1, x2][2])
            pt3 = ((x1, y2), image[y2, x1][2])
            pt4 = ((x2, y2), image[y2, x2][2])
            unknown = (posX, posY)
            resultant_intensity_b = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            return (resultant_intensity_r, resultant_intensity_g, resultant_intensity_b)

        M = np.append(M, [[0,0,1]],axis = 0) 
        inverse = np.linalg.inv(M)

        for x_prime in range(0, int(img.shape[0] * image_size_factor_x)):
            for y_prime in range(0, int(img.shape[1] * image_size_factor_y)):
                pos = np.array([[x_prime],[y_prime],[1]], np.float32)
                pos = np.matmul(inverse, pos)

                x = pos[0][0]
                y = pos[1][0]

                if (x <= rows - 1 and x >= 0 and y <= cols - 1 and y >= 0):
                    result_image[y_prime][x_prime] += GetBilinearPixel(img, x, y)

        return result_image