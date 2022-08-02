import math
import random

import numpy as np
import numpy.random as nr
from sklearn.preprocessing import minmax_scale

from Application import Application
from IIoTDevice import IIoTDevice
from MECServer import MECServer
from task import Task
from service import Service
from proposed_double_auction import doubleAuction
from proposed_DTS import proposed_DTS

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

		# discount factor
		gamma_PDTS = 0.99
		gamma_DTS = 0.99
		gamma_DUCB = 0.99
		gamma_gaussian = 0.99
		appList = dict()

		taskGenerationRate = 10 * math.pow(10, 4)
		taskDataEntrySize = 36.288 *8 * math.pow(10, 6)
		taskResultSize = math.pow(10, 4)
		computationalLoadCPUCycles = 20 * math.pow(10, 4)
		deadlineCriticalTasks = 0.5 * math.pow(10, 6)
		percentageOfCriticalTasks = 0.1

		appList['APP1'] = {'taskGen':taskGenerationRate,'taskDataSize':taskDataEntrySize,'taskResultSize':taskResultSize,'computationalLoadCycle':computationalLoadCPUCycles,'percentageOfCriticalTask':percentageOfCriticalTasks,'deadlineCriticaltask':deadlineCriticalTasks}
		applicaton1 = Application()
		applicaton2 = Application()
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
		D2Dlink_1 = []
		D2Dlink_1_IRD = []
		D2Dlink_1_ISD = []
		D2Dlink_2 = []
		D2Dlink_2_IRD = []
		D2Dlink_2_ISD = []
		MECoffloading = []
		Bandwidth = 100

		while systemTime != 100:
			# ---------------------------------------------------------------------------
			#  1. Initiates simulation
			# ---------------------------------------------------------------------------
			if systemTime == 0:
				rateOfGeneratedTasks = 12#applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(NumberOfIoT, rateOfGeneratedTasks, D2Dlink_1_IRD, D2Dlink_2_IRD)
				MEC = MECServer()
				MEC_temp = MEC.MECserver(1)
				A = IIoT.getPosition()
				print(A.count(1),A.count(2),A.count(3))
				print(len(IIoT.getRoleIIoT()))
				for i in range(2, (NumberOfIoT - 2)):
					if IIoT.getPosition()[i] == 1:
						D2Dlink_1.append(IIoT.getId()[i])
						if IIoT.getRoleIIoT()[i] == 'IRD':
							D2Dlink_1_IRD.append(IIoT.getId()[i])
						else:
							D2Dlink_1_ISD.append(IIoT.getId()[i])
					elif IIoT.getPosition()[i] == 2:
						D2Dlink_2.append(IIoT.getId()[i])
						if IIoT.getRoleIIoT()[i] == 'IRD':
							D2Dlink_2_IRD.append(IIoT.getId()[i])
						else:
							D2Dlink_2_ISD.append(IIoT.getId()[i])
					else:
						MECoffloading.append(IIoT.getId()[i])
			elif systemTime == subSystemTime:
				rateOfGeneratedTasks = applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(NumberOfIoT, rateOfGeneratedTasks,D2Dlink_1_IRD,D2Dlink_2_IRD)
			else:
				print("나머지 작업 처리")
				#나머지
			# ---------------------------------------------------------------------------
			# 2. Tasks are created
			# ---------------------------------------------------------------------------
			self.app = applicaton1.application('app1', taskGenerationRate, taskDataEntrySize, taskResultSize,
											   computationalLoadCPUCycles, percentageOfCriticalTasks,
											   deadlineCriticalTasks,D2Dlink_1_IRD)
			self.app2 = applicaton2.application('app2', taskGenerationRate, taskDataEntrySize, taskResultSize,
											   computationalLoadCPUCycles, percentageOfCriticalTasks,
											   deadlineCriticalTasks, D2Dlink_2_IRD)
			self.task_D2D1 = Task()
			self.task_D2D2 = Task()
			print(D2Dlink_1_ISD)
			self.task_D2D1.Task(D2Dlink_1_IRD,applicaton1.getCriticalTaskDeadline(), systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
			self.task_D2D2.Task(D2Dlink_2_IRD,applicaton2.getCriticalTaskDeadline(), systemTime,applicaton2.getComputaionWorkload(),applicaton2.getDataEntrySize(),applicaton2.getResultSize())


			self.service_D2D1 = Service()
			self.service_D2D2 = Service()
			self.service_D2D1.Service(D2Dlink_1_ISD,applicaton1.getCriticalTaskDeadline(), systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
			self.service_D2D2.Service(D2Dlink_2_ISD,applicaton2.getCriticalTaskDeadline(), systemTime,applicaton2.getComputaionWorkload(),applicaton2.getDataEntrySize(),applicaton2.getResultSize())
			print(D2Dlink_1_IRD)
			print(self.service_D2D1.getAsk())

			# ---------------------------------------------------------------------------
			# 3. Double Auction is started
			# ---------------------------------------------------------------------------
			D2D1_doubleauction_IRDcandidate, D2D1_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(D2Dlink_1_IRD, D2Dlink_1_ISD,1)
			D2D2_doubleauction_IRDcandidate, D2D2_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(D2Dlink_2_IRD, D2Dlink_2_ISD,2)
			print(D2D1_doubleauction_IRDcandidate)

			self.temp_doubleAuction = doubleAuction()
			win_IRD, self.win_ISD, bid_price, ask_price, K, remainingIRD = self.temp_doubleAuction.doubleAuction(D2D1_doubleauction_IRDcandidate,D2D1_doubleauction_ISDcandidate)

			# ---------------------------------------------------------------------------
			# 4. Multi-Armed Bandit is started
			# ---------------------------------------------------------------------------
			answerOfwinIRD = self.MABanswer()
			print("엉",answerOfwinIRD)
			opt_ISD = proposed_DTS(answerOfwinIRD,gamma_PDTS)
			print('어엉',opt_ISD)
			for index, (key, value) in enumerate(answerOfwinIRD.items()):
				answerOfwinIRD[key] = {'mabResult': opt_ISD[index]}
			sorting_opt_ISD = dict(sorted(answerOfwinIRD.items(), key=lambda x: x[1]['mabResult'],reverse=True))

			# ---------------------------------------------------------------------------
			# 5. Matching IRD and ISD
			# ---------------------------------------------------------------------------
			sortingWinIRD = dict()
			for index,(key,value) in enumerate(win_IRD.items()):
				for i in range(len(self.task_D2D1.getDeviceId())):
					if key == self.task_D2D1.getDeviceId()[i]:
						sortingWinIRD[key] = {'dataSize': self.task_D2D1.getEntryDataSize()[i],'computationWorkload':self.task_D2D1.getCompLoad()[i],'deadlineLatency':self.task_D2D1.getDeadline()[i]}
						sortingWinIRD[key] = {'order': sortingWinIRD[key]['dataSize'] * sortingWinIRD[key]['computationWorkload']}
						continue
			sortedWinIRD = dict(sorted(sortingWinIRD.items(),key=lambda x: x[1]['order'], reverse=True))
			sortedWinIRDID = list(sortedWinIRD.keys())

			matchList = [[0 for n in range(2)] for m in range(len(sorting_opt_ISD))]
			for index,(key,value) in enumerate(sorting_opt_ISD.items()):
				matchList[index][0] = sortedWinIRDID[index]
				matchList[index][1] = key
			print('후후',matchList)
			# scheduler_temp = scheduler()
			# Scheduler_D2D1 = scheduler_temp.sheduler(task_D2D1, coefficientEnergy, coefficientTime, alpha,beta,gamma,IIoT,MEC)
			# scheduler_temp = scheduler()
			# Scheduler_D2D2 = scheduler_temp.sheduler(task_D2D2, coefficientEnergy, coefficientTime, alpha, beta, gamma, IIoT,MEC)

			systemTime += 1

	def MABanswer(self):
		ISD_BW = 10 / len(self.win_ISD)
		signal = nr.normal(1, 0, len(self.win_ISD))
		channelGain = nr.normal(1, 0, len(self.win_ISD))
		noise = self.awgn(signal)
		temp_importance = []
		for index, (key, value) in enumerate(self.win_ISD.items()):
			SNR = ((channelGain[index] ** 2) * ISD_BW) / (noise[index] ** 2)
			self.win_ISD[key] = {'importance': ISD_BW * np.log2(1 + SNR)}
			temp_importance.append(ISD_BW * np.log2(1 + SNR))

		temp_importance = minmax_scale(temp_importance)
		for i in range(len(temp_importance)):
			if temp_importance[i] > 1:
				temp_importance[i] = 1
			elif temp_importance[i] < 0:
				temp_importance[i] = 0
			else:
				continue
		for index,(key,value) in enumerate(self.win_ISD.items()):
			self.win_ISD[key] = temp_importance[index]

		return self.win_ISD

	def awgn(self,sinal):
		regsnr = 54
		sigpower = sum([math.pow(abs(sinal[i]), 2) for i in range(len(sinal))])
		print(sigpower)
		sigpower = sigpower / len(sinal)
		noisepower = sigpower / (math.pow(10, regsnr / 10))
		noise = math.sqrt(noisepower) * (np.random.uniform(-1, 1, size=len(sinal)))
		print(noise)
		return noise

	def matchRoleForDoubleAuction(self,D2Dlink_IRD,D2Dlink_ISD,link):
		D2D_doubleauction_IRDcandidate = dict()
		D2D_doubleauction_ISDcandidate = dict()
		if link == 1:
			task = self.task_D2D1
			service = self.service_D2D1
		else:
			task = self.task_D2D2
			service = self.service_D2D2
		j = 0
		for i in D2Dlink_IRD:
			D2D_doubleauction_IRDcandidate[i] = {'bid': task.getBid()[j]}
			j += 1
		j = 0
		for i in D2Dlink_ISD:
			D2D_doubleauction_ISDcandidate[i] = {'ask': service.getAsk()[j]}
			j += 1
		return D2D_doubleauction_IRDcandidate, D2D_doubleauction_ISDcandidate




						# while systemTime == 1000:
						# 	for i in range(numberIoT):
						# 		print(IIoT.getBaseTime()[i],applicaton1.getRateGenerate(),"비교")
						# 		if ((systemTime - IIoT.getBaseTime()[i]) % int(applicaton1.getRateGenerate())) == 0:
						# 			task_temp = Task()
						# 			newTask = task_temp.Task("TarefaDummy","DeviceDummy",-1,0,0,0,0)
						# 			print(numberTasks,"ㅇ태스크수여")
						# 			if numberCreatedTasks < numberTasks:
						# 				print(numberCreatedTasks,"음ㄴ이루ㅏㅣㅁㄴㅇㄻㄴㅇ")
						# 				if applicaton1.defineInTaskIsCritical(numberCreatedTasks) == True:
						# 					newTask = task_temp.Task("task"+str(numberCreatedTasks), IIoT.getId()[i], applicaton1.getCriticalTaskDeadline(), systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
						# 				else:
						# 					newTask = task_temp.Task("task"+str(numberCreatedTasks), IIoT.getId()[i], -1, systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
						# 				numberCreatedTasks += 1
						# 			else:
						# 				break
						# 			scheduler_temp = scheduler()
						# 			Scheduler = scheduler_temp.sheduler(task_temp, coefficientEnergy, coefficientTime, alpha,beta,gamma,IIoT,MEC)
						#
						# 			flagIoTDevice = False
						# 			if IIoT.verifyCPUFree(i) == True:
						# 				flagIoTDevice = True
						#
						# 			flagMec = False
						# 			print(MEC.getStatusCOU(),"뿐ㅇ")
						# 			if numberMEC == 1:
						# 				if MEC.verifyCPUFree() == True:
						# 					flagMec = True
						# 					break
						# 			else:
						# 				for k in range(numberMEC):
						# 					if MEC.verifyCPUFree2(k) == True:
						# 						flagMec = True
						# 						break
						#
						# 			octet = scheduler_temp.defineAllocationPolicy(flagIoTDevice,flagMec)
						#
						# 			if octet[7] == self.POLICY_IIOT:
						# 				IIoT.alterCPUStatus(self.CORE_OCCUPIED)[i]
						# 				IIoT.consumeBattery(octet[1] + octet[2])[i]
						# 				# self.listOfIIoTDevice[i].alterCPUStatus(self.CORE_OCCUPIED)
						# 				# self.listOfIIoTDevice[i].consumeBattery(octet[1] + octet[2])
						# 			elif octet[7] == self.POLICY_MEC:
						# 				for k in range(numberMEC):
						# 					if MEC.verifyCPUFree()[k] == True:
						# 						MEC.occupyCPU()[k]
						# 						break
						#
						# 			newTask.setExeEnery(octet[1])
						# 			newTask.setTransferEnergy(octet[2])
						# 			newTask.setEXETime(octet[3])
						# 			newTask.setTransferTime(octet[4])
						# 			newTask.setPolicy(octet[7])
						#
						# 			if False:
						# 				print("기기 리스트아이디, 배터리레벨, cpufree?")
						# 			listRunningTask.extend(newTask)
						#
						# 			if False:
						# 				print("dlrjsms ")
						#
						# 	if listRunningTask:
						# 		listRunningTaskAux = []
						# 		listRunningTaskAux.extend(listRunningTask)
						# 		for k in range(listRunningTaskAux):
						#
						# 			task = Task.Task(k)
						# 			if task.verifyTaksFinish(systemTime) == True:
						# 				listFinishedTask[numberTasksCanceledAndConcluded] = task
						# 				numberTasksCanceledAndConcluded += 1
						# 				listRunningTask.remove(k)
						#
						# 				if task.getPolicy() == self.POLICY_IIOT:
						# 					id = task.getIdDeviceGenerator()
						# 					listOfIIoTDevice[id].alterCPUstatus(self.CORE_FREE)
						# 				if task.getPolicy() == self.POLICY_MEC:
						# 					for k in range(numberMEC):
						# 						if listOfMECServer[k].freeCPU() == True:
						# 							break
						# 				if True:
						# 					if numberTasksCanceledAndConcluded % 100 == 0:
						# 						print("number of task concluded")
						# 	if numberTasksCanceledAndConcluded ==  numberTasks:
						# 		if False:
						# 			for k in range(numberTasks):
						# 				print(listFinishedTasks[k].getIdTask(),"끝난 작업 목록")
						#
						# 	systemTime += 1
						# 	print(systemTime,"systemtime")
						# 	print(numberCreatedTasks,"numberCreatedTasks")


sim = SimulationEXE()
sim.main()

