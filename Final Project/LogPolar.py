import numpy as np
import math

class LogPolar:
    def logpolar_naive(self,image, i_0, j_0, p_n=None, t_n=None):
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
