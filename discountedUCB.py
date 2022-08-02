import math

from bandit2 import BanditTwoArmedHighLowFixed
import numpy as np
from random import *
from sklearn.preprocessing import minmax_scale
#win_ISD = {n+1: {'a_isd':round(uniform(3,10),3),'com_isd':round(uniform(10,100)/100,3)} for n in range(10)}
#arm_count = len(win_ISD)
# x = np.zeros(arm_count)
# U = np.zeros(arm_count)
# count = np.zeros(arm_count)

def discounted_UCB(win_ISD,gamma):

    total_rounds = 500
    arm_count = len(win_ISD)
    count = np.zeros(arm_count)
    arm_reward = win_ISD
    sum_rewards = np.zeros(arm_count)
    Q = np.zeros(arm_count)
    x = np.zeros(arm_count)
    U = np.zeros(arm_count) #
    P = np.zeros(arm_count) # 처리시간
    Oreward = np.zeros(arm_count)
    Oreward_sum = np.zeros(arm_count)
    #arm = np.zeros(total_rounds)

    T = np.zeros(arm_count)  # 1 bit당 전체 코스트
    T_L = [1 / round(uniform(0.5,1),3) for n in range(arm_count)]
    p_tr = [round(uniform(0.5,1),3) for n in range(arm_count)]
    lambda_k = 0.1 # 모든 가중치
    alpha = 1


    tau = [randint(1,20) for n in range(total_rounds)]  # task 완료시간
    epsilon = [randint(1,10) for n in range(total_rounds)]  # 에너지 소비
    L = [round(uniform(1,15),3) for n in range(total_rounds)] # data 길이

    env = BanditTwoArmedHighLowFixed(arm_reward, arm_count)
    arm_t = 0
    for i in range(total_rounds):

        ucb = np.zeros(arm_count)
        if i < arm_count:
            arm = i

        else:
            for j in range(arm_count):
                ucb[j] = x[j] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[j])
                #ucb[j] = Q[j] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[j])
            arm = np.argmax(ucb)

        #arm = UCB(i, arm_count, x, count)
        next_state, reward, done, info = env.step(arm)
        count[arm] += 1
        Oreward_sum[arm] += reward
        Oreward[arm] = Oreward_sum[arm] / count[arm]
        # sum_rewards[arm] += reward
        # Q[arm] = sum_rewards[arm] / count[arm]
        P[arm] = math.pow(gamma, total_rounds - i) * ((tau[i] + (lambda_k * epsilon[i])) / L[i])
        #P[arm] = gamma * ((tau[i] + (lambda_k * epsilon[i])) / L[i])
        sum_rewards[arm] += P[arm]
        Q[arm] = sum_rewards[arm] / count[arm]
        T[arm] = (1 + lambda_k * p_tr[arm]) * T_L[arm]
        if arm != arm_t or i == 0:
            switching = 1
        else:
            switching = 0
        U[arm] = L[i] * T[arm] + L[i] * Q[arm] + alpha * switching
        x[arm] = 22 - U[arm]
        x = minmax_scale(x)
        arm_t = arm
    # opt_arm = np.argmax(x)
    # for index, (key, elem) in enumerate(win_ISD.items()):
    #     if opt_arm == index:
    #         opt_arm = key
    #         break
    #return Oreward
    return x
# def UCB(i,arm_count,x_t,count):
#     ucb = np.zeros(arm_count)
#     if i < arm_count:
#         return i
#     else:
#         for arm in range(arm_count):
#             ucb[arm] = x_t[arm] + 44 * np.sqrt((0.6 * np.log(sum(count))) / count[arm])
#
#     return np.argmax(ucb)
# opt_arm = discounted_UCB(win_ISD,0.99)
# print(win_ISD)
# print(x,opt_arm)
# print(count)
