import math
import random
import numpy.random as nr


class IIoTDevice():

    def __init__(self):
        #
        # self.IIoTID
        # self. capacitance
        # self.powerIdle
        # self.batteryLevel
        # self.ISL
        # self.baseTime
        # self.taskGenerationRate
        # self.statusCPU
        self.CPU_FREE = 1
        self.CPU_OCCUPIED = 2
        self.maxDistance = 50

    def IIoTdevice(self,numberIoT,taskGenerationRate,D2Dlink_1_IRD,D2Dlink_2_IRD):
        self.numberIoT = numberIoT
        self.IIoTID = []
        self.taskGenerationRate = []
        self.baseTime = []
        self.capacitance = []
        self.powerIdle = []
        self.batteryLevel = []
        self.ISL = []
        self.pairsFrequencyVoltage = dict()
        self.statusCPU = []
        self.positionOfx = []
        self.positionOfy = []
        self.position = []
        self.roleOfIIoT = []
        self.role_temp = nr.normal(0, 1, size = numberIoT)
        for i in range(numberIoT):

            if i == D2Dlink_1_IRD or i == D2Dlink_2_IRD:

                continue
            self.taskGenerationRate.append(taskGenerationRate)
            self.baseTime.append(random.randint(0,taskGenerationRate) + 1)
            self.capacitance.append(2.2 * math.pow(10, -9))
            self.powerIdle.append(900 * math.pow(10, -6))
            self.batteryLevel.append(36000 * math.pow(10,6))
            self.ISL.append(self.batteryLevel[i] * 0.1)
            self.pairsFrequencyVoltage[i] = {'long': 1 * math.pow(10, 6), 'double': 1.8}
            # self.pairsFrequencyVoltage[i][2] = {'long': 1 * math.pow(10, 6), 'double': 2.3}
            # self.pairsFrequencyVoltage[i][3] = {'long': 1 * math.pow(10, 6), 'double': 2.7}
            # self.pairsFrequencyVoltage[i][4] = {'long': 1 * math.pow(10, 6), 'double': 4.0}
            # self.pairsFrequencyVoltage[i][5] = {'long': 1 * math.pow(10, 6), 'double': 5.0}
            if i == 0:
                self.IIoTID.append("IBD" + str(1))
                self.position.append(0)
            elif i == 1:
                self.IIoTID.append("IBD"+str(2))
                self.position.append(0)
            else:
                # if self.position_temp[i-2] <= 0:
                #     self.position.append(1)
                # elif self.position_temp[i-2] > 0 and self.position_temp[i-2] < 2:
                #     self.position.append(2)
                # else:
                #     self.position.append(3)
                subx = random.randint(-100,100)
                self.positionOfx.append(subx)
                suby = random.randint(-45,45)
                self.positionOfy.append(suby)
                temp_type = self.classificationType(subx,suby)
                self.position.append(temp_type)
                #self.IIoTID.append("iiot" + str(i))
                self.IIoTID.append(i)

            self.statusCPU.append(self.CPU_FREE)
        temp_count_D2D1 = self.position.count(1)
        temp_count_D2D2 = self.position.count(2)
        temp_role1 = nr.normal(0,1,temp_count_D2D1)
        temp_role1_count = 0
        temp_role2 = nr.normal(0, 1, temp_count_D2D2)
        temp_role2_count = 0
        for i in range(2,numberIoT):
            if self.position[i] == 3:
                self.roleOfIIoT.append('IRD')
            elif self.position[i] == 1:
                if temp_role1[temp_role1_count] <= 0:
                    self.roleOfIIoT.append('IRD')
                else:
                    self.roleOfIIoT.append('ISD')
                temp_role1_count += 1
            elif self.position[i] == 2:
                if temp_role2[temp_role2_count] <= 0:
                    self.roleOfIIoT.append('IRD')
                else:
                    self.roleOfIIoT.append('ISD')
                temp_role2_count += 1




    #
    # def IIoTdevice(self,id, taskGenerationRate):
    #     self.IIoTID = id
    #     self.taskGenerationRate = taskGenerationRate
    #     self.baseTime = random.randint(0,taskGenerationRate) + 1
    #     self.capacitance = 2.2 * math.pow(10, -9)
    #     self.powerIdle = 900 * math.pow(10, -6)
    #     self.batteryLevel = 36000 * math.pow(10,6)
    #     self.ISL = self.batteryLevel * 0.1
    #     self.pairsFrequencyVoltage = dict()
    #     self.pairsFrequencyVoltage[1] = {'long': 1 * math.pow(10, 6), 'double': 1.8}
    #     self.pairsFrequencyVoltage[2] = {'long': 1 * math.pow(10, 6), 'double': 2.3}
    #     self.pairsFrequencyVoltage[3] = {'long': 1 * math.pow(10, 6), 'double': 2.7}
    #     self.pairsFrequencyVoltage[4] = {'long': 1 * math.pow(10, 6), 'double': 4.0}
    #     self.pairsFrequencyVoltage[5] = {'long': 1 * math.pow(10, 6), 'double': 5.0}
    #
    #
    #     self.statusCPU = self.CPU_FREE

    def getRoleIIoT(self):
        return self.roleOfIIoT

    def classificationType(self,subx,suby):
        minus_x_1 = subx - (-60)
        minus_x_2 = subx - 60     # 2ND D2D
        minus_y = suby - 0
        distance1 = math.sqrt(math.pow(minus_x_1, 2) + math.pow(minus_y, 2))
        distance2 = math.sqrt(math.pow(minus_x_2,2)+math.pow(minus_y,2))
        if distance1 < self.maxDistance:
            D2Dposition = 1
        elif distance2 < self.maxDistance:
            D2Dposition = 2
        else:
            D2Dposition = 3         # MEC offloading
        return D2Dposition

    def getPosition(self):
        return self.position

    def getId(self):
        return self.IIoTID

    def getBaseTime(self):
        return self.baseTime

    def getPairsFrequencyValtage(self):
        return self.pairsFrequencyVoltage

    def getBatteryLevel(self):
        return self.batteryLevel

    def calculateDynamicPower(self, key,operatingFreq, volt):
        power = self.capacitance[key] * math.pow(volt,2.0) * operatingFreq
        return power

    def calculateExeTime(self, operatingFreq, compWorkload):
        time = compWorkload / operatingFreq
        time = time * math.pow(10,6)
        return time

    def calculateDynamicEnergy(self, key,operatingFreq, volt, compWorkload):
        energy = self.calculateDynamicPower(key,operatingFreq, volt) * self.calculateExeTime(operatingFreq, compWorkload)
        return energy

    def calculateConsumedIdleEneryg(self, timeInIDLE):
        idleEnergy = self.powerIdle * timeInIDLE
        return idleEnergy

    def consumeBattery(self, consumedEnergy):
        self.batteryLevel = self.batteryLevel - consumedEnergy

    def verifyCPUFree(self,key):
        if self.batteryLevel[key] <= self.ISL[key]:

            return False
        if self.statusCPU[key] == self.CPU_FREE:
            return True
        return False

    def alterCPUStatus(self, newStatus,key):
        if newStatus != self.CPU_FREE and newStatus != self.CPU_OCCUPIED:
            print("error",self.IIoTID)
        self.statusCPU[key] = newStatus
