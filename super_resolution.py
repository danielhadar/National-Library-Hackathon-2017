import sys
from nnlib import *

PER_CHANNEL_MEANS = np.array([0.47614917, 0.45001204, 0.40904046])

def super_upscale(fn):
    print(fn)
    fne = '.'.join(fn.split('.')[:-1])
    out_fn_super = fne + '.super.png'
    out_fn_bicubic = fne + '.bicubic.png'
    if os.path.exists(out_fn_super):
        print('skipping %s' % fn)
        return
    imgs = loadimg(fn)
    if imgs is None:
        return
    imgs = np.expand_dims(imgs, axis=0)
    if imgs.size > 5e6:
        print('Skipping %s because its size is %d' % (fn, imgs.size))
        return
    imgsize = np.shape(imgs)[1:]
    print('processing %s' % fn)
    xs = tf.placeholder(tf.float32, [1, imgsize[0], imgsize[1], imgsize[2]])
    rblock = [resi, [[conv], [relu], [conv]]]
    ys_est = NN('generator',
                [xs,
                 [conv], [relu],
                 rblock, rblock, rblock, rblock, rblock,
                 rblock, rblock, rblock, rblock, rblock,
                 [upsample], [conv], [relu],
                 [upsample], [conv], [relu],
                 [conv], [relu],
                 [conv, 3]])
    ys_res = tf.image.resize_images(xs, [4*imgsize[0], 4*imgsize[1]],
                                    method=tf.image.ResizeMethod.BICUBIC)
    ys_est += ys_res + PER_CHANNEL_MEANS
    sess = tf.InteractiveSession()
    tf.train.Saver().restore(sess, os.getcwd()+'/weights')
    output = sess.run([ys_est, ys_res+PER_CHANNEL_MEANS],
                      feed_dict={xs: imgs-PER_CHANNEL_MEANS})
    saveimg(output[0][0], out_fn_super)
    saveimg(output[1][0], out_fn_bicubic)
    sess.close()
    tf.reset_default_graph()


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        super_upscale(fn)