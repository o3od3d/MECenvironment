import numpy as np
from bandit2 import BanditTwoArmedHighLowFixed

class proposed_DTS():
    def __init__(self,NumberOfIoT,totalRound):
        print("bandit start")
        self.total_rounds = 50
        self.count = {i: 0 for i in range(NumberOfIoT)}#np.zeros(NumberOfIoT)
        self.sum_rewards = {i: 0 for i in range(NumberOfIoT)} #np.zeros(NumberOfIoT)
        self.Q = {i: 0 for i in range(NumberOfIoT)} #np.zeros(NumberOfIoT)
        self.alpha = {i: 0 for i in range(NumberOfIoT)} #np.ones(NumberOfIoT)
        self.beta = {i: 0 for i in range(NumberOfIoT)} #np.ones(NumberOfIoT)
        # self.x = np.zeros(self.total_rounds * totalRound)
        # self.y = np.zeros(self.total_rounds * totalRound)
        self.T = 50
        successRate = np.zeros(totalRound)
        arm2 = 0
        numberOfSuccess = 0
        regretUpdate = np.zeros(totalRound)

    def proposed_DTS(self,win_ISD,gamma):

        arm_count = win_ISD.keys()
        maximum = np.zeros(len(win_ISD))
        arm_reward = win_ISD
        Q, alpha, beta = self.preprocessing(win_ISD)

        env = BanditTwoArmedHighLowFixed(arm_reward, arm_count,0)

        #gamma = gamma * 0.99
        for i in range(self.total_rounds):
            arm2 = self.thompson_sampling(alpha, beta,maximum,arm_count)
            arm = self.UCB(i, self.T, arm2,self.count,list(arm_count))
            j = 0
            for k in list(arm_count):
                if k == arm:
                    next_state, reward, done, info = env.step(j)
                    break
                j += 1

            self.count[arm] += 1
            self.sum_rewards[arm] += reward
            Q[arm] = self.sum_rewards[arm] / self.count[arm]
            if reward == 1:
                alpha[arm] = gamma * alpha[arm] + 1
            else:
                beta[arm] = gamma * beta[arm] + 1


        opt_arm = np.argmax(Q)
        for index, (key, elem) in enumerate(win_ISD.items()):
            if opt_arm == index:
                opt_arm = key
                break
        self.postprocessing(win_ISD,Q,alpha,beta)
        Q,alpha,beta = self.preprocessing(win_ISD)

        return Q

    def preprocessing(self,win_ISD):
        Q = dict()
        alpha = dict()
        beta = dict()
        for key, value in list(win_ISD.items()):
            Q[key] = self.Q[key]
            alpha[key] = self.alpha[key]
            beta[key] = self.beta[key]
        return Q,alpha,beta

    def postprocessing(self,win_ISD,Q,alpha,beta):
        for key,value in list(win_ISD.items()):
            self.Q[key] = (self.Q[key] + Q[key]) / 2
            self.alpha[key] += alpha[key]
            self.beta[key] += beta[key]

    def UCB(self,i,T,samples,count,arm_count):
        if i < len(arm_count):
            return arm_count[i]
        else:
            T = T * 0.99
            denom = sum([np.exp(j / T) for j in count])
            probs = [np.exp(j/ T) / denom for j in count]
            ucb = {arm:(samples[arm] - probs[arm]) for arm in arm_count}

        return max(ucb, key=ucb.get)#np.argmax(ucb)

    def thompson_sampling(self,alpha, beta,maximum,arm_count):
        samples = {i:np.random.beta(alpha[i]+1, beta[i]+1) for i in arm_count}
        maximum[np.argmax(samples)] += 1
        return samples