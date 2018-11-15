import cv2
import numpy as np
from datetime import datetime


def logpolar_naive(image, i_0, j_0, p_n=None, t_n=None):
    (i_n, j_n) = image.shape[:2]

    i_c = max(i_0, i_n - i_0)
    j_c = max(j_0, j_n - j_0)
    d_c = (i_c ** 2 + j_c ** 2) ** 0.5

    if p_n == None:
        p_n = int(np.ceil(d_c))

    if t_n == None:
        t_n = j_n

    p_s = np.log(d_c) / p_n
    t_s = 2.0 * np.pi / t_n

    transformed = np.zeros((p_n, t_n) + image.shape[2:], dtype=image.dtype)

    for p in range(0, p_n):
        p_exp = np.exp(p * p_s)
        for t in range(0, t_n):
            t_rad = t * t_s

            i = int(i_0 + p_exp * np.sin(t_rad))
            j = int(j_0 + p_exp * np.cos(t_rad))

            if 0 <= i < i_n and 0 <= j < j_n:
                transformed[p, t] = image[i, j]

    return transformed


_transforms = {}


def _get_transform(i_0, j_0, i_n, j_n, p_n, t_n, p_s, t_s):
    transform = _transforms.get((i_0, j_0, i_n, j_n, p_n, t_n))

    if transform == None:
        i_k = []
        j_k = []
        p_k = []
        t_k = []

        for p in range(0, p_n):
            p_exp = np.exp(p * p_s)
            for t in range(0, t_n):
                t_rad = t * t_s

                i = int(i_0 + p_exp * np.sin(t_rad))
                j = int(j_0 + p_exp * np.cos(t_rad))

                if 0 <= i < i_n and 0 <= j < j_n:
                    i_k.append(i)
                    j_k.append(j)
                    p_k.append(p)
                    t_k.append(t)

        transform = ((np.array(p_k), np.array(t_k)), (np.array(i_k), np.array(j_k)))
        _transforms[i_0, j_0, i_n, j_n, p_n, t_n] = transform

    return transform


def logpolar_fancy(image, i_0, j_0, p_n=None, t_n=None):
    (i_n, j_n) = image.shape[:2]

    i_c = max(i_0, i_n - i_0)
    j_c = max(j_0, j_n - j_0)
    d_c = (i_c ** 2 + j_c ** 2) ** 0.5

    if p_n == None:
        p_n = int(np.ceil(d_c))

    if t_n == None:
        t_n = j_n

    p_s = np.log(d_c) / p_n
    t_s = 2.0 * np.pi / t_n

    (pt, ij) = _get_transform(i_0, j_0, i_n, j_n, p_n, t_n, p_s, t_s)

    transformed = np.zeros((p_n, t_n) + image.shape[2:], dtype=image.dtype)

    transformed[pt] = image[ij]
    return transformed

img = cv2.imread("Lenna.png", 1)
# result = logpolar_naive(img, 10, 10)  # height, width

result = logpolar_fancy(img, 128, 128)
img2 = cv2.logPolar(img, (img.shape[0]/2, img.shape[1]/2), 10, cv2.WARP_FILL_OUTLIERS)

output_dir = 'output/'
output_image_name = output_dir+"TranslationResult"+datetime.now().strftime("%m%d-%H%M%S")+".jpg"

cv2.imwrite(output_image_name, img2)