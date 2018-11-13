import numpy as np


class Translation:

    def translate(self, image, heightValue, widthValue):
        height, width = image.shape[0], image.shape[1]
        result = np.zeros(image.shape, np.uint8)

        for h in range(height):
            for w in range(width):
                new_w = w - widthValue
                new_h = h - heightValue
                if new_w >= 0 and new_h >= 0 and new_w < width and new_h < height:
                    result[h, w] = image[new_h, new_w]

        return result

