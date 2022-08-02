
import numpy as np
from bandit2 import BanditTwoArmedHighLowFixed


def main_DTS(win_ISD,gamma):
    total_rounds = 500
    arm_count = len(win_ISD)
    alpha = np.ones(arm_count)
    beta = np.ones(arm_count)
    count = np.zeros(arm_count)
    sum_rewards = np.zeros(arm_count)
    Q = np.zeros(arm_count)
    arm_reward = win_ISD
    arm_count = len(win_ISD)
    numberOfSuccess = 0
    regret = np.zeros(total_rounds)



    env = BanditTwoArmedHighLowFixed(arm_reward,arm_count)

    #gamma = gamma * 0.99
    for i in range(total_rounds):
        arm,arm2 = thompson_sampling(alpha,beta,arm_count)
        next_state, reward, done, info = env.step(arm)
        count[arm] += 1
        sum_rewards[arm] += reward
        Q[arm] = sum_rewards[arm] / count[arm]

        if reward == 1:
            alpha[arm] = gamma*alpha[arm] + 1
        else:
            beta[arm] = gamma*beta[arm] + 1
    opt_arm = np.argmax(Q)
    for index, (key, elem) in enumerate(win_ISD.items()):
        if opt_arm == index:
            opt_arm = key
            break
    return Q
def thompson_sampling(alpha, beta,arm_count):
    samples = [np.random.beta(alpha[i]+1, beta[i]+1) for i in range(arm_count)]
    return np.argmax(samples),samples