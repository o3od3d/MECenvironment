from bandit2 import BanditTwoArmedHighLowFixed
import numpy as np
#env = BanditTwoArmedHighLowFixed()

class gaussianTS():
    def __init__(self,NumberOfIoT,totalRound):
        print("gaussian bandit start")
        self.total_rounds = 500
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

    def gaussianTS(self,win_ISD,gamma):

        arm_count = win_ISD.keys()
        #rewards = np.zeros(arm_count)
        arm_reward = win_ISD
        rewards, t_0, mu_0 = self.preprocessing(win_ISD)

        env = BanditTwoArmedHighLowFixed(arm_reward, arm_count)
        for i in range(self.total_rounds):
            arm,Q = self.gauss(t_0,mu_0,arm_count)
            j = 0
            for k in list(arm_count):
                if k == arm:
                    next_state, reward, done, info = env.step(j)
                    break
                j += 1
            #next_state, reward, done, info = env.step(arm)
            mu_0[arm] = ((t_0[arm] * mu_0[arm]) + (self.count[arm] * rewards[arm])) / (t_0[arm] + self.count[arm])
            t_0[arm] += 1
            self.count[arm] += 1
            self.sum_rewards[arm] += reward
            rewards[arm] = self.sum_rewards[arm] / self.count[arm]

        self.postprocessing(win_ISD,rewards,t_0,mu_0)
        rewards,t_0,mu_0 = self.preprocessing(win_ISD)        # print(count)
        # print(Q)
        # print(rewards)
        return rewards

    def preprocessing(self,win_ISD):
        Q = dict()
        t_0 = dict()
        mu_0 = dict()
        for key, value in list(win_ISD.items()):
            Q[key] = self.Q[key]
            t_0[key] = self.t_0[key]
            mu_0[key] = self.mu_0[key]
        return Q,t_0,mu_0

    def postprocessing(self,win_ISD,Q,t_0,mu_0):
        for key,value in list(win_ISD.items()):
            self.Q[key] = (self.Q[key] + Q[key]) / 2
            self.t_0[key] += t_0[key]
            self.mu_0[key] += mu_0[key]

    def gauss(self,t_0,mu_0,arm_count):
        a = {arm: (np.random.rand() / np.sqrt(t_0[arm])) + mu_0[arm]for arm in arm_count}
        # a = np.zeros(len(arm_count))
        # for arm in range(arm_count):
        #     a[arm] = (np.random.rand() / np.sqrt(t_0[arm])) + mu_0[arm]
        #samples = [np.random.beta(alpha[i]+1, beta[i]+1) for i in range(10)]
        return max(a, key=a.get), a#np.argmax(a), a #np.argmax(samples),samples






