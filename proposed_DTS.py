import numpy as np
from bandit2 import BanditTwoArmedHighLowFixed

def proposed_DTS(win_ISD,gamma):
    total_rounds = 500
    arm_count = len(win_ISD)
    arm2 = np.zeros(arm_count)
    count = np.zeros(arm_count)
    sum_rewards = np.zeros(arm_count)
    Q = np.zeros(arm_count)
    alpha = np.ones(arm_count)
    beta = np.ones(arm_count)
    samples = np.zeros(arm_count)
    maximum = np.zeros(arm_count)
    ucb = np.zeros(arm_count)
    arm_reward = win_ISD
    x = np.zeros(total_rounds)
    y = np.zeros(total_rounds)
    T = 50
    successRate = np.zeros(total_rounds)
    arm2 = 0
    numberOfSuccess = 0
    regretUpdate = np.zeros(total_rounds)


    env = BanditTwoArmedHighLowFixed(arm_reward, arm_count)

    #gamma = gamma * 0.99
    for i in range(total_rounds):
        arm2 = thompson_sampling(alpha, beta,maximum,arm_count)
        x = arm2[0]
        arm = UCB(i, T, arm2,count,arm_count)

        next_state, reward, done, info = env.step(arm)
        count[arm] += 1
        sum_rewards[arm] += reward
        Q[arm] = sum_rewards[arm] / count[arm]
        if reward == 1:
            alpha[arm] = gamma * alpha[arm] + 1
        else:
            beta[arm] = gamma * beta[arm] + 1


    opt_arm = np.argmax(Q)
    for index, (key, elem) in enumerate(win_ISD.items()):
        if opt_arm == index:
            opt_arm = key
            break
    return Q

def UCB(i,T,samples,count,arm_count):
    if i < arm_count:
        return i
    else:
        T = T * 0.99
        denom = sum([np.exp(j) for j in count])
        probs = [np.exp(j) / denom for j in count]
        ucb = [(samples[arm] - probs[arm]) for arm in range(arm_count)]

    return np.argmax(ucb)

def thompson_sampling(alpha, beta,maximum,arm_count):
    samples = [np.random.beta(alpha[i]+1, beta[i]+1) for i in range(arm_count)]
    maximum[np.argmax(samples)] += 1
    return samples