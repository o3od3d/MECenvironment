import random

import numpy as np


class Application():

    def __init__(self):
        print("Hello application")
        # self.id
        # # self.rateGeneration                    # micro seconds
        # # self.dataEntrySize                     # bits
        # # self.resultsSize                         # bits
        # # self.computationalLoad              # CPU cycles
        # # self.criticalTaskPercentages  # percentages 0 ~1
        # # self.criticalTaksDeadline        # micro seconds
        # # self.numberOfTask
        # # percentages 0 ~1
        # if self.criticalTaskPercentages > 1 or self.criticalTaskPercentages < 0:
        #     print("app",self.id,"percente out of bounds")
    def application(self, id, rateGeneration, dataEntrySize, resultsSize, computationalLoad, criticalTaskPercentages, criticalTaksDeadline,tasknumber,remainTask,remainTaskData,remainCOMP):
        self.id = id
        self.dataEntrySize = dict()
        self.rateGeneration = rateGeneration  # micro seconds
        self.resultsSize = resultsSize  # bits
        self.computationalLoad = dict()
        for i in tasknumber:

            self.dataEntrySize.setdefault(i,round(random.uniform(10,100),3))#[i]['datasize'] = round(random.uniform(10,100),3)#dataEntrySize  # bits

            self.computationalLoad.setdefault(i,round(random.uniform(10,100),3))#[i]['comp'] = round(random.uniform(10,100),3)
        for i in remainTask:
            self.dataEntrySize.setdefault(i,remainTaskData[i])#[i]['datasize'] = remainTaskData[i]
            self.computationalLoad.setdefault(i,remainCOMP[i])#[i]['comp'] = remainCOMP[i]

                #computationalLoad
        if criticalTaskPercentages > 1 or criticalTaskPercentages < 0:
            print("app",self.id,"percente out of bounds")
        self.criticalTaskPercentages = criticalTaskPercentages  # percentages 0 ~1
        self.criticalTaksDeadline = criticalTaksDeadline  # micro seconds
        self.numberOfTask = 0

    def getID(self):
        return self.id

    def getRateGenerate(self):
        return self.rateGeneration

    def getDataEntrySize(self):
        return self.dataEntrySize

    def getResultSize(self):
        return self.resultsSize

    def getCriticalTaskDeadline(self):
        return self.criticalTaksDeadline

    def getCriticalTaskPercentage(self):
        return self.criticalTaskPercentages

    def getNumberOfTask(self):
        return self.numberOfTask

    def getComputaionWorkload(self):
        return self.computationalLoad

    def setNumberOfTask(self, numberOfTask):
        self.numberOfTask = numberOfTask

    def defineInTaskIsCritical(self, numberOfTask):
        if ((numberOfTask + 1) * self.numberOfTask * self.criticalTaskPercentages) % self.numberOfTask == 0:
            return True
        else:
            return False
