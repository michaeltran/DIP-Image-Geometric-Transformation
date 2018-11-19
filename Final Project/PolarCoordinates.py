import numpy as np

class PolarCoordinates:
    def polar_transform(self, image, center, max_radius):
        width, height, ch = image.shape

        result_image = np.zeros(shape=image.shape)

        Kx = width / max_radius
        Ky = height / (2 * np.pi)

        for theta in range(0, height):
            for rho in range(0, width):
                real_theta = theta / Ky
                real_rho = rho / Kx
                x = real_rho * np.cos(real_theta)
                x = x + center[0] # shift from center
                y = real_rho * np.sin(real_theta)
                y = y + center[1] # shift from center
                # add interpolation methods here
                result_image[theta][rho] = image[int(y)][int(x)]
                #result_image[theta][rho] = scaling_ref.apply_bilinear(image, x, y)

        return result_image

    def log_polar_transform(self, image, center, max_radius):
        width, height, ch = image.shape

        result_image = np.zeros(shape=image.shape)

        M = width / np.log(max_radius)
        Ky = height / (2 * np.pi)

        for theta in range(0, height):
            for rho in range(0, width):
                real_theta = theta / Ky
                real_rho = rho / M
                x = np.e**real_rho * np.cos(real_theta)
                x = x + center[0] # shift from center
                y = np.e**real_rho * np.sin(real_theta)
                y = y + center[1] # shift from center
                # add interpolation methods here
                result_image[theta][rho] = image[int(y)][int(x)]
                #result_image[theta][rho] = scaling_ref.apply_bilinear(image, x, y)

        return result_image