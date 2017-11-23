import os, sys
from skimage import exposure
from skimage import color

import scipy.misc
from math import exp

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as splinalg

import skimage.color


def _wls_filter(input_image, lambda_=1.0, alpha=1.2, guide_image=None):
    if guide_image is None:
        guide_image = np.log(input_image + 1e-8)

    small_number = 0.0001

    rows, columns = input_image.shape
    k = rows * columns

    dy = np.diff(guide_image, 1, axis=0)
    dy = -lambda_ / (np.abs(dy) ** alpha + small_number)
    dy = np.pad(dy, ((0,1), (0,0)), mode='constant')
    dy = dy.flatten('F')

    dx = np.diff(guide_image, 1, axis=1)
    dx = -lambda_ / (np.abs(dx) ** alpha + small_number)
    dx = np.pad(dx, ((0,0), (0,1)), mode='constant')
    dx = dx.flatten('F')

    d = (-rows, -1)
    A = sparse.diags([dx, dy], d, (k, k))

    e = dx
    w = np.pad(dx, (rows, 0), mode='constant')[:-rows]
    s = dy
    n = np.pad(dy, (1, 0), mode='constant')[:-1]

    D = np.ones(k) - (e + w + s + n)
    F = A + A.T + sparse.diags([D], [0], (k, k))

    solution = splinalg.spsolve(F, input_image.flatten('F')).reshape((rows, columns), order='F')
    return solution


def wls(image):
    assert(image.ndim == 3)
    guide_image = np.log(skimage.color.rgb2gray(image) + 1e-8)
    out_image = np.zeros_like(image)
    for c in range(image.shape[-1]):
        print(c)
        out_image[:,:,c] = _wls_filter(image[:,:,c], lambda_=0.05,  guide_image=guide_image)
    return out_image


def histogram_equalization(img):
	return exposure.equalize_hist(img)


def adaptive_histogram_equalization(img):
	return exposure.equalize_adapthist(img, clip_limit=0.01)


def gamma_correction(img, gamma=1, gain=1):
	return exposure.adjust_gamma(img, gamma=gamma, gain=gain)


def logarithmic_correction(img, gain=1, inverse=False):
	return exposure.adjust_log(img, gain=gain, inv=inverse)


def sigmoid(x):
    if (type(x) != 'float'): return x
    exp(2 * x - 10) / (1 + exp(2 * x - 10))

def adjust_saturation(img, saturation_factor):
    hsv = color.rgb2hsv(img)
    # hsv[:, :, 1] = np.clip(hsv[:, : ,1] * saturation_factor, 0, 1)

    dim_x, dim_y = hsv[:, :, 1].shape
    for x in range(dim_x):
        for y in range(dim_y):
            hsv[:, :, 1][x][y] = sigmoid(hsv[:, :, 1][x][y])

    return color.hsv2rgb(hsv)

def improve_image(fn):
    image = scipy.misc.imread(fn, mode='RGB')
    improved_image =  adjust_saturation(histogram_equalization(image), saturation_factor=1.15).astype(np.float32)
    #smoothed_image = cv2.ximgproc.guidedFilter(improved_image, improved_image, radius=6, eps=0.1*0.1)
    ext = os.path.splitext(fn)[1]
    out_fn = fn.replace(ext, '.improved' + ext)

    scipy.misc.imsave(out_fn, improved_image)

# used for eyeball testing
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        improve_image(fn)
        print('Improved {}'.format(fn))

