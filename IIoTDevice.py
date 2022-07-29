import math
import random


class IIoTDevice():

    def __init__(self):

        self.IIoTID
        self. capacitance
        self.powerIdle
        self.batteryLevel
        self.ISL
        self.baseTime
        self.taskGenerationRate
        self.statusCPU
        self.CPU_FREE = 1
        self.CPU_OCCUPIED = 2

    def IIoTdevice(self,id, taskGenerationRate):
        self.IIoTID = id
        self.taskGenerationRate = taskGenerationRate
        self.baseTime = random.randint(self.taskGenerationRate) + 1
        self.capacitance = 2.2 * math.pow(10, -9)
        self.powerIdle = 900 * math.pow(10, -6)
        self.batteryLevel = 36000 * math.pow(10,6)
        self.ISL = self.batteryLevel * 0.1
        self.pairsFrequencyVoltage = dict()
        self.pairsFrequencyVoltage[1] = {'long': 1 * math.pow(10, 6), 'double': 1.8}
        self.pairsFrequencyVoltage[2] = {'long': 1 * math.pow(10, 6), 'double': 2.3}
        self.pairsFrequencyVoltage[3] = {'long': 1 * math.pow(10, 6), 'double': 2.7}
        self.pairsFrequencyVoltage[4] = {'long': 1 * math.pow(10, 6), 'double': 4.0}
        self.pairsFrequencyVoltage[5] = {'long': 1 * math.pow(10, 6), 'double': 5.0}


        self.statusCPU = self.CPU_FREE

    def getId(self):
        return self.IIoTID

    def getBaseTime(self):
        return self.baseTime

    def getPairsFrequencyValtage(self):
        return self.pairsFrequencyVoltage

    def getBatteryLevel(self):
        return self.batteryLevel

    def calculateDynamicPower(self, operatingFreq, volt):
        power = self.capacitance * math.pow(volt, 2) * operatingFreq
        return power

    def calculateExeTime(self, operatingFreq, compWorkload):
        time = compWorkload / operatingFreq
        time = time * math.pow(10,6)
        return time

    def calculateDynamicEnergy(self, operatingFreq, volt, compWorkload):
        energy = self.calculateDynamicPower(operatingFreq, volt) * self.calculateExeTime(operatingFreq, compWorkload)
        return energy

    def calculateConsumedIdleEneryg(self, timeInIDLE):
        idleEnergy = self.powerIdle * timeInIDLE
        return idleEnergy

    def consumeBattery(self, consumedEnergy):
        self.batteryLevel = self.batteryLevel - consumedEnergy

    def verifyCPUFree(self):
        if self.batteryLevel <= self.ISL:
            print(self.IIoTID,"reched battery")
            return False
        if self.statusCPU == self.CPU_FREE:
            return True
        return False

    def alterCPUStatus(self, newStatus):
        if newStatus != self.CPU_FREE and newStatus != self.CPU_OCCUPIED:
            print("error",self.IIoTID)
        self.statusCPU = newStatus
