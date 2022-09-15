import random
import numpy.random as nr
import sys


class Service():

    def __init__(self):
        # self.taskId
        # self.deviceId
        # self.generateTime                   # Task generate time
        # self.deadlineLatency             # micro seconds
        # self.computationWorkload      # cpu cycles
        # self.dataSize                            # bits
        # self.returnDataSize
        # self.allocatedTask                 # whether to allocate iot,mec or cloud => 0,1,2
        # self.statusOftask                    # whether task processing has been completed => 0(deny) or 1(success) or 2(processing)
        print('service')
        self.TASK_ALIVE = 1
        self.TASK_CONCLUEDE = 2
        self.TASK_CANCELLED = 3
        # self.taskStatus
        #
        # self.poicy


    def Service(self, deviceId, remainASK,remainStauts_ISD,remain_ISD,deadlineLatency, generateTime, computationWorkload, dataSize, returnDataSize):
        self.deviceId = deviceId + remain_ISD
        self.ask = dict()
        self.generateTime = []
        self.deadlineLatency = []
        self.computationWorkload = dict()
        self.dataSize = dict()
        self.returnDataSize = []
        self.taskStatus = dict()
        self.freq_level = []
        self.energyExe = []
        self.energyTransfer = []
        self.timeEXE = []
        self.timeTransfer = []
        for i in deviceId:

            self.ask.setdefault(i, round(random.uniform(3, 10), 3))

            # self.generateTime.append(generateTime)  # Task generate time
            # self.deadlineLatency.append(deadlineLatency)  # micro seconds
            self.computationWorkload.setdefault(i,round(random.uniform(0,1),3))  # cpu cycles
            # self.dataSize.setdefault(i,round(random.uniform(10,100),3))
            # self.returnDataSize.append(returnDataSize)

            self.energyExe.append(0)
            self.energyTransfer.append(0)
            self.timeEXE.append(0)
            self.timeTransfer.append(0)
            self.taskStatus.setdefault(i,self.TASK_ALIVE)
        for i in remain_ISD:
            self.ask.setdefault(i, remainASK[i])

            # self.generateTime.append(generateTime)  # Task generate time
            # self.deadlineLatency.append(deadlineLatency)  # micro seconds
            self.computationWorkload.setdefault(i, computationWorkload[i])  # cpu cycles
            # self.dataSize.setdefault(i, dataSize[i])
            # self.returnDataSize.append(returnDataSize)

            self.energyExe.append(0)
            self.energyTransfer.append(0)
            self.timeEXE.append(0)
            self.timeTransfer.append(0)
            self.taskStatus.setdefault(i, remainStauts_ISD[i])
        self.freq = nr.normal(1,0,len(deviceId))
        for i in range(len(deviceId)):
            if self.freq[i] < 0:
                self.freq_level.append('low')
            elif self.freq[i] >= 0 and self.freq[i] < 1:
                self.freq_level.append('mid')
            else:
                self.freq_level.append('high')

    def freqLevel(self):
        return self.freq_level

    def getAsk(self):
        return self.ask

    def getIDtask(self):
        return self.taskId

    def getIdDeviceGenerator(self):
        return self.deviceId

    def getTaskStatus(self):
        return self.taskStatus

    def getDeadline(self):
        return self.deadlineLatency

    def getBaseTime(self):
        return self.generateTime

    def getCompLoad(self):
        return self.computationWorkload

    def getEntryDataSize(self):
        return self.dataSize

    def getReturnDataSize(self):
        return self.returnDataSize

    def getPolicy(self):
        return self.getPolicy()

    def getTotalEneryCon(self):
        return self.energyExe + self.energyTransfer

    def getExeTime(self):
        return self.energyExe

    def getTransferEnery(self):
        return self.energyTransfer

    def getTotalElpTime(self):
        return self.timeExe + self.timeTransfer

    def getEXEtIME(self):
        return self.timeEXE

    def getTransferTime(self):
        return self.timeTransfer

    def setExeEnery(self,exeEnergy):
        self.energyExe = exeEnergy

    def setTransferEnergy(self, transferEN):
        self.energyTransfer = transferEN

    def setEXETime(self, exetime):
        self.timeEXE = exetime

    def setTransferTime(self, transferTime):
        self.timeTransfer = transferTime

    def setPolicy(self,policy):
        if policy != 1 and policy != 2 and policy != 3:
            print("error",self.getIDtask())
        self.policy = policy

    def verifyTaksFinish(self, systemTime):
        if self.statusOftask != self.TASK_ALIVE:
            print("error",self.taskId,"is already finished")
        timeToConclusion = self.generateTime + self.getTotalElpTime()
        if timeToConclusion == systemTime:
            self.finalizeTask(systemTime)
            return True
        return False


    def finalizeTask(self, systemTime):
        if self.deadlineLatency == -1:
            self.statusOftask = self.TASK_CONCLUEDE
            print('dfa')
        elif systemTime < (self.generateTask + self.deadlineLatency):
            self.statusOftask = self.TASK_CONCLUEDE
            print('fdas')
        else:
            self.statusOftask = self.TASK_CANCELLED
            print("task fail")



    def verifyTaskCritical(self):
        if self.deadlineLatency == -1:
            return False
        else:
            return True