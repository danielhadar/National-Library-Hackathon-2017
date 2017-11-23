import sys
import scipy.misc
from urllib.request import urlopen

import colorize
import impr_tools

import warnings
warnings.filterwarnings("ignore")

def image_from_url(url):
	with urlopen(url) as file:
		return scipy.misc.imread(file, mode='RGB') / 255.


def boolean_from_char(char):
	if char == 'n':
		return False
	return True


def process_image(image_url, image_name, is_url, should_colorize, should_equalize_hist, should_adjust_saturation):
	# Download image
	if is_url:
		img = image_from_url(image_url)
	else:
		img = scipy.misc.imread(image_url, mode='RGB') / 255.

	# Colorize
	if should_colorize:
		print("#-- Running Colorizing --#\n")
		img = colorize.colorize_image(img)
	else:
		print("!-- Skipping Colorizing --!\n")

	# Histogram Equalization
	if should_equalize_hist:
		print("#-- Running Histogram Equalization --#\n")
		img = impr_tools.histogram_equalization(img)
	else:
		print("!-- Skipping Histogram Equalization --!\n")

	# Adjust Saturation
	if should_adjust_saturation:
		print("#-- Running Adjust Saturation --#\n")
		img = impr_tools.adjust_saturation(img, saturation_factor=1.15)
	else:
		print("!-- Skipping Adjust Saturation --!\n")

	# Done
	print("#-- Exporting... --#\n")
	scipy.misc.imsave('/var/www/html/'+image_name, img)
	print('----> Done! <----\n')


usage = 'Usage: python main.py <file_url> <[url]/file> <[y]/n: colorize> <[y]/n: histogram equalization> <[y]/n: adjust saturation>'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print(usage)
		exit()

	image_url = sys.argv[1]
	is_url = len(sys.argv) <= 2 or sys.argv[2] == 'url'
	should_colorize = True if len(sys.argv) <= 3 else boolean_from_char(sys.argv[3])
	should_equalize_hist = True if len(sys.argv) <= 4 else boolean_from_char(sys.argv[4])
	should_adjust_saturation = True if len(sys.argv) <= 5 else boolean_from_char(sys.argv[5])
	process_image(image_url, is_url, should_colorize, should_equalize_hist, should_adjust_saturation)