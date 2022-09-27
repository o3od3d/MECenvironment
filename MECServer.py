import math


class MECServer():

    def __init__(self):
        # self.MECID
        # self.capacitance
        # self.powerIdle
        # self.statusCPUs
        self.Cpu_occupied = True
        self.CPU_FREE = False
        self.Max_CPUs = 10
        #self.pairsFrequencyVoltage == []
    def MECserver(self, MECnumber):
        self.MECID = []
        self.capacitance = []
        self.powerIdle = []
        self.pairsFrequencyVoltage = dict()
        self.statusCPUs = []
        for i in range(MECnumber):
            self.MECID.append("MEC" + str(i))
            self.capacitance.append((1.8 * math.pow(10, -9)))     # Farads
            self.powerIdle.append(0.675)                          # W

            self.pairsFrequencyVoltage[i] = {'long': 600 * math.pow(10, 6),'double': 0.8}
            # self.pairsFrequencyVoltage[2] = {'long': 750 * math.pow(10, 6), 'double': 0.825}
            # self.pairsFrequencyVoltage[3] = {'long': 1000 * math.pow(10, 6), 'double': 1.0}
            # self.pairsFrequencyVoltage[4] = {'long': 1500 * math.pow(10, 6), 'double': 1.2}


            self.statusCPUs.extend([False for i in range(self.Max_CPUs)])
    # def MECserver(self, MECID):
    #     self.MECID = MECID
    #     self.capacitance = (1.8 * math.pow(10, -9))     # Farads
    #     self.powerIdle = 0.675                          # W
    #
    #     self.pairsFrequencyVoltage = dict()
    #     self.pairsFrequencyVoltage[1] = {'long': 600 * math.pow(10, 6),'double': 0.8}
    #     self.pairsFrequencyVoltage[2] = {'long': 750 * math.pow(10, 6), 'double': 0.825}
    #     self.pairsFrequencyVoltage[3] = {'long': 1000 * math.pow(10, 6), 'double': 1.0}
    #     self.pairsFrequencyVoltage[4] = {'long': 1500 * math.pow(10, 6), 'double': 1.2}
    #
    #
    #     self.statusCPUs = [False for i in range(self.Max_CPUs)]
    def getStatusCOU(self):
        return self.statusCPUs

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

    def calculateDynamicPower(self, key,operationFrequency, voltage):
        power = (self.capacitance[key] * math.pow(voltage, 2) * operationFrequency)
        return power

    def calculateExecutionTime(self, operationFrequency, compuataionWorkload):
        time = compuataionWorkload / operationFrequency
        time = time * math.pow(10, 6)
        return time

    def calculateDynamicEnergyConsumed(self, key,operationFrequency, voltage, compuataionWorkload):
        energy = self.calculateDynamicPower(key,operationFrequency, voltage) * self.calculateExecutionTime(operationFrequency, compuataionWorkload)
        return energy



    def verifyCPUFree2(self,key):
        for status in self.statusCPUs[key]:
            if status == self.CPU_FREE:
                return True
        return False

    def verifyCPUFree(self):
        for status in self.statusCPUs:
            if status == self.CPU_FREE:
                return True
        return False

    def occupyCPU(self,key):
        if self.verifyCPUFree() == True:
            for i in range(self.Max_CPUs):
                if self.statusCPUs[i] == self.CPU_FREE:
                    #self.statusCPUs.pop(i)
                    #self.statusCPUs.append(self.Cpu_occupied)
                    self.statusCPUs[i] = self.Cpu_occupied
                    return True

        return False

    def freeCPU(self):
        for i in range(self.Max_CPUs):
            if self.statusCPUs[i] == self.Cpu_occupied:
                self.statusCPUs.pop(i)
                self.statusCPUs.append(self.CPU_FREE)
                return True

        return False
