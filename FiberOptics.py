import math


class FiberOptics():

    def __init__(self):
        print("hello fiberoptics")
        # self.latency
        # self.power
        # self.transferRate

    def FiberOptics(self):
        self.latency = 5 * math.pow(10, -3)
        self.power = 3.65
        self.transferRate = math.pow(10, 9)

    def calculateTransmissionTime(self, datasize):
        transmissionTime = datasize / self.transferRate
        transmissionTime = transmissionTime * math.pow(10, 6)
        return transmissionTime

    def calculateEnergyCon(self, datasize):
        energy = self.power * self.calculateTransmissionTime(datasize)
        return energy
