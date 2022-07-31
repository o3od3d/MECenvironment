import math
from Application import Application
from IIoTDevice import IIoTDevice
from MECServer import MECServer
from task import Task
from scheduler import scheduler

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
		self.app = Application.application('app1',taskGenerationRate,taskDataEntrySize,taskResultSize,computationalLoadCPUCycles,percentageOfCriticalTasks,deadlineCriticalTasks)
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
		self.listOfIIoTDevice = []
		self.listOfMECServer = []
		for numberTasks in listNumberOfTasks:
			listRunningTask = []
			# listFinishedTask =
			for numberIoT in listNumberOfIoT:
				if numberIoT > numberTasks:
					continue
					for numberMEC in listNumberOfMEC:
						for j in list(appList):
							self.app.setNumberOfTask(numberTasks)

							coefficientEnergy = 4.0 / 5.0
							coefficientTime = 1 - coefficientEnergy

							alpha = bata = gamma = 1.0 / 3.0

							rateOfGeneratedTasks = self.app.getRateGenerate()



							for i in range(numberIoT):
								self.listOfIIoTDevice.append(IIoTDevice.IIoTdevice("iiot"+i,rateOfGeneratedTasks))

							for i in range(numberMEC):
								self.listOfMECServer.append(MECServer("mec"+i))

							systemTime = 0
							numberTasksCanceledAndConcluded = 0
							numberCreatedTasks = 0

							while True:
								for i in range(numberIoT):
									if ((systemTime - self.listOfIIoTDevice[i].getBaseTime()) % self.app.getRateGenerate()) == 0:
										newTask = Task.Task("TarefaDummy","DeviceDummy",-1,0,0,0,0)
										if numberCreatedTasks < numberTasks:
											if app.defineInTaskIsCritical(numberCreatedTasks) == True:
												newTask = Task.Task("task"+numberCreatedTasks, self.listOfIIoTDevice[i].getId(), self.app.getCriticalTaskDeadline(), systemTime,self.app.getComputaionWorkload(),self.app.getDataEntrySize(),self.app.getResultSize())
											else:
												newTask = 	Task.Task("task"+numberCreatedTasks, self.listOfIIoTDevice[i].getId(), -1, systemTime,self.app.getComputaionWorkload(),self.app.getDataEntrySize(),self.app.getResultSize())
											numberCreatedTasks += 1
										else:
											break

										scheduler = sheduler.scheduler(newTask, coefficientEnergy, coefficientTime, alpha,beta,gamma)

										flagIoTDevice = False
										if self.listOfIIoTDevice[i].verifyCPUFree() == True:
											flagIoTDevice = True

										flagMec = False
										for k in range(numberMEC):
											if self.listOfMECServer[k].verifyCPUFree() == True:
												flagMec = True
												break

										octet = scheduler.defineAllocationPolicy(flagIoTDevice,flagMec)

										if octet[7] == self.POLICY_IIOT:
											self.listOfIIoTDevice[i].alterCPUStatus(self.CORE_OCCUPIED)
											self.listOfIIoTDevice[i].consumeBattery(octet[1] + octet[2])
										elif octet[7] == self.POLICY_MEC:
											for k in range(numberMEC):
												if self.listOfMECServer[k].verifyCPUFree() == True:
													self.listOfMECServer[k].occupyCPU()
													break

										newTask.setExeEnery(octet[1])
										newTask.setTransferEnergy(octet[2])
										newTask.setEXETime(octet[3])
										newTask.setTransferTime(octet[4])
										newTask.setPolicy(octet[7])

										if False:
											print("기기 리스트아이디, 배터리레벨, cpufree?")
										listRunningTask.append(newTask)

										if False:
											print("dlrjsms ")

								if listRunningTask:







	if __name__ == '__main__':
		main()













