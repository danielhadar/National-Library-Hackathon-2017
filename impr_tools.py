import sys
from skimage import exposure
from skimage import color

import scipy.misc

import matplotlib.pyplot as plt

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


def adjust_saturation(img, saturation_factor):
	hsv = color.rgb2hsv(img)
	hsv[:, :, 1] = np.clip(hsv[:,:,1] * saturation_factor, 0, 1)
	return color.hsv2rgb(hsv)


# used for eyeball testing
if __name__ == '__main__':
	filename = sys.argv[1]
	input_image = scipy.misc.imread(filename, mode='RGB') / 255.

	output_image = histogram_equalization(input_image)
	#output_image = adjust_saturation(input_image, 1)

	fig = plt.figure()
	fig.add_subplot(1, 2, 1)
	imgplot = plt.imshow(input_image)
	fig.add_subplot(1, 2, 2)
	imgplot = plt.imshow(output_image)
	plt.show()