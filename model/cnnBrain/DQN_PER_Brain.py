# -*- coding: UTF-8 -*-
"""
by Howard
using:
- python: 3.6
- Tensorflow: 1.2.1
- gym: 0.9.2
"""
import tensorflow as tf
import numpy as np
import re
from .DQN_Brain import DQN_Brain as Brain


class DQN_PER_Brain(Brain):
    def __init__(
        self,
        n_actions,  # 动作数，也就是输出层的神经元数
        observation_width,  # 图片的width
        observation_height,  # 图片的height
        observation_depth,  # 图片的depth
        filters_per_layer=np.array([32, 64, 64]),  # Conv_and_Pool_Layer i 层中 卷积的filters
        activation_function=tf.nn.relu,  # 激活函数
        kernel_size_per_layer=[(8, 8), (4, 4), (3, 3)],  # 卷积核的size
        conv_strides_per_layer=[(4, 4), (2, 2), (1, 1)],  # 卷积层的strides
        padding='valid',  # same or valid
        b_initializer=tf.constant_initializer(0.01),  # tf.constant_initializer(0.1)
        pooling_function=tf.layers.max_pooling2d,  # max_pooling2d or average_pooling2d
        pool_size=(2, 2),  # pooling的size
        pool_strides=(2, 2),  # pooling的strides
        Optimizer=tf.train.RMSPropOptimizer,  # 更新方法 tf.train.AdamOptimizer tf.train.RMSPropOptimizer..
        learning_rate=0.00025,  # 学习速率
        output_graph=False,  # 使用 tensorboard
        restore=False,  # 是否使用存储的神经网络
        checkpoint_dir='DQN_CNN_Net',  # 存储的dir name
    ):
        # self.n_actions = n_actions
        # self.observation_width = observation_width
        # self.observation_height = observation_height
        # self.observation_depth = observation_depth
        # self.filters_per_layer = filters_per_layer
        # self.activation_function = activation_function
        # self.kernel_size_per_layer = kernel_size_per_layer
        # self.conv_strides_per_layer = conv_strides_per_layer
        # self.padding = padding
        # self.b_initializer = b_initializer
        # self.pooling_function = pooling_function
        # self.pool_size = pool_size
        # self.pool_strides = pool_strides
        # self.Optimizer = Optimizer
        # self.lr = learning_rate
        # self.output_graph = output_graph
        # self._build_net()
        # self.checkpoint_dir = checkpoint_dir
        # self.sess = tf.Session()
        super(DQN_PER_Brain, self).__init__(n_actions, observation_width, observation_height, observation_depth, filters_per_layer, activation_function,
                                            kernel_size_per_layer, conv_strides_per_layer, padding, b_initializer, pooling_function, pool_size, pool_strides,
                                            Optimizer, learning_rate,  output_graph, restore, checkpoint_dir)

    def _build_net(self):
        def add_conv_and_pool_layer(
            inputs,
            n_layer,  # 当前层是第几层
            activation_function=tf.nn.relu,  # 激活函数
            filters=32,
            kernel_size=(5, 5),  # 卷积核的size
            conv_strides=(1, 1),  # 卷积层的strides
            padding='valid',  # same or valid
            pooling_function=tf.layers.max_pooling2d,  # max_pooling2d or average_pooling2d
            pool_size=(2, 2),  # pooling的size
            pool_strides=(2, 2),  # pooling的strides
        ):
            layer_name = 'Conv_and_Pool_Layer%s' % n_layer
            with tf.variable_scope(layer_name):
                conv_name = 'Conv%s' % n_layer
                pool_name = 'Pool%s' % n_layer
                conv = tf.layers.conv2d(inputs=inputs, filters=filters, kernel_size=kernel_size, padding=padding, strides=conv_strides,
                                        activation=activation_function, bias_initializer=self.b_initializer, name=conv_name)
                # pool = pooling_function(inputs=conv, pool_size=pool_size, strides=pool_strides, name=pool_name)
            return conv

        def build_layers(inputs, filters_per_layer, kernel_size_per_layer, conv_strides_per_layer):
            filters_per_layer = filters_per_layer.ravel()  # 平坦化数组
            layer_numbers = filters_per_layer.shape[0]
            l_range = range(0, layer_numbers)
            for l in l_range:  # 构造卷积和池化层
                filters = filters_per_layer[l]
                kernel_size = kernel_size_per_layer[l]
                conv_strides = conv_strides_per_layer[l]
                inputs = add_conv_and_pool_layer(inputs=inputs, n_layer=l + 1, activation_function=self.activation_function,
                                                 filters=filters, kernel_size=kernel_size, conv_strides=conv_strides,
                                                 padding=self.padding, pooling_function=self.pooling_function,
                                                 pool_size=self.pool_size, pool_strides=self.pool_strides)

            # 构造全连接层
            flat_size = inputs.shape[1] * inputs.shape[2] * inputs.shape[3]
            inputs_flat = tf.reshape(inputs, [-1, int(flat_size)])
            dense = tf.layers.dense(inputs=inputs_flat, units=512, activation=tf.nn.relu, bias_initializer=self.b_initializer)

            # 添加 dropout 处理过拟合
            # dropout = tf.layers.dropout(inputs=dense, rate=0.4)
            out_size = self.n_actions
            # 输出层
            # out = tf.layers.dense(inputs=dropout, units=out_size)
            out = tf.layers.dense(inputs=dense, units=out_size, bias_initializer=self.b_initializer)
            return out

        # ------------------ 创建 eval 神经网络, 及时提升参数 ------------------
        self.s = tf.placeholder(tf.float32, [None, self.observation_width, self.observation_height, self.observation_depth], name='s')  # input
        self.q_target = tf.placeholder(tf.float32, [None], name='Q_target')  # for calculating loss
        self.ISWeights = tf.placeholder(tf.float32, [None], name='IS_weights')

        # self.normalized_s = tf.to_float(self.s) / 255.0
        with tf.variable_scope('eval_net'):
            self.q_eval = build_layers(self.s, self.filters_per_layer, self.kernel_size_per_layer, self.conv_strides_per_layer)

        with tf.variable_scope('loss'):
            self.action = tf.placeholder(tf.float32, [None, self.n_actions], name='action')  # one hot presentatio
            Q_action = tf.reduce_sum(tf.multiply(self.q_eval, self.action), reduction_indices=1)
            # --------per---------
            print('self.q_target', self.q_target, 'Q_action', Q_action)
            self.abs_errors = tf.abs(self.q_target - Q_action)    # for updating Sumtree
            print('self.abs_errors', self.abs_errors)
            # --------new---------
            difference = tf.abs(Q_action - self.q_target)
            quadratic_part = tf.clip_by_value(difference, 0.0, 1.0)
            linear_part = difference - quadratic_part
            errors = (0.5 * tf.square(quadratic_part)) + linear_part
            # self.loss = tf.reduce_sum(errors)
            self.loss = tf.reduce_sum(tf.multiply(self.ISWeights, errors))
            # ----------------------
            # self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, Q_action))
            # self.loss = tf.reduce_mean(tf.square(self.q_target - Q_action))
            if self.output_graph:
                tf.summary.scalar('loss', self.loss)

        with tf.variable_scope('train'):
            self.train_op = self.Optimizer(learning_rate=self.lr, decay=.95, epsilon=.01).minimize(self.loss)

        # ------------------ 创建 target 神经网络, 提供 target Q ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.observation_width, self.observation_height, self.observation_depth], name='s_')
        # self.normalized_s_ = tf.to_float(self.s_) / 255.0
        with tf.variable_scope('target_net'):
            self.q_next = build_layers(self.s_, self.filters_per_layer, self.kernel_size_per_layer, self.conv_strides_per_layer)

        # ------------------ replace_target_params op ------------------
        self.update_target = []
        rr = re.compile('target_net')
        t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, rr)
        rr = re.compile('eval_net')
        e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, rr)
        for t, e in zip(t_params, e_params):
            self.update_target.append(tf.assign(t, e))

    # 训练 eval 神经网络
    def train(self, input_s, q_target, action, ISWeights, costCalculate=False):
        if costCalculate:
            _, abs_errors, cost = self.sess.run([self.train_op, self.abs_errors, self.loss], feed_dict={
                self.s: input_s, self.action: action, self.q_target: q_target, self.ISWeights: ISWeights})
            return abs_errors, cost
        else:
            _, abs_errors = self.sess.run([self.train_op, self.abs_errors], feed_dict={self.s: input_s, self.action: action, self.q_target: q_target, self.ISWeights: ISWeights})
            return abs_errors

    def output_tensorboard(self, input_s, q_target, input_s_, action, ISWeights, learn_step_counter):
        if self.output_graph:
            # 每隔100步记录一次
            if learn_step_counter % 100 == 0:
                rs = self.sess.run(self.merged, feed_dict={self.s: input_s, self.q_target: q_target, self.s_: input_s_, self.action: action, self.ISWeights: ISWeights})
                self.writer.add_summary(rs, learn_step_counter)


if __name__ == '__main__':
    Brain = CNN(n_actions=2, observation_width=210, observation_height=160, observation_depth=3, output_graph=True)
