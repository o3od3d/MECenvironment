import math


class CloudDataCenter():

	def __init__(self):
		print("Hello cloud")
		# self.cloudId
		# self.standardFrequency
		# self.turboBoostFrequency

	def cloudServer(self,cloudId):
		self.cloudId = cloudId
		self.standardFrequency = (2.8 * math.pow(10, 9)) 	# Hz
		self.turboBoostFrequency = (3.8 * math.pow(10, 9))	# Hz

	def getId(self):
		return self.cloudId

	def getStandardFrequency(self):
		return self.standardFrequency

	def getTurboBoostFrequency(self):
		return self.turboBoostFrequency

	def calculateExecutionTimeStardardFreq(self, computationWorkload):
		time = computationWorkload / self.standardFrequency
		time = time * math.pow(10,6)
		return time

	def calculateDynamicEnergyStandardFreq(self, computationWorkload):
		energyDynamic = 13.85 * self.calculateExecutionTimeStardardFreq(computationWorkload)
		return energyDynamic

	def calculaTempoExecucaoFreqTurboBoost(self, computationWorkload):
		time = computationWorkload / self.turboBoostFrequency
		time = time * math.pow(10, 6)
		return time

	def calculateDynamicEnergyTurboFreq(self, computationWorkload):
		energyDynamic = 24.28 * self.calculaTempoExecucaoFreqTurboBoost(computationWorkload)
		return energyDynamic



