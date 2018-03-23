# -*- coding: UTF-8 -*-
"""
by Howard
using:
- python: 3.6
"""


def cleanstring(string):
    return string.replace(".", "").replace("^", "").replace("-", "").replace(" ", "_")


def mkdir(path):
    import os
    path = path.strip()  # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
    else:
        print(path + ' 目录已存在')


def data_save(algorithm_name, env_name, Brain, Agent):
    import datetime
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    SETUP = cleanstring(nowTime) + '|' + env_name + "|algorithm:" + algorithm_name + "|neurons_per_layer:" + str(Brain.neurons_per_layer) + \
        "|learning_rate:" + str(Brain.lr) + "|reward_decay:" + str(Agent.gamma) + \
        "|replace_target_iter:" + str(Agent.replace_target_iter) + "|memory_size:" + \
        str(Agent.memory_size) + "|batch_size:" + str(Agent.batch_size) + "|MAX_EPSILON:" + \
        str(Agent.MAX_EPSILON) + "|MIN_EPSILON:" + str(Agent.MIN_EPSILON) + "|LAMBDA:" + str(Agent.LAMBDA)

    outStr = "Experiment_SETUP:\"" + SETUP + "\""
    outStr += "\nimport pylab\n"
    # rewards
    outStr += "\nRewards = " + str(Agent.rewards) + "\n"
    # cost_his
    outStr += "\ncost_his = " + str(Agent.cost_his) + "\n"
    # q value
    if hasattr(Agent, 'q_change_list'):
        outStr += "\nq_change_list = " + str(Agent.q_change_list) + "\n"

    path = env_name + algorithm_name + "_data"
    mkdir(path)
    f = open(path + "/" + SETUP + ".py", "w")
    f.write(outStr)
    f.close()

    print("\nsave to ", path, "successful!")


def plot(title, datas, data_labels, ylabel):
    import matplotlib.pyplot as plt
    for data, data_label in zip(datas, data_labels):
        plt.plot(range(len(data)), data, label=data_label)

    plt.legend(loc='best')
    plt.xlabel('episode')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.show()


if __name__ == '__main__':

    Rewards_1 = [18.0, 21.0, 51.0, 20.0, 14.0, 31.0, 20.0, 18.0, 26.0, 22.0, 19.0, 24.0, 11.0, 46.0, 22.0, 14.0, 28.0, 15.0, 14.0, 11.0, 18.0, 10.0, 24.0, 17.0, 15.0, 12.0, 29.0, 12.0, 29.0, 19.0, 25.0, 16.0, 13.0, 22.0, 30.0, 22.0, 10.0, 13.0, 14.0, 16.0, 13.0, 18.0, 24.0, 13.0, 29.0, 17.0, 17.0, 12.0, 21.0, 13.0, 28.0, 14.0, 14.0, 14.0, 16.0, 16.0, 13.0, 18.0, 18.0, 16.0, 14.0, 23.0, 13.0, 10.0, 9.0, 22.0, 12.0, 25.0, 13.0, 10.0, 19.0, 33.0, 10.0, 14.0, 11.0, 33.0, 22.0, 24.0, 13.0, 18.0, 15.0, 22.0, 35.0, 22.0, 14.0, 29.0, 12.0, 12.0, 13.0, 16.0, 14.0, 24.0, 14.0, 16.0, 9.0, 13.0, 22.0, 13.0, 15.0, 18.0, 19.0, 22.0, 18.0, 11.0, 9.0, 10.0, 54.0, 32.0, 12.0, 20.0, 36.0, 25.0, 15.0, 15.0, 10.0, 14.0, 29.0, 21.0, 13.0, 26.0, 15.0, 25.0, 32.0, 9.0, 13.0, 24.0, 27.0, 14.0, 19.0, 19.0, 19.0, 19.0, 18.0, 17.0, 28.0, 11.0, 14.0, 10.0, 15.0, 29.0, 12.0, 19.0, 12.0, 15.0, 24.0, 14.0, 26.0, 14.0, 16.0, 13.0, 16.0, 29.0, 27.0, 21.0, 15.0, 17.0, 22.0, 9.0, 16.0, 25.0, 11.0, 13.0, 17.0, 17.0, 16.0, 12.0, 15.0, 22.0, 18.0, 12.0, 15.0, 14.0, 25.0, 18.0, 20.0, 17.0, 44.0, 13.0, 10.0, 14.0, 16.0, 30.0, 24.0, 15.0, 14.0, 45.0, 29.0, 18.0, 30.0, 21.0, 40.0, 25.0, 13.0, 11.0, 24.0, 11.0, 12.0, 34.0, 23.0, 57.0, 9.0, 18.0, 18.0, 14.0, 21.0, 20.0, 14.0, 39.0, 39.0, 26.0, 39.0, 111.0, 18.0, 15.0, 131.0, 128.0, 54.0, 26.0, 57.0, 12.0, 64.0, 19.0, 20.0, 12.0, 12.0, 22.0, 39.0, 18.0, 19.0, 63.0, 59.0, 90.0, 34.0, 44.0, 43.0, 49.0, 94.0, 54.0, 94.0, 65.0, 68.0, 121.0, 14.0, 83.0, 18.0, 87.0, 76.0, 113.0, 73.0, 18.0, 102.0, 114.0, 126.0, 30.0, 127.0, 87.0, 80.0, 111.0, 116.0, 181.0, 194.0, 46.0, 138.0, 159.0, 168.0, 44.0, 111.0, 114.0, 209.0, 181.0, 133.0, 88.0, 146.0, 153.0, 110.0, 207.0, 173.0, 200.0, 142.0, 144.0, 183.0, 103.0, 197.0, 140.0, 194.0, 227.0, 199.0, 199.0, 186.0, 204.0, 168.0, 197.0, 158.0, 192.0, 190.0, 191.0, 193.0, 14.0, 206.0, 181.0, 183.0, 141.0, 158.0, 227.0, 174.0, 190.0, 168.0, 180.0, 218.0, 200.0, 184.0, 174.0, 218.0, 186.0, 185.0, 183.0, 182.0, 172.0,
                 171.0, 232.0, 183.0, 204.0, 176.0, 183.0, 205.0, 156.0, 171.0, 155.0, 171.0, 183.0, 197.0, 180.0, 174.0, 207.0, 168.0, 235.0, 232.0, 206.0, 192.0, 200.0, 169.0, 166.0, 168.0, 166.0, 183.0, 176.0, 168.0, 197.0, 193.0, 204.0, 181.0, 189.0, 158.0, 199.0, 181.0, 186.0, 159.0, 169.0, 182.0, 174.0, 163.0, 158.0, 195.0, 177.0, 168.0, 167.0, 164.0, 157.0, 156.0, 175.0, 159.0, 146.0, 160.0, 194.0, 170.0, 161.0, 167.0, 168.0, 166.0, 170.0, 183.0, 160.0, 171.0, 161.0, 172.0, 166.0, 159.0, 163.0, 169.0, 154.0, 180.0, 176.0, 158.0, 168.0, 155.0, 177.0, 174.0, 174.0, 171.0, 159.0, 179.0, 162.0, 175.0, 184.0, 157.0, 186.0, 176.0, 166.0, 166.0, 166.0, 169.0, 157.0, 156.0, 173.0, 166.0, 178.0, 157.0, 161.0, 170.0, 144.0, 148.0, 158.0, 168.0, 162.0, 151.0, 163.0, 156.0, 157.0, 161.0, 167.0, 157.0, 160.0, 164.0, 180.0, 167.0, 171.0, 172.0, 161.0, 181.0, 175.0, 173.0, 173.0, 173.0, 197.0, 147.0, 168.0, 164.0, 155.0, 175.0, 181.0, 173.0, 196.0, 172.0, 167.0, 171.0, 181.0, 185.0, 180.0, 179.0, 177.0, 169.0, 167.0, 163.0, 164.0, 207.0, 169.0, 177.0, 181.0, 172.0, 165.0, 171.0, 173.0, 166.0, 171.0, 170.0, 166.0, 152.0, 170.0, 153.0, 154.0, 159.0, 177.0, 163.0, 162.0, 174.0, 186.0, 155.0, 148.0, 160.0, 165.0, 170.0, 173.0, 168.0, 163.0, 168.0, 157.0, 151.0, 159.0, 169.0, 157.0, 179.0, 171.0, 171.0, 204.0, 163.0, 165.0, 149.0, 159.0, 165.0, 173.0, 156.0, 161.0, 160.0, 188.0, 170.0, 162.0, 156.0, 148.0, 173.0, 154.0, 153.0, 167.0, 159.0, 167.0, 157.0, 154.0, 173.0, 154.0, 145.0, 147.0, 153.0, 153.0, 143.0, 158.0, 158.0, 172.0, 158.0, 156.0, 147.0, 158.0, 144.0, 150.0, 168.0, 163.0, 150.0, 154.0, 155.0, 136.0, 145.0, 154.0, 156.0, 170.0, 147.0, 159.0, 144.0, 159.0, 159.0, 149.0, 169.0, 158.0, 147.0, 163.0, 157.0, 152.0, 161.0, 151.0, 152.0, 145.0, 147.0, 143.0, 149.0, 139.0, 165.0, 149.0, 146.0, 144.0, 182.0, 145.0, 156.0, 156.0, 172.0, 156.0, 146.0, 151.0, 156.0, 150.0, 158.0, 155.0, 165.0, 153.0, 168.0, 165.0, 159.0, 509.0, 160.0, 427.0, 158.0, 154.0, 170.0, 158.0]

    Rewards_2 = [29.0, 15.0, 17.0, 14.0, 15.0, 10.0, 26.0, 17.0, 13.0, 21.0, 12.0, 25.0, 18.0, 41.0, 25.0, 30.0, 10.0, 11.0, 41.0, 27.0, 35.0, 34.0, 37.0, 12.0, 43.0, 13.0, 20.0, 46.0, 23.0, 20.0, 14.0, 21.0, 24.0, 33.0, 10.0, 42.0, 16.0, 21.0, 45.0, 31.0, 26.0, 24.0, 18.0, 17.0, 71.0, 30.0, 23.0, 39.0, 27.0, 19.0, 17.0, 45.0, 14.0, 25.0, 17.0, 13.0, 29.0, 24.0, 46.0, 13.0, 40.0, 14.0, 12.0, 30.0, 49.0, 32.0, 21.0, 23.0, 14.0, 32.0, 24.0, 13.0, 26.0, 34.0, 92.0, 54.0, 32.0, 13.0, 15.0, 27.0, 27.0, 49.0, 66.0, 27.0, 20.0, 41.0, 41.0, 33.0, 91.0, 49.0, 47.0, 64.0, 13.0, 36.0, 12.0, 43.0, 25.0, 20.0, 21.0, 45.0, 43.0, 23.0, 47.0, 33.0, 33.0, 34.0, 59.0, 59.0, 13.0, 16.0, 46.0, 17.0, 19.0, 67.0, 23.0, 49.0, 24.0, 104.0, 38.0, 53.0, 35.0, 20.0, 60.0, 66.0, 19.0, 25.0, 33.0, 32.0, 43.0, 24.0, 48.0, 59.0, 25.0, 42.0, 18.0, 35.0, 41.0, 29.0, 19.0, 40.0, 53.0, 12.0, 18.0, 45.0, 25.0, 50.0, 10.0, 20.0, 48.0, 33.0, 13.0, 17.0, 43.0, 77.0, 36.0, 47.0, 52.0, 33.0, 38.0, 16.0, 50.0, 146.0, 37.0, 23.0, 54.0, 51.0, 48.0, 58.0, 19.0, 26.0, 33.0, 97.0, 22.0, 72.0, 67.0, 69.0, 71.0, 51.0, 19.0, 57.0, 70.0, 25.0, 82.0, 140.0, 91.0, 69.0, 13.0, 72.0, 65.0, 86.0, 150.0, 76.0, 75.0, 78.0, 218.0, 83.0, 119.0, 95.0, 141.0, 58.0, 78.0, 88.0, 119.0, 172.0, 101.0, 182.0, 167.0, 133.0, 175.0, 128.0, 104.0, 251.0, 151.0, 215.0, 163.0, 161.0, 144.0, 209.0, 168.0, 163.0, 173.0, 185.0, 187.0, 166.0, 150.0, 172.0, 184.0, 200.0, 161.0, 230.0, 186.0, 170.0, 204.0, 162.0, 170.0, 156.0, 165.0, 199.0, 166.0, 171.0, 170.0, 137.0, 188.0, 169.0, 162.0, 162.0, 200.0, 174.0, 167.0, 162.0, 150.0, 154.0, 164.0, 183.0, 179.0, 180.0, 152.0, 159.0, 200.0, 191.0, 241.0, 168.0, 149.0, 171.0, 190.0, 178.0, 158.0, 168.0, 170.0, 170.0, 162.0, 169.0, 175.0, 187.0, 190.0, 175.0, 157.0, 165.0, 158.0, 162.0, 162.0, 159.0, 173.0, 185.0, 167.0, 186.0, 203.0, 166.0, 155.0, 188.0, 170.0, 189.0, 165.0, 158.0, 181.0, 174.0, 161.0, 174.0, 158.0, 167.0, 167.0, 148.0, 153.0, 172.0, 160.0, 161.0, 152.0, 159.0, 184.0, 174.0, 167.0, 150.0, 184.0,
                 167.0, 166.0, 162.0, 162.0, 165.0, 155.0, 198.0, 174.0, 176.0, 170.0, 171.0, 194.0, 144.0, 165.0, 151.0, 155.0, 167.0, 171.0, 160.0, 156.0, 176.0, 153.0, 187.0, 181.0, 170.0, 175.0, 166.0, 150.0, 151.0, 147.0, 146.0, 165.0, 163.0, 156.0, 172.0, 185.0, 186.0, 162.0, 173.0, 152.0, 187.0, 171.0, 182.0, 150.0, 166.0, 175.0, 175.0, 159.0, 155.0, 184.0, 171.0, 159.0, 173.0, 160.0, 154.0, 160.0, 175.0, 166.0, 154.0, 160.0, 197.0, 172.0, 163.0, 164.0, 171.0, 170.0, 174.0, 197.0, 168.0, 180.0, 172.0, 183.0, 164.0, 157.0, 164.0, 167.0, 153.0, 187.0, 178.0, 163.0, 171.0, 154.0, 185.0, 177.0, 175.0, 176.0, 158.0, 181.0, 164.0, 166.0, 185.0, 152.0, 176.0, 172.0, 165.0, 159.0, 159.0, 166.0, 164.0, 161.0, 177.0, 172.0, 194.0, 168.0, 177.0, 185.0, 156.0, 162.0, 180.0, 200.0, 187.0, 164.0, 184.0, 170.0, 165.0, 170.0, 170.0, 160.0, 166.0, 171.0, 200.0, 166.0, 179.0, 184.0, 169.0, 190.0, 174.0, 179.0, 172.0, 172.0, 192.0, 149.0, 171.0, 162.0, 146.0, 169.0, 172.0, 166.0, 187.0, 167.0, 158.0, 170.0, 174.0, 174.0, 174.0, 175.0, 176.0, 170.0, 164.0, 157.0, 156.0, 190.0, 162.0, 161.0, 180.0, 171.0, 164.0, 172.0, 183.0, 168.0, 169.0, 166.0, 167.0, 154.0, 170.0, 154.0, 157.0, 161.0, 185.0, 161.0, 163.0, 182.0, 186.0, 155.0, 153.0, 160.0, 171.0, 172.0, 185.0, 178.0, 162.0, 172.0, 158.0, 148.0, 156.0, 170.0, 155.0, 191.0, 177.0, 178.0, 213.0, 170.0, 172.0, 151.0, 166.0, 181.0, 193.0, 158.0, 162.0, 166.0, 206.0, 175.0, 166.0, 158.0, 155.0, 183.0, 164.0, 156.0, 172.0, 157.0, 172.0, 170.0, 158.0, 188.0, 163.0, 153.0, 158.0, 158.0, 161.0, 147.0, 176.0, 172.0, 184.0, 168.0, 170.0, 160.0, 174.0, 155.0, 160.0, 185.0, 175.0, 160.0, 165.0, 158.0, 143.0, 148.0, 158.0, 158.0, 162.0, 154.0, 164.0, 148.0, 176.0, 167.0, 156.0, 178.0, 166.0, 159.0, 162.0, 176.0, 171.0, 183.0, 170.0, 161.0, 160.0, 159.0, 150.0, 153.0, 152.0, 181.0, 157.0, 151.0, 156.0, 207.0, 155.0, 172.0, 171.0, 186.0, 166.0, 156.0, 156.0, 170.0, 159.0, 157.0, 175.0, 176.0, 158.0, 186.0, 160.0, 164.0, 165.0, 171.0, 168.0, 162.0, 162.0, 188.0, 164.0]

    datas = [Rewards_1, Rewards_2]
    data_labels = ['dqn', 'ddqn']
    ylabel = 'reward'
    plot("title", datas, data_labels, ylabel)

    cost_his = [0.53036535, 0.34001577, 0.22790347, 0.14961621, 0.13484702, 0.11350937, 0.074557506, 0.033830196, 0.018705487, 0.020254992, 0.02121841, 0.010574605, 0.010100246, 0.0033154581, 0.0021279198, 0.0033396168, 0.0089815836, 0.0066626286, 0.0081631029, 0.014952227, 0.018440746, 0.011900799, 0.013223919, 0.015099897, 0.0029108108, 0.007184586, 0.0090703629, 0.0088107157, 0.0043517519, 0.013393433, 0.015788084, 0.019993395, 0.011740174, 0.0063485876, 0.0077639855, 0.02220396, 0.43722248, 0.060020488, 0.030263238, 0.068949223, 0.15957479, 0.0062239175, 0.044006057, 0.022784602, 0.021094875, 0.027156251, 0.029698811, 0.028612124, 0.021787122, 0.01088878, 0.047502533, 0.03762015, 0.024659064, 0.011497336, 0.025964301, 0.02579047, 0.005634658, 0.0060201995, 0.025036044, 0.040497649, 0.030815996, 0.001780699, 0.0091668442, 0.0099193882, 0.060824562, 0.038230497, 0.054914303, 0.02479781, 0.017084822, 0.095608965, 0.023363873, 0.026432196, 0.028517969, 0.0021661529, 0.022984559, 0.016325474, 0.022721546, 0.021310389, 0.010903371, 0.044917405, 0.0046370137, 0.034164436, 0.050340895, 0.031738222, 0.039011918, 0.81371504, 0.13315229, 0.075618654, 0.014429256, 0.066880189, 0.063857511, 0.07621447, 0.058307894, 0.19919848, 0.044883247, 0.1029273, 0.086370721, 0.24465689, 0.083963558, 0.023503779, 0.0098326132, 0.015656851, 0.12458228, 0.081945896, 0.058387391, 0.039572898, 0.042057257, 0.13542929, 0.090012848, 0.070126384, 0.072040968, 0.22253136, 0.011401746, 0.065439083, 0.026262652, 0.059859358, 0.021376986, 0.085592791, 0.14431952, 0.10938206, 0.028511599, 0.38084581, 0.038953517, 0.096117526, 0.1233334, 0.3041614, 0.25633019, 0.1168144, 0.068519369, 0.18198597, 0.020620098, 0.033849936, 0.026859768, 0.022037171, 0.13061509, 0.0087917279, 0.044630788, 0.028233709, 0.03795632, 0.024718437, 0.0089555243, 0.10324511, 0.019591417, 0.077117816, 0.33976528, 0.11374084, 0.10290372, 0.035343047, 0.2492778, 0.012074696, 0.11408786, 0.012099594, 0.029277485, 0.04297572, 0.038824633, 0.084925815, 0.099164605, 0.13419777, 0.027046364, 0.14663406, 0.025591623, 0.19474426, 0.0068946504, 0.043428026, 0.16607231, 0.026535179, 0.045626163, 0.89134347, 0.073081233, 0.17539163, 0.48055887, 0.016936772, 0.30584353, 0.057324126, 0.015105134, 0.23077872, 0.12806326, 0.038398586, 0.44079599, 0.2849496, 0.069502428, 0.11373247, 0.039843436, 0.17389889, 0.058143776, 0.027503863, 0.080415159, 0.03957158, 0.071064815, 0.40288782, 0.024868993, 0.64174753, 0.026721673, 0.033875395, 0.05365286, 0.20596209, 0.17576566, 0.051089127, 0.043693341, 0.097464778, 0.061829869, 0.073561206, 0.034743633, 0.063187666, 0.572061, 0.037427738, 0.55789125, 0.029402394, 0.050114773, 0.348896, 0.073023677, 0.0222628, 0.025771905, 0.057147168, 0.14816782, 0.64413488, 0.075046912, 0.56358558, 1.2106405, 0.056696262, 0.046089463, 2.426018, 0.065896302, 0.048352346, 0.083230235, 1.2460239, 0.10858773, 2.5180101, 0.04559179, 1.406425, 0.12033448, 2.1467094, 0.052027021, 1.7105479, 0.07274536, 0.050041988, 0.061526217, 1.8145511, 0.20651734, 0.047748607, 0.041109014, 0.035196111, 0.047840178, 0.084341303, 0.028552517, 0.070959426, 0.083878107, 0.089118063, 0.1631867, 0.056710914, 0.030283336, 0.051298458, 2.7837245, 0.048254497, 0.047680333, 0.098891407, 0.1010572, 0.03771257, 0.044124007, 0.12098639, 0.062624484, 0.038762614, 1.3908277, 0.14733195, 0.056504242, 0.056139071, 0.30142716, 0.079203136, 0.057406358, 0.180236, 0.03578895, 0.16710994, 0.33975846, 0.062854186, 0.065354668, 0.050621741, 0.090883732, 0.046608862, 0.073631309, 0.093885086, 0.097678781, 0.15327895, 0.19564098, 0.13209628, 0.064646572, 0.1723648, 0.033531725, 0.8261553, 0.039874595, 0.21791688, 0.086268447, 0.073398821, 0.025288988, 0.066446751, 0.11492684, 0.059888035, 0.056040309, 0.036940001, 0.071522124,
                0.10049807, 0.20228302, 0.14419354, 0.032921128, 0.60965025, 0.045170434, 0.12260561, 0.76107121, 1.8113407, 0.072475508, 0.11232759, 0.22627774, 0.049510941, 0.040959362, 0.69630367, 0.55233264, 0.053961538, 0.08525034, 0.50614029, 0.017320104, 0.11008172, 0.092700467, 0.077417433, 0.61975414, 0.030197795, 0.27044791, 0.038856417, 0.10338859, 0.36790201, 0.017781302, 0.031788506, 0.22921634, 0.027701611, 0.027940024, 0.028550025, 0.037838705, 0.030507304, 0.066867597, 0.10808733, 0.039466169, 0.0237859, 0.38766745, 0.021948038, 0.069194034, 0.90903914, 0.065860324, 0.10024051, 0.028208204, 0.057999693, 0.15849096, 0.035605222, 1.641519, 0.023875386, 0.017033523, 0.061665893, 0.089909993, 0.23257947, 0.042574391, 0.035200112, 0.045686834, 0.078084946, 0.037127852, 0.080083475, 0.095543079, 0.16131656, 0.15936887, 0.99662387, 0.1977533, 0.10584722, 0.14980508, 1.3216892, 0.35193086, 0.22831534, 0.023776397, 0.071450353, 0.25877169, 0.16798985, 0.10851559, 0.022115616, 0.2465668, 0.044281185, 0.023713913, 0.26362959, 0.024774253, 0.010778687, 0.023125105, 0.040659267, 0.28169796, 0.063486755, 0.014190727, 0.079521149, 0.014042474, 0.064804971, 0.050381038, 0.36966747, 0.16861606, 0.016233318, 0.23432505, 0.053237151, 0.028114421, 0.030597158, 0.11041483, 0.02210002, 0.025327716, 0.12668763, 0.058395967, 0.032319669, 0.13954669, 0.047905974, 0.08599516, 0.03473435, 0.041125253, 6.0995617, 0.0283488, 1.0054884, 0.13710576, 0.019297864, 0.085130833, 0.019245801, 0.054467343, 0.023963045, 0.11028466, 0.029881604, 0.065753981, 0.12066986, 0.11401121, 0.044660158, 0.14433907, 0.028431352, 0.014410682, 0.018580083, 0.042306453, 0.12604962, 0.11736712, 0.020924903, 0.036739532, 0.01874309, 0.12463739, 0.028444666, 0.1801402, 0.0099518569, 0.10427419, 0.021859743, 0.019639261, 0.49158916, 0.019872289, 0.073446184, 0.0290448, 0.039261509, 0.84128135, 0.2477186, 0.034966901, 1.7582314, 0.014580767, 0.10510944, 0.12466834, 0.079173937, 0.041540861, 1.8419335, 0.10802203, 0.15906641, 0.028896231, 0.10999706, 0.23771757, 0.017838469, 0.036951482, 0.18157625, 0.030574694, 0.10933769, 0.064782254, 0.023097362, 0.018856298, 0.021432279, 0.079462118, 0.02103485, 0.073715307, 0.036223259, 0.20606521, 0.043170005, 0.05629354, 0.021601042, 0.39204845, 0.023914687, 0.17785789, 0.078412697, 0.10123944, 0.021096922, 0.18662554, 0.022518869, 0.074331202, 0.011800215, 0.046212282, 0.085676126, 0.083836839, 0.044860788, 0.058527902, 0.079075783, 0.056607261, 0.025912201, 0.14285816, 0.093917064, 0.029874489, 0.030234488, 0.14851019, 0.060886279, 0.012914435, 0.11406076, 0.033716187, 0.036233302, 0.14437619, 0.26577514, 0.13050658, 0.039007239, 0.033226214, 0.047560912, 0.051580049, 0.054466497, 0.078525111, 0.058790985, 0.10955701, 0.012692536, 0.20473488, 0.068305098, 0.036488794, 0.030445797, 0.053577781, 0.082928017, 0.047911372, 0.029680787, 0.094576672, 0.81634474, 0.026044017, 0.085851029, 0.018376183, 0.024158712, 0.042388279, 0.14215255, 0.07561069, 0.025364567, 0.01819062, 0.069883198, 0.013630169, 0.055743054, 0.17447223, 0.018322311, 0.076737612, 0.22258689, 0.082602344, 0.030654024, 0.16451757, 0.087106071, 0.050461084, 0.059370007, 0.049416456, 0.011661669, 0.15782219, 0.071791351, 0.021945488, 0.14256418, 0.060378771, 0.0295012, 0.50387001, 0.021613346, 0.063477859, 0.28846484, 0.019701734, 0.02082343, 0.075395778, 0.18095787, 0.015831459, 0.022579458, 0.011523644, 0.044699565, 0.020276973, 0.3594411, 0.65125465, 0.029350659, 0.034362707, 0.031090409, 0.031041987, 0.013895446, 0.018255401, 0.10316484, 0.040875629, 0.061994646, 0.029887225, 0.029941363, 0.012785424, 0.094824106, 0.41365933, 0.11765406, 0.025556317, 0.077963069, 0.31842741, 0.041601658, 0.05745611, 0.040580481, 0.12006623, 0.015463967, 0.023664638, 0.028323662]

    plot("title", [cost_his], ['dqn'], 'loss')
