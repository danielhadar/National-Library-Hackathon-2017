import sys
import scipy.misc
from urllib.request import urlopen

from PIL import Image
import requests
from io import BytesIO

import colorize
import impr_tools

import warnings
warnings.filterwarnings("ignore")


def image_from_url(url):
	with urlopen(url) as file:
		img = scipy.misc.imread(file, mode='RGB') / 255.

	# response = requests.get(url)
	# img = Image.open(BytesIO(response.content))
	return img


def boolean_from_char(char):
	if char == 'n':
		return False
	return True


usage = 'Usage: python main.py <file_url> <[y]/n: colorize> <[y]/n: histogram equalization> <[y]/n: adjust saturation>'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print(usage)
		exit()

	# Download image
	image_url = sys.argv[1]
	img = image_from_url(image_url)

	# Colorize
	should_colorize = True if len(sys.argv) <= 2 else sys.argv[2]
	if should_colorize:
		print("#-- Running Colorizing --#\n")
		img = colorize.colorize_image(img)
	else:
		print("!-- Skipping Colorizing --!\n")

	# Histogram Equalization
	should_equalize_hist = True if len(sys.argv) <= 3 else sys.argv[3]
	if should_equalize_hist:
		print("#-- Running Histogram Equalization --#\n")
		img = impr_tools.histogram_equalization(img)
	else:
		print("!-- Skipping Histogram Equalization --!\n")

	# Adjust Saturation
	should_adjust_saturation = True if len(sys.argv) <= 4 else sys.argv[4]
	if should_adjust_saturation:
		print("#-- Running Adjust Saturation --#\n")
		img = impr_tools.adjust_saturation(img, saturation_factor=1.15)
	else:
		print("!-- Skipping Adjust Saturation --!\n")

	# Done
	scipy.misc.imsave('./final_image.png', img)
	print('︵ \(°□°)/ ︵ ----> Done!\n')
