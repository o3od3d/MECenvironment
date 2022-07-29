import math


class RAN_5G():

    def __init__(self):
        self.latency
        self.alpha
        self.beta
        self.transferRate

    def RAN_5G(self):
        self.latency = 5 * math.pow(10, -3)
        self.alpha = 0.52 * math.pow(10, -3)
        self.beta = 3.86412
        self.transferRate = math.pow(10, 9)

    def calculatePower(self):
        power = self.alpha * self.transferRate / math.pow(10, 6) + self.beta
        return power

    def calculateTransferTime(self, datasize):
        transferTime = datasize / self.transferRate
        transferTime = transferTime * math.pow(10, 6)
        return transferTime

    def calculateComsumedEnergy(self, datasize):
        energy = self.calculatePower() * self.calculateTransferTime(datasize)
        return energy
