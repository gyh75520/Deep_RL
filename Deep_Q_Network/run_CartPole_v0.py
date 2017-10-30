# -*- coding: UTF-8 -*-
import gym
from MLP import Neural_Networks as brain
from Agent import Agent
import numpy as np

env = gym.make('CartPole-v0')   # 定义使用 gym 库中的那一个环境
env = env.unwrapped  # 注释掉的话 每局游戏 reward之和最高200

print(env.action_space.sample())  # 查看这个环境中可用的 action 有多少个
print(env.observation_space.shape)    # 查看这个环境中可用的 state 的 observation 有多少个
print(env.observation_space.high)   # 查看 observation 最高取值
print(env.observation_space.low)    # 查看 observation 最低取值

# learning_rate 重要
# restore 和 MAX_EPSILON 一起调整
Brain = brain(
    n_actions=env.action_space.n,
    n_features=env.observation_space.shape[0],
    neurons_per_layer=np.array([8, 4, 8]),
    learning_rate=0.001,
    output_graph=True,
    restore=False,
)
RL = Agent(
    brain=Brain,
    n_actions=env.action_space.n,
    observation_space_shape=env.observation_space.shape,
    reward_decay=0.9,
    replace_target_iter=200,
    memory_size=30000,
    MAX_EPSILON=0.9,
    LAMBDA=0.0001,
)

total_steps = 0


for i_episode in range(500):

    observation = env.reset()
    ep_r = 0
    totalR = 0
    while True:
        # env.render()

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.step(action)
        totalR += reward
        RL.store_memory(observation, action, reward, observation_, done)

        ep_r += reward
        if total_steps > 50:
            RL.learn()

        if done:
            print('episode: ', i_episode,
                  ' epsilon: ', round(RL.epsilon, 2),
                  'total_reward:', totalR)
            break

        observation = observation_
        total_steps += 1
Brain.save()  # 存储神经网络
