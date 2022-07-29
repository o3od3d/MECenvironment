
from task import Task
from IIoTDevice import IIoTDevice
from MECServer import MECServer
from cloudServer import CloudDataCenter
from RAN_5G import RAN_5G
from FiberOptics import FiberOptics

class scheduler():

    def __init__(self):
        self.coefficientEnergy
        self.coefficientTime

        self.energy5GUp
        self.time5GUp
        self.energy5GDown
        self.time5GDown
        self.energyFiberUp
        self.timeFiberUp
        self.energyFiberDown
        self.timeFiberDown

        self.POLICY_IOT = 1
        self.POLICY_MEC = 2
        self.POLICY_CLOUD = 3

        self.NORMAL_TASK = -1

        self.costListIoTDevice = dict()
        self.costListMECServer = dict()
        self.costListCloud = dict()

    def sheduler(self, task, coefficientEnergy, coefficientTime, alpha, beta, gamma):
        self.task = task
        self.iotDevice = IIoTDevice.IIoTdevice("IRD",100)
        self.serverMEC = MECServer.MECserver("MEC")
        self.cloud = CloudDataCenter.cloudServer("cloud")

        self.transmission5G = RAN_5G()
        self.transmissionFiber = FiberOptics()

        self.coefficientEnergy = coefficientEnergy
        self.coefficientTime = coefficientTime

        self.energy5GUp = self.transmission5G.calculateComsumedEnergy(self.task.getEntryDataSize())
        self.time5GUp = self.transmission5G.calculateTransferTime(self.task.getEntryDataSize())
        self.energy5GDown = self.transmission5G.calculateComsumedEnergy(self.task.getReturnDataSize())
        self.time5GDown = self.transmission5G.calculateTransferTime(self.task.getReturnDataSize())

        self.energyFiberUp = self.transmissionFiber.calculateEnergyCon(self.task.getEntryDataSize())
        self.timeFiberUp = self.transmissionFiber.calculateTransmissionTime(self.task.getEntryDataSize())
        self.energyFiberDown = self.transmissionFiber.calculateEnergyCon(self.task.getReturnDataSize())
        self.timeFiberDown = self.transmissionFiber.calculateTransmissionTime(self.task.getReturnDataSize())

        self.calculateCostIoTDevice(alpha)
        self.calculateCostMECServer(beta)
        self.calculateCostCloud(gamma)

    def calculateCostIoTDevice(self,alpha):
        pairsFrequencyVoltage = self.iotDevice.getPairsFrequencyValtage()

        for key,value in list(pairsFrequencyVoltage):
            exeTime = self.iotDevice.calculateExeTime(value['long'],self.task.getCompLoad())
            dynamicEnergy = self.iotDevice.calculateDynamicEnergy(value['long'],value['double'],self.task.getCompLoad())
            cost = (self.coefficientEnergy * dynamicEnergy + self.coefficientTime * exeTime) * alpha
            self.costListIoTDevice[key] = {'cost':cost, 'dynamicEnergy':dynamicEnergy,'consumed energy':0.0,'exe time':exeTime,'elap time':0.0,'op freq':value['long'],'supply volt':value['double']}

    def calculateCostMECServer(self,beta):
        pairsFrequencyVoltage = self.serverMEC.getPairsFrequencyValtage()

        for key,value in list(pairsFrequencyVoltage):
            exeTime = self.serverMEC.calculateExecutionTime(value['long'],self.task.getCompLoad())
            dynamicEnergy = self.serverMEC.calculateDynamicEnergyConsumed(value['long'],value['double'],self.task.getCompLoad())
            totalDynamicEnergy = dynamicEnergy + self.energy5GUp + self.energy5GDown
            totalExeTime = exeTime + self.time5GUp + self.time5GDown
            cost = (self.coefficientEnergy * totalDynamicEnergy + self.coefficientTime * totalExeTime) * beta
            self.costListMECServer[key] = {'cost':cost, 'dynamicEnergy':dynamicEnergy,'consumed energy':(self.energy5GUp + self.energy5GDown),'exe time':exeTime,'elap time':(self.time5GUp + self.time5GDown),'op freq':value['long'],'supply volt':value['double']}

    def calculateCostCloud(self,gamma):

        standardFreq = self.cloud.getStandardFrequency()
        standTime = self.cloud.calculateExecutionTimeStardardFreq(self.task.getCompLoad())
        standEnergy = self.cloud.calculateDynamicEnergyStandardFreq(self.task.getCompLoad())

        totalStandardEnergy = standEnergy + self.energy5GUp + self.energyFiberUp + self.energyFiberDown + self.energy5GDown
        totalStandardTime = standTime + self.time5GUp + self.timeFiberUp + self.timeFiberDown +self.time5GDown

        standCost = (self.coefficientEnergy * totalStandardEnergy + self.coefficientTime * totalStandardTime) * gamma
        self.costListCloud[1] = {'cost': standCost, 'dynamicEnergy': standEnergy,
                                       'consumed energy': (self.energy5GUp + self.energyFiberUp + self.energyFiberDown + self.energy5GDown), 'exe time': standTime,
                                       'elap time': (self.time5GUp + self.timeFiberUp + self.timeFiberDown +self.time5GDown), 'op freq': standardFreq,
                                       'supply volt': 0.0}

        turboFreq = self.cloud.getTurboBoostFrequency()
        turboTime = self.cloud.calculaTempoExecucaoFreqTurboBoost(self.task.getCompLoad())
        turboEnergy = self.cloud.calculateDynamicEnergyTurboFreq(self.task.getCompLoad())

        totalTurboEnergy = turboEnergy + self.energy5GUp + self.energyFiberUp + self.energyFiberDown + self.energy5GDown
        totalTurboTime = turboTime + self.time5GUp + self.time5GDown + self.timeFiberDown + self.timeFiberUp

        turboCost = (self.coefficientEnergy * totalTurboEnergy + self.coefficientTime * totalTurboTime) * gamma
        self.costListCloud[2] = {'cost': turboCost, 'dynamicEnergy': turboEnergy,
                                 'consumed energy': (
                                             self.energy5GUp + self.energyFiberUp + self.energyFiberDown + self.energy5GDown),
                                 'exe time': turboTime,
                                 'elap time': (self.time5GUp + self.timeFiberUp + self.timeFiberDown + self.time5GDown),
                                 'op freq': turboFreq,
                                 'supply volt': 0.0}

    def defineAllocationPolicy(self,flagIoT, flagMECServer):
        globalCostList = dict()
        globalCostListCritical = [[]]
        resultOctet = []
        if flagIoT == True:
            for key, value in list(self.costListIoTDevice):
                index = '1'+key
                globalCostList[index] = self.costListIoTDevice[key]
                globalCostList[index]['POLICY'] = 1
            globalCostList = dict(globalCostList)
        if flagMECServer == True:
            for key, value in list(self.costListMECServer):
                index = '2' + key
                globalCostList[index] = self.costListIoTDevice[key]
                globalCostList[index]['POLICY'] = 2
            globalCostList = dict(globalCostList)
        for key, value in list(self.costListCloud):
            index = '3' + key
            globalCostList[index] = self.costListCloud[key]
            globalCostList[index]['POLICY'] = 3
        globalCostList = dict(globalCostList)

        # critical order
        if self.task.getDeadline() != self.NORMAL_TASK:
            for index,(key,value) in enumerate(globalCostList):
                globalCostListCritical[index].append(value['exe time'] + value['elap time'])
                globalCostListCritical[index].append(value['dynamicEnergy'])
                globalCostListCritical[index].append(value['consumed energy'])
                globalCostListCritical[index].append(value['cost'])
                globalCostListCritical[index].append(value['elap time'])
                globalCostListCritical[index].append(value['op freq'])
                globalCostListCritical[index].append(value['supply volt'])
                globalCostListCritical[index].append(value['POLICY'])
            # globalCostListCritical 정렬 필요
            if False:
                self.printOctetList(globalCostListCritical)

            resultOctet.append(globalCostListCritical[0][3])
            resultOctet.append(globalCostListCritical[0][1])
            resultOctet.append(globalCostListCritical[0][2])
            resultOctet.append(globalCostListCritical[0][0] - globalCostListCritical[0][4])
            resultOctet.append(globalCostListCritical[0][4])
            resultOctet.append(globalCostListCritical[0][5])
            resultOctet.append(globalCostListCritical[0][6])
            resultOctet.append(globalCostListCritical[0][7])

            return resultOctet
        else:
            # globalCostList.sort()
            if False:
                self.printOctetList(globalCostList)
            return globalCostList[0] # 가장 작은 값 리턴

    def printOctetList(self,globalCostListCritical):
        if self.task.getDeadline() != -1:
            print("critical task")
        else:
            print("non-critical task")


    def printSystemCosts(self):
        print("local processing")


