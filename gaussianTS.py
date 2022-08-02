from bandit2 import BanditTwoArmedHighLowFixed
import numpy as np
#env = BanditTwoArmedHighLowFixed()

def gaussianTS(win_ISD,gamma):

    arm_count = len(win_ISD)
    count = np.zeros(arm_count)
    sum_rewards = np.zeros(arm_count)
    rewards = np.zeros(arm_count)
    Q = np.zeros(arm_count)
    arm_reward = win_ISD
    t_0 = [0.0001 for n in range(arm_count)]
    mu_0 = [1 for n in range(arm_count)]
    num_rounds = 350
    total_rounds = 100
    arm = 0
    env = BanditTwoArmedHighLowFixed(arm_reward, arm_count)
    for i in range(num_rounds):
        arm,Q = thompson_sampling(t_0,mu_0,arm_count)
        next_state, reward, done, info = env.step(arm)
        mu_0[arm] = ((t_0[arm] * mu_0[arm]) + (count[arm] * rewards[arm])) / (t_0[arm] + count[arm])
        t_0[arm] += 1
        count[arm] += 1
        sum_rewards[arm] += reward
        rewards[arm] = sum_rewards[arm] / count[arm]
    # print(count)
    # print(Q)
    # print(rewards)
    return rewards

def thompson_sampling(t_0,mu_0,arm_count):
    a = np.zeros(arm_count)
    for arm in range(arm_count):
        a[arm] = (np.random.rand() / np.sqrt(t_0[arm])) + mu_0[arm]
    #samples = [np.random.beta(alpha[i]+1, beta[i]+1) for i in range(10)]
    return np.argmax(a), a #np.argmax(samples),samples






