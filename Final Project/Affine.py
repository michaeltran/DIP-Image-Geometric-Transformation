import cv2
import numpy as np
from Interpolation import interpolation
from Scaling import Scaling

class Affine:

    def affine_transform(self, image_name, pts1, pts2):
        
        input_image = cv2.imread(image_name, 1)

        print(input_image.shape)
        file_name = "ReferenceImages/affine.jpg"

        rows,cols,ch = input_image.shape

        #pts1 = np.float32([[50,50],[200,50],[50,200]])
        #pts2 = np.float32([[10,100],[200,50],[100,250]])

        #pts1 = np.float32([[0,0],[rows,0],[0,cols]])
        #pts2 = np.float32([[0,0],[rows,0],[0,cols]])

        #M = cv2.getAffineTransform(pts1, pts2)

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

        M = self.getAffineMatrix(pts1, pts2)

        #dst = cv2.warpAffine(input_image, M, (cols,rows))
        dst = self.warpAffine(input_image, M)

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

    def warpAffine(self, img, M):
        rows, cols, ch = img.shape
        result_image = np.zeros(shape=(img.shape))
        img_size = np.zeros(shape=(img.shape))

        def GetBilinearPixel(imArr, posX, posY):
            interpolation_ref = interpolation()

            x1 = int(np.floor(posX))
            x2 = int(x1 + 1)
            y1 = int(np.floor(posY))
            y2 = int(y1 + 1)

            if (x2 >= rows):
                x2 = x1
            if (y2 >= cols):
                y2 = y1

            pt1 = ((x1, y1), imArr[y1][x1][0])
            pt2 = ((x2, y1), imArr[y1][x2][0])
            pt3 = ((x1, y2), imArr[y2][x1][0])
            pt4 = ((x2, y2), imArr[y2][x2][0])
            unknown = (posX, posY)
            resultant_intensity_r = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            pt1 = ((x1, y1), imArr[y1, x1][1])
            pt2 = ((x2, y1), imArr[y1, x2][1])
            pt3 = ((x1, y2), imArr[y2, x1][1])
            pt4 = ((x2, y2), imArr[y2, x2][1])
            unknown = (posX, posY)
            resultant_intensity_g = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            pt1 = ((x1, y1), imArr[y1, x1][2])
            pt2 = ((x2, y1), imArr[y1, x2][2])
            pt3 = ((x1, y2), imArr[y2, x1][2])
            pt4 = ((x2, y2), imArr[y2, x2][2])
            unknown = (posX, posY)
            resultant_intensity_b = interpolation_ref.bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)

            return (resultant_intensity_r, resultant_intensity_g, resultant_intensity_b)



        #for i in range(0, img.shape[0] - 1): #x
        #    for j in range(0, img.shape[1] - 1): #y
        #        #x' = ax + by + c
        #        #y' = dx + ey + f
        #        pos = np.array([[i],[j],[1]], np.float32)
        #        pos = np.matmul(M, pos)

        #        M = np.append(M, [[0,0,1]],axis = 0) 

        #        inverse = np.linalg.inv(M)

        #        print (M)
        #        print ()
        #        print (inverse)

        #        pos = np.array([[i],[j],[1]], np.float32)
        #        test = np.matmul(inverse, pos)

        #        #x_prime = int(pos[0][0])
        #        #y_prime = int(pos[1][0])
        #        #x_prime = int(pos[0][0] + 0.5)
        #        #y_prime = int(pos[1][0] + 0.5)
        #        x_prime = pos[0][0]
        #        y_prime = pos[1][0]
        #        if (x_prime <= rows-1 and x_prime >= 0 and y_prime <= cols-1 and y_prime >= 0):
        #            x_prime_rounded = int(x_prime + 0.5)
        #            y_prime_rounded = int(y_prime + 0.5)

        #            #print((x_prime_rounded, y_prime_rounded))

        #            img_size[y_prime_rounded][x_prime_rounded] = img_size[y_prime_rounded][x_prime_rounded] + 1
        #            result_image[y_prime_rounded][x_prime_rounded] += GetBilinearPixel(img, i, j)

        #            #if (x_prime_rounded > 0 and x_prime_rounded < rows - 1):
        #            #    img_size[y_prime_rounded][x_prime_rounded+1] = img_size[y_prime_rounded][x_prime_rounded+1] + 1
        #            #    result_image[y_prime_rounded][x_prime_rounded+1] += GetBilinearPixel(img, i+1, j)

        #            #if (y_prime_rounded > 0 and y_prime_rounded < cols - 1):
        #            #    img_size[y_prime_rounded+1][x_prime_rounded] = img_size[y_prime_rounded+1][x_prime_rounded] + 1
        #            #    result_image[y_prime_rounded+1][x_prime_rounded] += GetBilinearPixel(img, i, j+1)

        #            #if (x_prime_rounded > 0 and x_prime_rounded < rows - 1 and y_prime_rounded > 0 and y_prime_rounded < cols - 1):
        #            #    img_size[y_prime_rounded+1][x_prime_rounded+1] = img_size[y_prime_rounded+1][x_prime_rounded+1] + 1
        #            #    result_image[y_prime_rounded+1][x_prime_rounded+1] += GetBilinearPixel(img, i+1, j+1)


        #for i in range(0, result_image.shape[0]):
        #    for j in range(0, result_image.shape[1]):
        #        if (np.any(img_size[i][j] > 0)):
        #            result_image[i][j] = result_image[i][j] / img_size[i][j]

        M = np.append(M, [[0,0,1]],axis = 0) 
        inverse = np.linalg.inv(M)

        for x_prime in range(0, img.shape[0]):
            for y_prime in range(0, img.shape[1]):
                pos = np.array([[x_prime],[y_prime],[1]], np.float32)
                pos = np.matmul(inverse, pos)

                x = pos[0][0]
                y = pos[1][0]

                if (x <= rows - 1 and x >= 0 and y <= cols - 1 and y >= 0):
                    result_image[y_prime][x_prime] += GetBilinearPixel(img, x, y)

        return result_image