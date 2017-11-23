import sys
from skimage import exposure
import scipy.misc


import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def histogram_equalization(img):
	img_eq = exposure.equalize_hist(img)
	return img_eq


def adaptive_histogram_equalization(img):
	img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)
	return img_adapteq


if __name__ == '__main__':
	filename = sys.argv[1]
	input_image = scipy.misc.imread(filename, mode='RGB') / 255.

	output_image = histogram_equalization(input_image)

	fig = plt.figure()
	fig.add_subplot(1, 2, 1)
	imgplot = plt.imshow(input_image)
	fig.add_subplot(1, 2, 2)
	imgplot = plt.imshow(output_image)
	plt.show()