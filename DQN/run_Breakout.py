import gym
from CNN_Brain import CNN_Brain as brain
from Agent import Agent
import numpy as np
import blosc

env = gym.make('Breakout-v0')   # 定义使用 gym 库中的那一个环境


print(env.action_space.n)  # 查看这个环境中可用的 action 有多少个
print(env.observation_space)    # 查看这个环境中可用的 state 的 observation 有多少个
# print(env.observation_space.high)   # 查看 observation 最高取值
# print(env.observation_space.low)    # 查看 observation 最低取值


Brain = brain(n_actions=env.action_space.n,
              observation_width=env.observation_space.shape[0],
              observation_height=env.observation_space.shape[1],
              observation_depth=env.observation_space.shape[2],
              filters_per_layer=np.array([32, 64, 64]),
              restore=False,
              output_graph=False)
RL = Agent(
    brain=Brain,
    n_actions=env.action_space.n,
    observation_space_shape=env.observation_space.shape,
    reward_decay=0.99,
    MAX_EPSILON=1,  # epsilon 的最大值
    MIN_EPSILON=0.1,  # epsilon 的最小值
    replace_target_iter=10000,
    memory_size=1000000,
    batch_size=32,
)


def Compress(screens):
    s = []
    for i in range(4):
        s.append(np.reshape(np.fromstring(blosc.decompress(screens[i]), dtype=np.uint8), (84, 84, 1)))

    return s


total_steps = 0


for i_episode in range(10000):

    observation = env.reset()
    ep_r = 0
    totalR = 0
    while True:
        # env.render()

        action = RL.choose_action(observation)

        observation_, env_reward, done, info = env.step(action)

        # the smaller theta and closer to center the better

        totalR += env_reward
        RL.store_memory(observation, action, env_reward, observation_, done)

        if total_steps > 5000:
            RL.learn()
        if done:
            print('episode: ', i_episode,
                  ' epsilon: ', round(RL.epsilon, 2),
                  'total_reward:', totalR)
            break

        observation = observation_
        total_steps += 1

Brain.save()