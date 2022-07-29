import sys


class Task():

    def __init__(self):
        self.taskId
        self.deviceId
        self.generateTime                   # Task generate time
        self.deadlineLatency             # micro seconds
        self.computationWorkload      # cpu cycles
        self.dataSize                            # bits
        self.returnDataSize
        self.allocatedTask                 # whether to allocate iot,mec or cloud => 0,1,2
        self.statusOftask                    # whether task processing has been completed => 0(deny) or 1(success) or 2(processing)

        self.TASK_ALIVE = 1
        self.TASK_CONCLUEDE = 2
        self.TASK_CANCELLED = 3
        self.taskStatus

        self.poicy


    def Task(self, taskId, deviceId, deadlineLatency, generateTime, computationWorkload, dataSize, returnDataSize):
        self.taskId = taskId
        self.deviceId = deviceId
        self.generateTime = generateTime  # Task generate time
        self.deadlineLatency = deadlineLatency  # micro seconds
        self.computationWorkload = computationWorkload  # cpu cycles
        self.dataSize = dataSize
        self.returnDataSize = returnDataSize

        self.energyExe = 0
        self.energyTransfer = 0
        self.timeEXE = 0
        self.timeTransfer = 0
        self.taskStatus = self.TASK_ALIVE

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
        elif systemTime < (self.generateTask + self.deadlineLatency):
            self.statusOftask = self.TASK_CONCLUEDE
        else:
            self.statusOftask = self.TASK_CANCELLED



    def verifyTaskCritical(self):
        if self.deadlineLatency == -1:
            return False
        else:
            return True