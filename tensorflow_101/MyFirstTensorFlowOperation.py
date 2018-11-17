import tensorflow as tf

a = tf.constant([40.0, 50.0])
b = tf.constant([2.0, 1.0])

my_first_ph = tf.placeholder(dtype=tf.float32)

add_op = tf.add(a, b)

mask_op = add_op * my_first_ph

policy = mask_op


sess = tf.get_default_session()

if not sess:
    sess = tf.Session()
    print(sess.run(mask_op, feed_dict=
    {
        my_first_ph: 2.0
    }))