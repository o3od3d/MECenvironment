import math

from bandit2 import BanditTwoArmedHighLowFixed
import numpy as np
from random import *
from sklearn.preprocessing import minmax_scale

class DUCB():
    def __init__(self,NumberOfIoT,totalRound):
        print("DUCB bandit start")
        self.total_rounds = 50
        self.count = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)
        self.sum_rewards = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)
        self.Q = {i: 0 for i in range(NumberOfIoT)}  # np.zeros(NumberOfIoT)

        self.T = 50
        self.t_0 = {i: 0.0001 for i in range(NumberOfIoT)}
        self.mu_0 = {i: 1 for i in range(NumberOfIoT)}
        successRate = np.zeros(totalRound)
        arm2 = 0
        numberOfSuccess = 0
        regretUpdate = np.zeros(totalRound)

        self.x = np.zeros(NumberOfIoT)
        self.U = np.zeros(NumberOfIoT)  #
        self.P = np.zeros(NumberOfIoT)  # 처리시간
        self.Oreward = np.zeros(NumberOfIoT)
        self.Oreward_sum = np.zeros(NumberOfIoT)
        # arm = np.zeros(total_rounds)

        self.T = np.zeros(NumberOfIoT)  # 1 bit당 전체 코스트
        self.T_L = [1 / round(uniform(0.5, 1), 3) for n in range(NumberOfIoT)]
        self.p_tr = [round(uniform(0.5, 1), 3) for n in range(NumberOfIoT)]


        self.tau = [randint(1, 20) for n in range(self.total_rounds)]  # task 완료시간
        self.epsilon = [randint(1, 10) for n in range(self.total_rounds)]  # 에너지 소비
        self.L = [round(uniform(1, 15), 3) for n in range(self.total_rounds)]  # data 길이
    def discounted_UCB(self,win_ISD,gamma):

        arm_count = win_ISD.keys()
        arm_reward = win_ISD

        lambda_k = 0.1  # 모든 가중치
        alpha = 1
        x = self.preprocessing(win_ISD)
        env = BanditTwoArmedHighLowFixed(arm_reward, arm_count)
        arm_t = 0
        for i in range(self.total_rounds):

            # ucb = np.zeros(arm_count)
            # if i < arm_count:
            #     arm = i
            #
            # else:
            #     for j in range(arm_count):
            #         ucb[j] = x[j] + 44 * np.sqrt((0.6 * np.log(sum(self.count))) / self.count[j])
            #         #ucb[j] = Q[j] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[j])
            #     arm = np.argmax(ucb)

            arm = self.UCB(i, list(arm_count), x, self.count)

            j = 0
            for k in list(arm_count):
                if k == arm:
                    next_state, reward, done, info = env.step(j)
                    break
                j += 1

            self.count[arm] += 1
            self.Oreward_sum[arm] += reward
            self.Oreward[arm] = self.Oreward_sum[arm] / self.count[arm]
            # sum_rewards[arm] += reward
            # Q[arm] = sum_rewards[arm] / count[arm]
            self.P[arm] = math.pow(gamma, self.total_rounds - i) * ((self.tau[i] + (lambda_k * self.epsilon[i])) / self.L[i])
            #P[arm] = gamma * ((tau[i] + (lambda_k * epsilon[i])) / L[i])
            self.sum_rewards[arm] += self.P[arm]
            self.Q[arm] = self.sum_rewards[arm] / self.count[arm]
            self.T[arm] = (1 + lambda_k * self.p_tr[arm]) * self.T_L[arm]
            if arm != arm_t or i == 0:
                switching = 1
            else:
                switching = 0
            self.U[arm] = self.L[i] * self.T[arm] + self.L[i] * self.Q[arm] + alpha * switching
            x[arm] = 22 - self.U[arm]
            # 정규화
            temp_x = []
            for index, (key,value) in enumerate(x.items()):
                temp_x.append(value)
            temp_x = minmax_scale(temp_x)
            for index, (key,value) in enumerate(x.items()):
                x[key] = temp_x[index]
            arm_t = arm
            self.postprocessing(win_ISD,x)
        # opt_arm = np.argmax(x)
        # for index, (key, elem) in enumerate(win_ISD.items()):
        #     if opt_arm == index:
        #         opt_arm = key
        #         break
        #return Oreward
        return x
    def preprocessing(self,win_ISD):
        Q = dict()
        # t_0 = dict()
        # mu_0 = dict()
        for key, value in list(win_ISD.items()):
            Q[key] = self.x[key]

        return Q

    def postprocessing(self,win_ISD,x):
        for key,value in list(win_ISD.items()):
            self.x[key] = (self.x[key] + x[key]) / 2

    def UCB(self,i,arm_count,x_t,count):
        #ucb = np.zeros(arm_count)
        if i < len(arm_count):
            return arm_count[i]
        else:
            ucb = {arm: x_t[arm] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[arm]) for arm in list(arm_count)}
            # for arm in range(arm_count):
            #     ucb[arm] = x_t[arm] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[arm])

        return max(ucb, key=ucb.get)
    # opt_arm = discounted_UCB(win_ISD,0.99)
    # print(win_ISD)
    # print(x,opt_arm)
    # print(count)
