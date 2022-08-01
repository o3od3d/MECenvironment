import math
import numpy.random as nr

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
		applicaton1 = Application()
		self.app = applicaton1.application('app1',taskGenerationRate,taskDataEntrySize,taskResultSize,computationalLoadCPUCycles,percentageOfCriticalTasks,deadlineCriticalTasks)
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
		print(applicaton1.getID(),"우잉")
		listNumberOfTasks = [500, 5000]
		NumberOfIoT = 150
		listNumberOfMEC = [1]
		listOfIIoTDevice = []
		self.listOfMECServer = []
		systemTime = 0
		numberOfTaskFailure = 0
		subSystemTime = 500
		numberCreatedTasks = 0
		numberSuccessTasks = 0
		count1 = 0
		count2 = 0
		count3 = 0
		while systemTime != 800:
			if systemTime == 0:
				rateOfGeneratedTasks = applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(NumberOfIoT, rateOfGeneratedTasks)
				MEC = MECServer()
				MEC_temp = MEC.MECserver(1)
				task_temp = Task()
				print(IIoT.getPosition())
				print(IIoT.getPosition().count(1))
				print(IIoT.getPosition().count(2))
				print(IIoT.getPosition().count(3))
				print(IIoT.getRoleIIoT())
				print(IIoT.getRoleIIoT().count('IRD'))
				print(IIoT.getRoleIIoT().count('ISD'))
			elif systemTime == subSystemTime:
				rateOfGeneratedTasks = applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(NumberOfIoT, rateOfGeneratedTasks)

			systemTime += 1



		#
		# for numberTasks in listNumberOfTasks:
		# 	listRunningTask = []
		# 	listFinishedTask = []
		# 	print("numberTasks :",numberTasks)
		# 	for numberIoT in listNumberOfIoT:
		# 		print("numberIIOT",numberIoT)
		# 		if numberIoT > numberTasks:
		# 			continue
		# 		for numberMEC in listNumberOfMEC:
		# 			print("numberMEC",numberMEC)
		# 			for j in list(appList):
		# 				#self.app.setNumberOfTask(numberTasks)
		# 				print("sdfasdfasdfad")
		# 				applicaton1.setNumberOfTask(numberTasks)
		# 				print(applicaton1.getNumberOfTask(),"ㅅㅁ나tn")
		# 				coefficientEnergy = 4.0 / 5.0
		# 				coefficientTime = 1 - coefficientEnergy
		# 				print(coefficientTime,"time")
		# 				alpha = 1.0 / 3.0
		# 				beta = 1.0 / 3.0
		# 				gamma = 1.0 / 3.0
		#
		# 				rateOfGeneratedTasks = applicaton1.getRateGenerate()
		# 				print(rateOfGeneratedTasks,"rateOfGenerateTasks")
		#
		# 				IIoT = IIoTDevice()
		# 				IIoT_temp = IIoT.IIoTdevice(numberIoT,rateOfGeneratedTasks)
		#
		# 				MEC = MECServer()
		# 				MEC_temp = MEC.MECserver(numberMEC)
		# 				for i in range(numberIoT):
		# 					IIoT = IIoTDevice()
		# 					IIoT_temp = IIoT.IIoTdevice("IIoT"+str(i),rateOfGeneratedTasks)
		# 					listOfIIoTDevice.append(IIoT.getId())
		# 					print(IIoT.getBaseTime(),"LISTiiOT")
		# 				for i in range(numberIoT):
		# 					if IIoT.getId() == "IIoT1":
		# 						print(IIoT.getBaseTime(),"결과")
		# 				for i in range(numberMEC):
		# 					self.listOfMECServer.append(MECServer("mec"+i))
		# 					print(self.listOfMECServer,"listMEC")
		#
		# 				systemTime = 0
		# 				numberTasksCanceledAndConcluded = 0
		# 				numberCreatedTasks = 0

						while systemTime == 1000:
							for i in range(numberIoT):
								print(IIoT.getBaseTime()[i],applicaton1.getRateGenerate(),"비교")
								if ((systemTime - IIoT.getBaseTime()[i]) % int(applicaton1.getRateGenerate())) == 0:
									task_temp = Task()
									newTask = task_temp.Task("TarefaDummy","DeviceDummy",-1,0,0,0,0)
									print(numberTasks,"ㅇ태스크수여")
									if numberCreatedTasks < numberTasks:
										print(numberCreatedTasks,"음ㄴ이루ㅏㅣㅁㄴㅇㄻㄴㅇ")
										if applicaton1.defineInTaskIsCritical(numberCreatedTasks) == True:
											newTask = task_temp.Task("task"+str(numberCreatedTasks), IIoT.getId()[i], applicaton1.getCriticalTaskDeadline(), systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
										else:
											newTask = task_temp.Task("task"+str(numberCreatedTasks), IIoT.getId()[i], -1, systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
										numberCreatedTasks += 1
									else:
										break
									scheduler_temp = scheduler()
									Scheduler = scheduler_temp.sheduler(task_temp, coefficientEnergy, coefficientTime, alpha,beta,gamma,IIoT,MEC)

									flagIoTDevice = False
									if IIoT.verifyCPUFree(i) == True:
										flagIoTDevice = True

									flagMec = False
									print(MEC.getStatusCOU(),"뿐ㅇ")
									if numberMEC == 1:
										if MEC.verifyCPUFree() == True:
											flagMec = True
											break
									else:
										for k in range(numberMEC):
											if MEC.verifyCPUFree2(k) == True:
												flagMec = True
												break

									octet = scheduler_temp.defineAllocationPolicy(flagIoTDevice,flagMec)

									if octet[7] == self.POLICY_IIOT:
										IIoT.alterCPUStatus(self.CORE_OCCUPIED)[i]
										IIoT.consumeBattery(octet[1] + octet[2])[i]
										# self.listOfIIoTDevice[i].alterCPUStatus(self.CORE_OCCUPIED)
										# self.listOfIIoTDevice[i].consumeBattery(octet[1] + octet[2])
									elif octet[7] == self.POLICY_MEC:
										for k in range(numberMEC):
											if MEC.verifyCPUFree()[k] == True:
												MEC.occupyCPU()[k]
												break

									newTask.setExeEnery(octet[1])
									newTask.setTransferEnergy(octet[2])
									newTask.setEXETime(octet[3])
									newTask.setTransferTime(octet[4])
									newTask.setPolicy(octet[7])

									if False:
										print("기기 리스트아이디, 배터리레벨, cpufree?")
									listRunningTask.extend(newTask)

									if False:
										print("dlrjsms ")

							if listRunningTask:
								listRunningTaskAux = []
								listRunningTaskAux.extend(listRunningTask)
								for k in range(listRunningTaskAux):

									task = Task.Task(k)
									if task.verifyTaksFinish(systemTime) == True:
										listFinishedTask[numberTasksCanceledAndConcluded] = task
										numberTasksCanceledAndConcluded += 1
										listRunningTask.remove(k)

										if task.getPolicy() == self.POLICY_IIOT:
											id = task.getIdDeviceGenerator()
											listOfIIoTDevice[id].alterCPUstatus(self.CORE_FREE)
										if task.getPolicy() == self.POLICY_MEC:
											for k in range(numberMEC):
												if listOfMECServer[k].freeCPU() == True:
													break
										if True:
											if numberTasksCanceledAndConcluded % 100 == 0:
												print("number of task concluded")
							if numberTasksCanceledAndConcluded ==  numberTasks:
								if False:
									for k in range(numberTasks):
										print(listFinishedTasks[k].getIdTask(),"끝난 작업 목록")

							systemTime += 1
							print(systemTime,"systemtime")
							print(numberCreatedTasks,"numberCreatedTasks")


sim = SimulationEXE()
sim.main()

