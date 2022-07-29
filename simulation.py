import math


class SimulationEXE():

	def __init__(self):
		self.CORE_FREE = 1
		self.CORE_OCCUPIED = 2

		self.POLICY_IIOT = 1
		self.POLICY_MEC = 2
		self.POLICY_CLOUD = 3

		self.TASK_ALIVE = 1
		self.TASK_CONCLUDED = 2
		self.TASK_CANCELED = 3

	def main(self):
		appList = dict()

		taskGenerationRate = 10 * math.pow(10, 4)
		taskDataEntrySize = 36.288 *8 * math.pow(10, 6)
		taskResultSize = math.pow(10, 4)
		computationalLoadCPUCycles = 20 * math.pow(10, 4)
		deadlineCriticalTasks = 0.5 * math.pow(10, 6)
		percentageOfCriticalTasks = 0.1

		appList['APP1'] = {'taskGen':taskGenerationRate,'taskDataSize':taskDataEntrySize,'taskResultSize':taskResultSize,'computationalLoadCycle':computationalLoadCPUCycles,'percentageOfCriticalTask':percentageOfCriticalTasks,'deadlineCriticaltask':deadlineCriticalTasks}

		# taskGenerationRate = 0.1 * math.pow(10, 6)
		# taskDataEntrySize = 4 * 8 * math.pow(10, 6)
		# taskResultSize = 5 * math.pow(10, 3)
		# computationalLoadCPUCycles = 200 * math.pow(10, 6)
		# deadlineCriticalTasks = 0.1 * math.pow(10, 6)
		# percentageOfCriticalTasks = 0.5
		#
		# appList['APP2'] = {'taskGen': taskGenerationRate, 'taskDataSize': taskDataEntrySize,
		# 				   'taskResultSize': taskResultSize, 'computationalLoadCycle': computationalLoadCPUCycles,
		# 				   'percentageOfCriticalTask': percentageOfCriticalTasks,
		# 				   'deadlineCriticaltask': deadlineCriticalTasks}

		listNumberOfTasks = [500, 5000]
		listNumberOfIoT = [100, 500, 1000]
		listNumberOfMEC = [1, 2]

		for numberTasks in listNumberOfTasks:
			# listRunningTask =
			# listFinishedTask =
			for numberIoT in listNumberOfIoT:
				if numberIoT > numberTasks:
					continue
					# for numberMEC in listNumberOfMEC:
					# 	for key,value in list(appList):

	if __name__ == '__main__':
		main()
