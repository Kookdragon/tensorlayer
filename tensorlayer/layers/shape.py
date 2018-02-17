# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
from six.moves import xrange

from . import cost, files, iterate, ops, utils, visualize
from .core import *


class FlattenLayer(Layer):
    """
    The :class:`FlattenLayer` class is layer which reshape high-dimension
    input to a vector. Then we can apply DenseLayer, RNNLayer, ConcatLayer and
    etc on the top of it.

    [batch_size, mask_row, mask_col, n_mask] ---> [batch_size, mask_row * mask_col * n_mask]

    Parameters
    ----------
    layer : :class:`Layer`
        Previous layer.
    name : str
        A unique layer name.

    Examples
    --------
    >>> x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
    >>> net = tl.layers.InputLayer(x, name='input')
    >>> net = tl.layers.FlattenLayer(net, name='flatten')
    """

    def __init__(
            self,
            layer=None,
            name='flatten_layer',
    ):
        Layer.__init__(self, name=name)
        self.inputs = layer.outputs
        self.outputs = flatten_reshape(self.inputs, name=name)
        self.n_units = int(self.outputs.get_shape()[-1])
        logging.info("FlattenLayer %s: %d" % (self.name, self.n_units))
        self.all_layers = list(layer.all_layers)
        self.all_params = list(layer.all_params)
        self.all_drop = dict(layer.all_drop)
        self.all_layers.extend([self.outputs])


class ReshapeLayer(Layer):
    """
    The :class:`ReshapeLayer` class is layer which reshape the tensor.

    Parameters
    ----------
    layer : :class:`Layer`
        Previous layer
    shape : tuple of int
        The output shape, see ``tf.reshape``.
    name : str
        A unique layer name.

    Examples
    --------
    - Use TensorLayer
    >>> x = tf.placeholder(tf.float32, shape=[None, 28, 28, 1])
    >>> net = tl.layers.InputLayer(x, name='input')
    >>> net = tl.layers.ReshapeLayer(net, (-1, 28*28), name='reshape')
    >>> print(net.outputs)
    ... (?, 784)

    - Use native TensorFlow API ``tf.reshape``
    >>> x = tf.placeholder(tf.float32, shape=[None, 3])
    >>> y = tf.reshape(x, shape=[-1, 3, 3])
    >>> sess = tf.InteractiveSession()
    >>> print(sess.run(y, feed_dict={x:[[1,1,1],[2,2,2],[3,3,3],[4,4,4],[5,5,5],[6,6,6]]}))
    ... [[[ 1.  1.  1.]
    ... [ 2.  2.  2.]
    ... [ 3.  3.  3.]]
    ... [[ 4.  4.  4.]
    ... [ 5.  5.  5.]
    ... [ 6.  6.  6.]]]
    """

    def __init__(
            self,
            layer=None,
            shape=[],
            name='reshape_layer',
    ):
        Layer.__init__(self, name=name)
        self.inputs = layer.outputs
        self.outputs = tf.reshape(self.inputs, shape=shape, name=name)
        logging.info("ReshapeLayer %s: %s" % (self.name, self.outputs.get_shape()))
        self.all_layers = list(layer.all_layers)
        self.all_params = list(layer.all_params)
        self.all_drop = dict(layer.all_drop)
        self.all_layers.extend([self.outputs])


class TransposeLayer(Layer):
    """
    The :class:`TransposeLayer` class transposes the dimension of a teneor, see `tf.transpose() <https://www.tensorflow.org/api_docs/python/tf/transpose>`_ .

    Parameters
    ----------
    layer : :class:`Layer`
        Previous layer
    perm: list of int
        The permutation of the dimensions, similar with ``numpy.transpose``.
    name : str
        A unique layer name.
    """

    def __init__(
            self,
            layer=None,
            perm=None,
            name='transpose',
    ):
        Layer.__init__(self, name=name)
        self.inputs = layer.outputs
        assert perm is not None

        logging.info("TransposeLayer  %s: perm:%s" % (self.name, perm))
        # with tf.variable_scope(name) as vs:
        self.outputs = tf.transpose(self.inputs, perm=perm, name=name)
        self.all_layers = list(layer.all_layers)
        self.all_params = list(layer.all_params)
        self.all_drop = dict(layer.all_drop)
        self.all_layers.extend([self.outputs])
        # self.all_params.extend( variables )
