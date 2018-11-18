import numpy as np

import cv2

import matplotlib.pyplot as plt


def main():
    data = cv2.imread("Lenna0.jpg")

    plot_polar_image(data, origin=None)
    # plot_directional_intensity(data, origin=None)

    #plt.show()


def plot_polar_image(data, origin=None):
    """Plots an image reprojected into polar coordinages with the origin
    at "origin" (a tuple of (x0, y0), defaults to the center of the image)"""
    polar_grid, r, theta = reproject_image_into_polar(data, origin)

    plt.figure()
    #plt.imshow(polar_grid, extent=(512, 0, 512, 0))
    plt.imsave('test.png', polar_grid, origin="lower")



def index_coords(data, origin=None):
    """Creates x & y coords for the indicies in a numpy array "data".
    "origin" defaults to the center of the image. Specify origin=(0,0)
    to set the origin to the lower left corner of the image."""
    ny, nx = data.shape[:2]
    if origin is None:
        origin_x, origin_y = nx // 2, ny // 2
    else:
        origin_x, origin_y = origin
    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    x -= origin_x
    y -= origin_y
    return x, y


def cart2polar(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    return r, theta


def polar2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def get_approx_points(band, coords):
    result = []
    max_x, max_y = band.shape
    size = len(coords[0])
    for i in range(size):
        val1 = int(coords[0][i] + 0.5)
        val2 = int(coords[1][i] + 0.5)
        if val1 >= max_x or val2 >= max_y or val1 < 0 or val2 < 0:
            result.append(0)
        else:
            result.append(band[val1][val2])

    return np.array(result)


def reproject_image_into_polar(data, origin=None):
    """Reprojects a 3D numpy array ("data") into a polar coordinate system.
    "origin" is a tuple of (x0, y0) and defaults to the center of the image."""
    ny, nx = data.shape[:2]
    if origin is None:
        origin = (nx // 2, ny // 2)

    # Determine that the min and max r and theta coords will be...
    x, y = index_coords(data, origin=origin)
    r, theta = cart2polar(x, y)
    # print(r.max())

    # Make a regular (in polar space) grid based on the min and max r & theta
    r_i = np.linspace(r.min(), r.max(), nx)
    theta_i = np.linspace(theta.min(), theta.max(), ny)
    r_grid, theta_grid = np.meshgrid(r_i, theta_i)

    # Project the r and theta grid back into pixel coordinates
    xi, yi = polar2cart(r_grid, theta_grid)
    xi += origin[0]  # We need to shift the origin back to
    yi += origin[1]  # back to the lower-left corner...

    # print(xi,yi)

    xi, yi = xi.flatten(), yi.flatten()
    coords = np.vstack((yi, xi))  # (map_coordinates requires a 2xn array)

    # Reproject each band individually and the restack
    # (uses less memory than reprojection the 3-dimensional array in one step)
    bands = []

    for band in data.T:
        print(band.shape)
        # zi = sp.ndimage.map_coordinates(band, coords, order=0)
        print(coords[0][0], coords[0][1])

        zi = get_approx_points(band, coords)

        # print(zi)

        bands.append(zi.reshape((nx, ny)))
    output = np.dstack(bands)
    print(output.shape)
    return output, r_i, theta_i


if __name__ == '__main__':
    main()