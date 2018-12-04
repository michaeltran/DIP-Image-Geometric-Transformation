import numpy as np

class Rotation:

    def rotate(self, image, angle, direction):
        print("in rotate function call")
        PI = np.pi

        if direction == "counterclockwise":  # clockwise
            angle = float(angle)


        elif direction == "clockwise":  # counterclockwise
            a = float(angle)
            angle = -a

        degree = float(angle) * PI / 180.
        cos = np.cos(degree)
        sin = np.sin(degree)
        sp = image.shape
        width = sp[1]
        height = sp[0]

        newWidth = int(height * abs(sin) + width * abs(cos))
        newHeight = int(width * abs(sin) + height * abs(cos))

        rotateImage = np.zeros((newHeight, newWidth, image.ndim), dtype=np.uint8)

        temp = np.array([0, 0, 0, 0], dtype=int)
        channel = image.ndim
        for i in range(newHeight):
            for j in range(newWidth):

                a = cos * (j - (newWidth + 1) / 2) - sin * (i - (newHeight + 1) / 2) + (width + 1) / 2
                b = sin * (j - (newWidth + 1) / 2) + cos * (i - (newHeight + 1) / 2) + (height + 1) / 2

                # bilinear inpterpolation
                if b < 1.0 or a < 1.0 or b >= height or a >= width:
                    for c in range(channel):
                        rotateImage[i, j, c] = 0
                else:
                    b = b - 1
                    a = a - 1
                    ty = int(b)
                    tx = int(a)
                    by = int(b + 1)
                    bx = int(a + 1)
                    for c in range(channel):
                        temp[0] = image[ty, tx, c]
                        temp[1] = image[ty, bx, c]
                        temp[2] = image[by, tx, c]
                        temp[3] = image[by, bx, c]
                        z1 = (temp[1] - temp[0]) * (a - int(a)) + temp[0]
                        z2 = (temp[3] - temp[2]) * (a - int(a)) + temp[2]
                        z3 = int(z1 + (z2 - z1) * (b - int(b)))
                        rotateImage[i, j, c] = z3

        return rotateImage