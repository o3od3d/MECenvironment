import random
import sys


class Task():

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

        self.TASK_ALIVE = 1
        self.TASK_CONCLUEDE = 2
        self.TASK_CANCELLED = 3
        # self.taskStatus
        #
        # self.poicy


    def Task(self, deviceId, deadlineLatency, generateTime, computationWorkload, dataSize, returnDataSize):
        self.taskId = []
        self.deviceId = deviceId
        self.generateTime = []
        self.deadlineLatency = []
        self.computationWorkload = []
        self.dataSize = []
        self.returnDataSize = []
        self.bid = []
        self.energyExe = []
        self.energyTransfer = []
        self.timeEXE = []
        self.timeTransfer = []
        self.taskStatus = []
        self.policy = []
        for i in range(len(deviceId)):
            self.taskId.append(deviceId[i])
            self.generateTime.append(generateTime)  # Task generate time
            self.deadlineLatency.append(round(random.uniform(0, 14), 3))  # micro seconds
            self.computationWorkload.append(computationWorkload[i])  # cpu cycles
            self.dataSize.append(dataSize[i])
            self.returnDataSize.append(returnDataSize)

            self.bid.append(round(random.uniform(0, 14), 3))

            self.energyExe.append(0)
            self.energyTransfer.append(0)
            self.timeEXE.append(0)
            self.timeTransfer.append(0)
            self.taskStatus.append(self.TASK_ALIVE)

    def getDeviceId(self):
        return self.deviceId

    def getBid(self):
        return self.bid

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
        return self.policy

    def getTotalEneryCon(self):
        return self.energyExe + self.energyTransfer

    def getExeTime(self):
        return self.energyExe

    def getTransferEnery(self):
        return self.energyTransfer

    def getTotalElpTime(self,key):
        return self.getEXEtIME()[key] + self.timeTransfer[key]

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

    def setPolicy(self,policy,D2Dlink_1_IRD):
        if policy != 1 and policy != 2 and policy != 3:
            print("error",self.getIDtask())
        for i in range(len(D2Dlink_1_IRD)):
            self.policy.append(policy)

    def verifyTaksFinish(self, systemTime,key):
        temp = 0
        for i in range(len(self.deviceId)):
            if key == self.deviceId[i]:
                temp = i
        if self.taskStatus[temp] != self.TASK_ALIVE:
            print("error",self.taskId,"is already finished")
        timeToConclusion = self.generateTime[temp] + self.getTotalElpTime(temp)
        if timeToConclusion == systemTime:
            self.finalizeTask(systemTime,temp)
            return True
        return False


    def finalizeTask(self, systemTime,key):
        if self.deadlineLatency[key] == -1:
            self.taskStatus[key] = self.TASK_CONCLUEDE
        elif systemTime < (self.generateTime[key] + self.deadlineLatency[key]):
            self.taskStatus[key] = self.TASK_CONCLUEDE
        else:
            self.taskStatus[key] = self.TASK_CANCELLED



    def verifyTaskCritical(self):
        if self.deadlineLatency == -1:
            return False
        else:
            return True