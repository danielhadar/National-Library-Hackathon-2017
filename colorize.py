import os
import sys

import numpy as np

import skimage.color
import skimage.transform
import skimage.io

import scipy.misc

if __name__ == '__main__':
    input_image = scipy.misc.imread(sys.argv[1], mode='RGB') / 255.
    small_size = (input_image.shape[0] // 4) , (input_image.shape[1] // 4)
    input_image_downsampled = skimage.transform.resize(input_image, small_size, preserve_range=True, mode='reflect')

    small_fn = sys.argv[1].replace(sys.argv[1][-4:], '.small' + sys.argv[1][-4:])
    small_colored_fn = sys.argv[1].replace(sys.argv[1][-4:], '.small.color' + sys.argv[1][-4:])
    out_fn = sys.argv[1].replace(sys.argv[1][-4:], '.color' + sys.argv[1][-4:])

    scipy.misc.imsave(small_fn, input_image_downsampled)
    os.system('th colorize.lua %s %s' % (small_fn, small_colored_fn))

    small_colored = skimage.io.imread(small_colored_fn)
    small_chroma = skimage.color.rgb2yuv(small_colored)

    upscaled_chroma = skimage.transform.resize(small_chroma,
        (input_image.shape[0], input_image.shape[1], 3), preserve_range=True, mode='reflect')[:,:,1:]
    orig_lum = input_image

    print(orig_lum.shape, upscaled_chroma.shape)
    combined_lab = np.concatenate([orig_lum[:,:,0:1], upscaled_chroma], axis=-1)
    out_image = skimage.color.yuv2rgb(combined_lab).clip(0., 1.)

    scipy.misc.imsave(out_fn, out_image)
