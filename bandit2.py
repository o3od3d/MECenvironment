import random

import numpy as np
import gym
from gym import spaces
from gym.utils import seeding
#from random import *

class BanditEnv(gym.Env):
    """
    Bandit environment base to allow agents to interact with the class n-armed bandit
    in different variations
    p_dist:
        A list of probabilities of the likelihood that a particular bandit will pay out
    r_dist:
        A list of either rewards (if number) or means and standard deviations (if list)
        of the payout that bandit has
    info:
        Info about the environment that the agents is not supposed to know. For instance,
        info can releal the index of the optimal arm, or the value of prior parameter.
        Can be useful to evaluate the agent's perfomance
    """

    def __init__(self, p_dist, r_dist, info={}):
        if len(p_dist) != len(r_dist):
            raise ValueError("Probability and Reward distribution must be the same length")

        if min(p_dist) < 0 or max(p_dist) > 1:
            raise ValueError("All probabilities must be between 0 and 1")

        for reward in r_dist:
            if isinstance(reward, list) and reward[1] <= 0:
                raise ValueError("Standard deviation in rewards must all be greater than 0")

        self.p_dist = p_dist
        self.r_dist = r_dist
        self.info = info

        self.n_bandits = len(p_dist)
        self.action_space = spaces.Discrete(self.n_bandits)
        self.observation_space = spaces.Discrete(1)

        self._seed()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)

        reward = 0
        done = True

        if np.random.uniform() < self.p_dist[action]:
            if not isinstance(self.r_dist[action], list):
                reward = self.r_dist[action]
            else:
                reward = np.random.normal(self.r_dist[action][0], self.r_dist[action][1])

        return [0], reward, done, self.info

    def reset(self):
        return [0]

class BanditTwoArmedHighLowFixed(BanditEnv):
    """Stochastic version with a large difference between which bandit pays out of two choices"""

    def __init__(self,arm_reward,arm_count):
        self.arm_reward = arm_reward
        self.arm_count = len(arm_count)
        arm_prob = np.zeros(self.arm_count)#{i: 0 for i in arm_count}
        maxArm = max(self.arm_reward.items(), key=lambda x: x[1]['importance'])
        maxArm_index = maxArm[0]
        i = 0
        for index,(key,value) in enumerate(self.arm_reward.items()):
            arm_prob[index] = value['importance']
        #print("ㅎㅎㅎ",arm_prob,min(arm_prob.values()))

        BanditEnv.__init__(self, p_dist=arm_prob, r_dist=np.ones(self.arm_count), info={'optimal_arm': maxArm_index})

        #BanditEnv.__init__(self, p_dist=[0.1, 0.2, 0.3, 0.4, 0.8, 0.9, 0.99, 0.7, 0.8, 1], r_dist=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], info={'optimal_arm':10})
