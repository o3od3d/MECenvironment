import math

from bandit2 import BanditTwoArmedHighLowFixed
import numpy as np
from random import *
from sklearn.preprocessing import minmax_scale

class DUCB():
    def __init__(self,NumberOfIoT,totalRound):

        self.total_rounds = 50

        self.count = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)
        self.sum_rewards = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)
        self.Q = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)
        self.U = 0.1
        self.C = {i: 0 for i in range(NumberOfIoT)}

         # data 길이
    def discounted_UCB(self,win_ISD,gamma,systemTime,subsystemTime):

        arm_count = win_ISD.keys()
        arm_reward = win_ISD
        #print('UCB의 REWARD',win_ISD)
        C = self.preprocessing(win_ISD)
        env = BanditTwoArmedHighLowFixed(arm_reward, arm_count,1)
        tempTime = 0
        if systemTime == 0:
            tempTime = 0
        else:
            tempTime = systemTime // subsystemTime
            tempTime = tempTime * 10


        for i in range(self.total_rounds):


            arm = self.UCB(i, list(arm_count), C, self.count,systemTime,tempTime)

            j = 0
            for k in list(arm_count):
                if k == arm:
                    next_state, reward, done, info = env.step(j)
                    break
                j += 1
            #print(systemTime,':',reward,'워ㅜ에ㅔ에')
            self.count[arm] += 1
            self.sum_rewards[arm] += reward
            self.Q[arm] = self.sum_rewards[arm] / self.count[arm]

            # 정규화
            # temp_x = []
            # for index, (key,value) in enumerate(x.items()):
            #     temp_x.append(value)
            # temp_x = minmax_scale(temp_x)
            # for index, (key,value) in enumerate(x.items()):
            #     x[key] = temp_x[index]
            # arm_t = arm
            self.postprocessing(win_ISD,C)
            #print('정답',C)
            #print(self.Q)
            C = self.preprocessing(win_ISD)
        # opt_arm = np.argmax(x)
        # for index, (key, elem) in enumerate(win_ISD.items()):
        #     if opt_arm == index:
        #         opt_arm = key
        #         break
        #return Oreward
        return C
    def preprocessing(self,win_ISD):
        Q = dict()
        # t_0 = dict()
        # mu_0 = dict()
        for key, value in list(win_ISD.items()):
            Q[key] = self.Q[key]

        return Q

    def postprocessing(self,win_ISD,x):
        for key,value in list(win_ISD.items()):
            self.Q[key] = (self.Q[key] + x[key]) / 2

    def UCB(self,i,arm_count,x_t,count,systemTime,tempTime):
        #ucb = np.zeros(arm_count)
        if i < len(arm_count):
            return arm_count[i]
        else:
            ucb = {arm: x_t[arm] - (self.U * np.sqrt(np.log(systemTime - tempTime) / count[arm])) for arm in list(arm_count)}
            # for arm in range(arm_count):
            #     ucb[arm] = x_t[arm] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[arm])

        return min(ucb, key=ucb.get)
    # opt_arm = discounted_UCB(win_ISD,0.99)
    # print(win_ISD)
    # print(x,opt_arm)
    # print(count)
