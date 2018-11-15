import numpy as np

class Rotation:

    def rotate(self, image, angle, direction):
        print("in rotate function call")
        PI = np.pi

        if direction == "clockwise":  # clockwise
            angle = float(angle)

        elif direction == "counterclockwise":  # counterclockwise
            a = float(angle)
            angle = -a

        degree = float(angle) * PI / 180.
        cos = np.cos(degree)
        sin = np.sin(degree)
        sp = image.shape
        width = sp[1]
        height = sp[0]

        # x,y store the four corner coordinatation
        x = [0, 0, 0, 0]
        y = [0, 0, 0, 0]
        x1 = [0, 0, 0, 0]
        y1 = [0, 0, 0, 0]
        x[0] = -(width - 1) / 2
        x[1] = -x[0]
        x[2] = -x[0]
        x[3] = x[0]
        y[0] = -(height - 1) / 2
        y[1] = y[0]
        y[2] = -y[0]
        y[3] = -y[0]
        # x1,y1 store the new image four corner coordinatation
        for i in range(4):
            x1[i] = (int)(x[i] * cos + y[i] * sin + 0.5)
            y1[i] = (int)(-x[i] * sin + y[i] * cos + 0.5)

        # newWidth=int(height * abs(sin) + width * abs(cos))
        # newHeight=int (width * abs (sin) + height * abs (cos))
        if (abs(y1[2] - y1[0]) > abs(y1[3] - y1[1])):
            newHeight = abs(y1[2] - y1[0])
            newWidth = abs(x1[3] - x1[1])

        else:
            newHeight = abs(y1[3] - y1[1])
            newWidth = abs(x1[2] - x1[0])

        rotateImage = np.zeros((newHeight, newWidth, image.ndim), dtype=np.uint8)

        fx = -1 * (newWidth - 1) * cos * 0.5 - (newHeight - 1) * sin * 0.5 + (width - 1) / 2
        fy = (newWidth - 1) * sin * 0.5 - (newHeight - 1) * cos * 0.5 + (height - 1) / 2

        temp = np.array([0, 0, 0, 0], dtype=int)
        channel = image.ndim
        for i in range(newHeight):
            for j in range(newWidth):
                # [s r 1] = [j i 1] * HINV*/
                a = j * cos + i * sin + fx
                b = -j * sin + i * cos + fy

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