import os
import sys

import numpy as np

import skimage.color
import skimage.transform
import skimage.io

import scipy.misc

MIN_AXIS_SIZE = 360
TEMP_IMG_NAME = 'temp'

def colorize_image(input_image):
    small_size = np.array(input_image.shape[:2]) * (float(MIN_AXIS_SIZE) / min(input_image.shape[:2]))
    small_size = np.round(small_size).astype(int)
    input_image_downsampled = skimage.transform.resize(input_image, small_size, preserve_range=True,
                                                       mode='reflect')

    small_fn = TEMP_IMG_NAME+'.small.png'
    small_colored_fn = TEMP_IMG_NAME+'.small.color.png'

    scipy.misc.imsave(small_fn, input_image_downsampled)
    os.system('th colorize.lua %s %s colornet.t7' % (small_fn, small_colored_fn))

    small_colored = skimage.io.imread(small_colored_fn)
    small_chroma = skimage.color.rgb2yuv(small_colored)

    upscaled_chroma = skimage.transform.resize(small_chroma,
                                               input_image.shape, preserve_range=True,
                                               mode='reflect')[:, :, 1:]
    orig_lum = input_image

    combined_lab = np.concatenate([orig_lum[:, :, 0:1], upscaled_chroma], axis=-1)
    out_image = skimage.color.yuv2rgb(combined_lab).clip(0., 1.)

    os.unlink(small_fn)
    os.unlink(small_colored_fn)
    return out_image


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        colorize_image(fn)
        print('Colorized {}'.format(fn))
