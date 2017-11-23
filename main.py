import sys
from PIL import Image
import requests
from io import BytesIO


import matplotlib.pyplot as plt


def image_from_url(url):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	return img




# Usage: python main.py <file_url> <[y]/n: colorize> <[y]/n: super-resolution>
if __name__ == '__main__':
	# Download image
	image_url = sys.argv[1]
	img = image_from_url(image_url)

	# Colorize
	if 
