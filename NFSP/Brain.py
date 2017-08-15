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


class Brain:
    def __init__(
        self,
        n_actions,  # 动作数，也就是输出层的神经元数
        n_features,  # 特征数，也就是输入的矩阵的列数
        neurons_per_layer=np.array([10]),  # 隐藏层每层神经元数
        activation_function=tf.nn.relu,  # 激活函数
        Optimizer=tf.train.AdamOptimizer,  # 更新方法 tf.train.AdamOptimizer tf.train.GradientDescentOptimizer..
        learning_rate=0.01,  # 学习速率
        w_initializer=tf.random_normal_initializer(0., 0.3),
        b_initializer=tf.constant_initializer(0.1),
        output_graph=False,  # 使用tensorboard
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.neurons_per_layer = neurons_per_layer
        self.activation_function = activation_function
        self.lr = learning_rate
        self.Optimizer = Optimizer
        self.w_initializer = w_initializer
        self.b_initializer = b_initializer
        self.output_graph = output_graph
        self._build_net()

        self.sess = tf.Session()

        if self.output_graph:
            if tf.gfile.Exists("graph/"):
                tf.gfile.DeleteRecursively("graph/")
            tf.gfile.MakeDirs("graph/")
            self.merged = tf.summary.merge_all()
            # terminal 输入 tensorboard --logdir graph
            self.writer = tf.summary.FileWriter("graph/", self.sess.graph)

        self.sess.run(tf.global_variables_initializer())

    def _build_net(self):
        def add_layer(
            inputs,
            in_size,  # 传入数，即上一层神经元数
            out_size,  # 当前层的神经元数
            n_layer,  # 当前层是第几层
            c_names,
            activation_function=None,  # 激活函数
        ):
            layer_name = 'Layer%s' % n_layer
            with tf.variable_scope(layer_name):
                Weights = tf.get_variable('Weights', [in_size, out_size], initializer=self.w_initializer, collections=c_names)
                biases = tf.get_variable('biases', [1, out_size], initializer=self.b_initializer, collections=c_names)
                Wx_plus_b = tf.add(tf.matmul(inputs, Weights), biases)

                if activation_function is None:
                    outputs = Wx_plus_b
                else:
                    outputs = activation_function(Wx_plus_b, )

                if self.output_graph:
                    tf.summary.histogram(layer_name + '/weights', Weights)
                    tf.summary.histogram(layer_name + '/biases', biases)
                    tf.summary.histogram(layer_name + '/outputs', outputs)
            return outputs

        def build_eval_layers(inputs, neurons_per_layer, c_names):
            neurons_per_layer = neurons_per_layer.ravel()  # 平坦化数组
            layer_numbers = neurons_per_layer.shape[0]  # 隐藏层层数
            neurons_range = range(0, layer_numbers)
            in_size = self.n_features
            for n_neurons in neurons_range:  # 构造隐藏层
                out_size = neurons_per_layer[n_neurons]
                inputs = add_layer(inputs, in_size, out_size, n_neurons + 1, c_names, self.activation_function)
                in_size = out_size

            out_size = self.n_actions
            out = add_layer(inputs, in_size, out_size, layer_numbers + 1, c_names, None)  # 构造输出层
            return out

        def build_average_policy_layers(inputs, neurons_per_layer, c_names):
            neurons_per_layer = neurons_per_layer.ravel()  # 平坦化数组
            layer_numbers = neurons_per_layer.shape[0]  # 隐藏层层数
            neurons_range = range(0, layer_numbers)
            in_size = self.n_features
            for n_neurons in neurons_range:  # 构造隐藏层
                out_size = neurons_per_layer[n_neurons]
                inputs = add_layer(inputs, in_size, out_size, n_neurons + 1, c_names, self.activation_function)
                in_size = out_size

            out_size = self.n_actions
            out = add_layer(inputs, in_size, out_size, layer_numbers + 1, c_names, tf.nn.softmax)  # 构造输出层 使用softmax
            return out

        # ------------------ 创建 average_policy 神经网络 ------------------
        self.ap_s = tf.placeholder(tf.float32, [None, self.n_features], name='average_policy_s')
        self.action = tf.placeholder(tf.float32, [None, self.n_actions], name='action')
        # self.policy_target = tf.placeholder(tf.float32, [None, self.n_actions], name='AP_target')
        with tf.variable_scope('average_policy_net'):
            c_names = ['average_policy_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            self.policy = build_average_policy_layers(self.ap_s, self.neurons_per_layer, c_names)

        with tf.variable_scope('ap_net_loss'):
            self.ap_net_loss = tf.reduce_mean(-tf.reduce_sum(self.n_actions * tf.log(self.policy), axis=1))  # 交叉熵
            if self.output_graph:
                tf.summary.scalar('ap_net_loss', self.ap_net_loss)

        with tf.variable_scope('ap_net_train'):
            self.ap_net_train_op = self.Optimizer(self.lr).minimize(self.ap_net_loss)

        # ------------------ 创建 eval 神经网络, 及时提升参数 ------------------
        self.eval_s = tf.placeholder(tf.float32, [None, self.n_features], name='eval_s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='q_target')  # for calculating eval loss

        with tf.variable_scope('eval_net'):
            c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            self.q_eval = build_eval_layers(self.eval_s, self.neurons_per_layer, c_names)

        with tf.variable_scope('eval_net_loss'):
            self.eval_net_loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
            if self.output_graph:
                tf.summary.scalar('eval_net_loss', self.eval_net_loss)

        with tf.variable_scope('eval_net_train'):
            self.eval_net_train_op = self.Optimizer(self.lr).minimize(self.eval_net_loss)

        # ------------------ 创建 target 神经网络, 提供 target Q ------------------
        self.target_s = tf.placeholder(tf.float32, [None, self.n_features], name='target_s')
        with tf.variable_scope('target_net'):
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            self.q_next = build_eval_layers(self.target_s, self.neurons_per_layer, c_names)

    def train_ap_net(self, input_s, action, learn_step_counter):
        _, cost = self.sess.run([self.ap_net_train_op, self.ap_net_loss], feed_dict={self.ap_s: input_s, self.action: action})

    def train_eval_net(self, input_s, q_target, learn_step_counter):
        # 训练 eval 神经网络
        _, cost = self.sess.run([self.eval_net_train_op, self.eval_net_loss], feed_dict={self.eval_s: input_s, self.q_target: q_target})

        '''
        if self.output_graph:
            # 每隔100步记录一次
            if learn_step_counter % 100 == 0:
                rs = self.sess.run(self.merged, feed_dict={self.eval_s: input_s, self.q_target: q_target, self.target_s: input_s})
                self.writer.add_summary(rs, learn_step_counter)
        '''
        return cost

    def predict_eval_action(self, input_s):
        actions_value = self.sess.run(self.q_eval, feed_dict={self.eval_s: input_s})
        return actions_value

    def predict_target_action(self, input_s):
        actions_value = self.sess.run(self.q_next, feed_dict={self.target_s: input_s})
        return actions_value

    def replace_target_params(self):
        # 将 target_net 的参数 替换成 eval_net 的参数
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        for t, e in zip(t_params, e_params):
            self.sess.run(tf.assign(t, e))


if __name__ == '__main__':
    Brain = Brain(n_actions=1, n_features=1, output_graph=True)