import math


class MECServer():

    def __init__(self):
        self.MECID
        self.capacitance
        self.powerIdle
        self.statusCPUs
        self.Cpu_occupied = True
        self.CPU_FREE = False
        self.Max_CPUs = 20
        self.pairsFrequencyVoltage == []
    def MECserver(self, MECID):
        self.MECID = MECID
        self.capacitance = (1.8 * math.pow(10, -9))     # Farads
        self.powerIdle = 0.675                          # W

        self.pairsFrequencyVoltage = dict()
        self.pairsFrequencyVoltage[1] = {'long': 600 * math.pow(10, 6),'double': 0.8}
        self.pairsFrequencyVoltage[2] = {'long': 750 * math.pow(10, 6), 'double': 0.825}
        self.pairsFrequencyVoltage[3] = {'long': 1000 * math.pow(10, 6), 'double': 1.0}
        self.pairsFrequencyVoltage[4] = {'long': 1500 * math.pow(10, 6), 'double': 1.2}


        self.statusCPUs = [False for i in range(self.Max_CPUs)]

    def getId(self):
        return self.MECID

    def getNumberOfFreeCPUs(self):
        count = 0
        for i in range(self.Max_CPUs):
            if(self.statusCPUs[i] == self.CPU_FREE):
                count += 1
        return count

    def getPairFrequencyVoltages(self):
        return self.pairsFrequencyVoltage

    def calculateDynamicPower(self, operationFrequency, voltage):
        power = (self.capacitance * math.pow(voltage, 2) * operationFrequency)
        return power

    def calculateExecutionTime(self, operationFrequency, compuataionWorkload):
        time = compuataionWorkload / operationFrequency
        time = time * math.pow(10, 6)
        return time

    def calculateDynamicEnergyConsumed(self, operationFrequency, voltage, compuataionWorkload):
        energy = self.calculateDynamicPower(operationFrequency, voltage) * self.calculateExecutionTime(operationFrequency, compuataionWorkload)
        return energy

    def verifyCPUFree(self):
        for status in self.statusCPUs:
            if status == self.CPU_FREE:
                return True
        return False

    def occupyCPU(self):
        if self.verifyCPUFree() == True:
            for i in range(self.MAX_CPUs):
                if self.statusCPUs[i] == self.CPU_FREE:
                    self.statusCPUs.remove(i)
                    self.statusCPUs.append(self.Cpu_occupied)
                    return True
        print(self.MECID,"all cpu occupied")
        return False

    def freeCPU(self):
        for i in range(self.Max_CPUs):
            if self.statusCPUs[i] == self.Cpu_occupied:
                self.statusCPUs.remove(i)
                self.statusCPUs.append(i)
                return True
        print(self.MECID,"All cpu already free")
        return False
