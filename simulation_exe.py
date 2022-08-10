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
		sortedMECoffloadingDict = dict()
		taskGenerationRate = 10 * math.pow(10, 4)
		taskDataEntrySize = 36.288 * 8 * math.pow(10, 6)
		taskResultSize = math.pow(10, 4)
		computationalLoadCPUCycles = 20 * math.pow(10, 4)
		deadlineCriticalTasks = 0.5 * math.pow(10, 6)
		percentageOfCriticalTasks = 0.1
		numberTasksCanceledAndConcludedD2D = 0
		numberTasksCanceledAndConcludedMEC = 0
		processingTaskD2D = []
		processingTaskMEC = []
		remainMECoffloading = []
		completeTaskD2DIRD = []
		completeTaskD2DISD = []
		remainD2Dlink_1_IRD = []
		remainD2Dlink_1_ISD = []
		remainD2Dlink_2_IRD = []
		remainD2Dlink_2_ISD = []
		numberOffailureTask = 0

		completeTaskMEC = []
		NumberOfIoT = 80
		totalRound = 100
		self.proposed_DTS = proposed_DTS(NumberOfIoT,totalRound)
		appList['APP1'] = {'taskGen':taskGenerationRate,'taskDataSize':taskDataEntrySize,'taskResultSize':taskResultSize,'computationalLoadCycle':computationalLoadCPUCycles,'percentageOfCriticalTask':percentageOfCriticalTasks,'deadlineCriticaltask':deadlineCriticalTasks}
		applicaton1 = Application()
		applicaton2 = Application()
		applicaton3 = Application()
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
		totalRemain = []
		remainTaskDataSize = []
		remainTaskCOMP = []
		totalRemain2 = []
		remainTaskDataSize2 = []
		remainTaskCOMP2 = []
		totalRemainMEC = []
		remainTaskDataSizeMEC = []
		remainTaskCOMPMEC = []
		Bandwidth = 100
		MECoffloadingDict = {i: {'Policy': 0} for i in MECoffloading}
		CloudOffloading = []
		remainD2Dlink_1_IRD = []
		remainD2Dlink_2_IRD = []
		self.task_D2D1 = Task()
		self.task_D2D2 = Task()
		self.task_MEC = Task()
		self.service_D2D1 = Service()
		self.service_D2D2 = Service()
		remainBid_D2D1 = dict()
		remainStatus_D2D1 = dict()
		remainBid_D2D2 = dict()
		remainStatus_D2D2 = dict()
		remainBid_MEC = dict()
		remainStatus_MEC = dict()
		remainAsk_D2D1 = dict()
		remainAsk_D2D2 = dict()
		remainStauts_D2D1_ISD = dict()
		remainStauts_D2D2_ISD = dict()
		matchList = [[]]
		MECoffloading_already = []
		D2Dlink_1_already = []
		D2Dlink_2_already = []
		D2Dlink_1_IRD_already = []
		D2Dlink_1_ISD_already = []
		D2Dlink_2_IRD_already = []
		D2Dlink_2_ISD_already = []
		remainDeadlined2d1 = dict()
		remainDeadlined2d2 = dict()
		remainDeadlineMEC = dict()
		taskGenerateTimeD2D1 = dict()
		taskGenerateTimeD2D2 = dict()
		taskGenerateTimeMEC = dict()
		while systemTime != totalRound:
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
				MECoffloading_already = MECoffloading
				D2Dlink_1_already = D2Dlink_1
				D2Dlink_2_already = D2Dlink_2
				D2Dlink_1_IRD_already = D2Dlink_1_IRD
				D2Dlink_1_ISD_already = D2Dlink_1_ISD
				D2Dlink_2_IRD_already = D2Dlink_2_IRD
				D2Dlink_2_ISD_already = D2Dlink_2_ISD
				# taskGenerateTimeD2D1 = {i:systemTime for i in range(len(D2Dlink_1_IRD))}
				# taskGenerateTimeD2D2 = {i: systemTime for i in range(len(D2Dlink_2_IRD))}
				# taskGenerateTimeMEC = {i: systemTime for i in range(len(MECoffloading))}
			elif systemTime == subSystemTime:
				rateOfGeneratedTasks = applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(NumberOfIoT, rateOfGeneratedTasks,D2Dlink_1_IRD,D2Dlink_2_IRD)
			else:
				# D2D1
				remainD2Dlink_1_IRD = list(set(D2Dlink_1_IRD) - set(completeTaskD2DIRD))
				remainD2Dlink_1_ISD = list(set(D2Dlink_1_ISD) - set(completeTaskD2DISD))
				D2Dlink_1_IRD_already = list(set(D2Dlink_1_IRD) - set(remainD2Dlink_1_IRD))
				D2Dlink_1_ISD_already = list(set(D2Dlink_1_ISD) - set(remainD2Dlink_1_ISD))
				D2Dlink_1_already = D2Dlink_1_IRD_already + D2Dlink_1_ISD_already
				totalRemain = remainD2Dlink_1_IRD + remainD2Dlink_1_ISD
				completeTaskD2DIRD = []
				completeTaskD2DISD = []
				remainTaskDataSize = applicaton1.getDataEntrySize()
				remainTaskCOMP = applicaton1.getComputaionWorkload()

				# D2D2
				remainD2Dlink_2_IRD = list(set(D2Dlink_2_IRD) - set(completeTaskD2DIRD))
				remainD2Dlink_2_ISD = list(set(D2Dlink_2_ISD) - set(completeTaskD2DISD))
				D2Dlink_2_IRD_already = list(set(D2Dlink_2_IRD) - set(remainD2Dlink_2_IRD))
				D2Dlink_2_ISD_already = list(set(D2Dlink_2_ISD) - set(remainD2Dlink_2_ISD))
				D2Dlink_2_already = D2Dlink_2_IRD_already + D2Dlink_2_ISD_already
				# D2Dlink_2_IRD = completeTaskD2DIRD
				# D2Dlink_2_ISD = completeTaskD2DISD
				# D2Dlink_2 = D2Dlink_2_IRD + D2Dlink_2_ISD
				totalRemain2 = remainD2Dlink_2_IRD + remainD2Dlink_2_ISD
				completeTaskD2DIRD = []
				completeTaskD2DISD = []
				remainTaskDataSize2 = applicaton2.getDataEntrySize()
				remainTaskCOMP2 = applicaton2.getComputaionWorkload()

				# MEC
				totalRemainMEC = list(set(MECoffloading) - set(completeTaskMEC))
				MECoffloading_already = list(set(MECoffloading) - set(totalRemainMEC))
				completeTaskMEC = []
				remainTaskDataSizeMEC = applicaton3.getDataEntrySize()
				remainTaskCOMPMEC = applicaton3.getComputaionWorkload()
				print(applicaton2.getDataEntrySize())
				print(applicaton2.getComputaionWorkload())
				print("나머지 작업 처리")
				#나머지
			# ---------------------------------------------------------------------------
			# 2. Tasks are created
			# ---------------------------------------------------------------------------
			self.app = applicaton1.application('app1', taskGenerationRate, taskDataEntrySize, taskResultSize,
											   computationalLoadCPUCycles, percentageOfCriticalTasks,
											   remainDeadlined2d1,D2Dlink_1_already,totalRemain,remainTaskDataSize,remainTaskCOMP)
			self.app2 = applicaton2.application('app2', taskGenerationRate, taskDataEntrySize, taskResultSize,
											   computationalLoadCPUCycles, percentageOfCriticalTasks,
											   remainDeadlined2d2, D2Dlink_2_already,totalRemain2,remainTaskDataSize2,remainTaskCOMP2)
			self.app3 = applicaton3.application('app3', taskGenerationRate, taskDataEntrySize, taskResultSize,
												computationalLoadCPUCycles, percentageOfCriticalTasks,
												remainDeadlineMEC, MECoffloading_already,totalRemainMEC,remainTaskDataSizeMEC,remainTaskCOMPMEC)
			remainDeadlined2d1 = applicaton1.getCriticalTaskDeadline()
			remainDeadlined2d2 = applicaton2.getCriticalTaskDeadline()
			remainDeadlineMEC = applicaton3.getCriticalTaskDeadline()
			print("dfasdfasdfasd",remainDeadlined2d1)

			self.task_D2D1.Task(D2Dlink_1_IRD_already,remainD2Dlink_1_IRD,remainBid_D2D1,remainStatus_D2D1,applicaton1.getCriticalTaskDeadline(), taskGenerateTimeD2D1,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize(),systemTime)
			self.task_D2D2.Task(D2Dlink_2_IRD_already,remainD2Dlink_2_IRD,remainBid_D2D2,remainStatus_D2D2,applicaton2.getCriticalTaskDeadline(), taskGenerateTimeD2D2,applicaton2.getComputaionWorkload(),applicaton2.getDataEntrySize(),applicaton2.getResultSize(),systemTime)
			self.task_MEC.Task(MECoffloading_already, totalRemainMEC,remainBid_MEC,remainStatus_MEC,applicaton3.getCriticalTaskDeadline(), taskGenerateTimeMEC,
								applicaton3.getComputaionWorkload(), applicaton3.getDataEntrySize(),
								applicaton3.getResultSize(),systemTime)
			self.task_D2D1.setPolicy(1,D2Dlink_1_IRD_already)
			print("dsfasdfasdf",len(D2Dlink_1_IRD_already),D2Dlink_1_IRD_already)
			print(len(D2Dlink_1_IRD),D2Dlink_1_IRD)
			print(len(remainD2Dlink_1_IRD),remainD2Dlink_1_IRD)
			print(len(self.task_D2D1.getDeviceId()),self.task_D2D1.getDeviceId())
			print(len(totalRemainMEC),totalRemainMEC)
			print(len(MECoffloading_already),MECoffloading_already)
			remainBid_D2D1 = self.task_D2D1.getBid()
			remainStatus_D2D1 = self.task_D2D1.getTaskStatus()
			remainBid_D2D2 = self.task_D2D2.getBid()
			remainStatus_D2D2 = self.task_D2D2.getTaskStatus()
			remainBid_MEC = self.task_MEC.getBid()
			remainStatus_MEC = self.task_MEC.getTaskStatus()
			taskGenerateTimeD2D1 = self.task_D2D1.getBaseTime()
			taskGenerateTimeD2D2 = self.task_D2D2.getBaseTime()
			taskGenerateTimeMEC = self.task_MEC.getBaseTime()


			self.service_D2D1.Service(D2Dlink_1_ISD_already,remainAsk_D2D1,remainStauts_D2D1_ISD,remainD2Dlink_1_ISD,applicaton1.getCriticalTaskDeadline(), systemTime,applicaton1.getComputaionWorkload(),applicaton1.getDataEntrySize(),applicaton1.getResultSize())
			self.service_D2D2.Service(D2Dlink_2_ISD_already,remainAsk_D2D2,remainStauts_D2D2_ISD,remainD2Dlink_2_ISD,applicaton2.getCriticalTaskDeadline(), systemTime,applicaton2.getComputaionWorkload(),applicaton2.getDataEntrySize(),applicaton2.getResultSize())
			remainStauts_D2D1_ISD = self.service_D2D1.getTaskStatus()
			remainStauts_D2D2_ISD = self.service_D2D2.getTaskStatus()
			remainAsk_D2D1 = self.service_D2D1.getAsk()
			remainAsk_D2D2 = self.service_D2D2.getAsk()
			# ---------------------------------------------------------------------------
			# 3. Double Auction is started
			# ---------------------------------------------------------------------------
			D2D1_doubleauction_IRDcandidate, D2D1_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(D2Dlink_1_IRD, D2Dlink_1_ISD,1)
			D2D2_doubleauction_IRDcandidate, D2D2_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(D2Dlink_2_IRD, D2Dlink_2_ISD,2)

			self.temp_doubleAuction = doubleAuction()
			win_IRD, self.win_ISD, bid_price, ask_price, K, remainingIRD = self.temp_doubleAuction.doubleAuction(D2D1_doubleauction_IRDcandidate,D2D1_doubleauction_ISDcandidate)
			print("얌",len(win_IRD),win_IRD)
			print(len(self.win_ISD),self.win_ISD)
			# ---------------------------------------------------------------------------
			# 4. Multi-Armed Bandit is started
			# ---------------------------------------------------------------------------
			answerOfwinIRD = self.MABanswer()
			if answerOfwinIRD == False:
				continue
			opt_ISD = self.proposed_DTS.proposed_DTS(answerOfwinIRD,gamma_PDTS)
			print("우에멘에에ㅔ에",opt_ISD)
			for index, (key, value) in enumerate(answerOfwinIRD.items()):
				answerOfwinIRD[key] = {'mabResult': opt_ISD[key]}
			sorting_opt_ISD = dict(sorted(answerOfwinIRD.items(), key=lambda x: x[1]['mabResult'],reverse=True))

			# ---------------------------------------------------------------------------
			# 5. Matching IRD and ISD
			# ---------------------------------------------------------------------------
			sortingWinIRD = dict()
			for index,(key,value) in enumerate(win_IRD.items()):
				for i in range(len(self.task_D2D1.getDeviceId())):
					if key == self.task_D2D1.getDeviceId()[i]:
						sortingWinIRD[key] = {'dataSize': self.task_D2D1.getEntryDataSize()[key],'computationWorkload':self.task_D2D1.getCompLoad()[key],'deadlineLatency':self.task_D2D1.getDeadline()[key]}
						print("sdfasdfasdf",self.task_D2D1.getEntryDataSize()[key])
						print(self.task_D2D1.getCompLoad()[key])
						print(sortingWinIRD[key]['dataSize'],sortingWinIRD[key]['computationWorkload'])
						sortingWinIRD[key] = {'order': sortingWinIRD[key]['dataSize'] * sortingWinIRD[key]['computationWorkload']}
						#continue
			#sortedWinIRD = dict(sorted(sortingWinIRD.items(),key=lambda x: x[1]['order'], reverse=True))
			sortedWinIRDID = list(sortingWinIRD.keys())
			print(self.task_D2D1.getDeviceId())

			matchList = [[0 for n in range(2)] for m in range(len(sorting_opt_ISD))]
			for index,(key,value) in enumerate(sorting_opt_ISD.items()):
				matchList[index][0] = sortedWinIRDID[index]
				matchList[index][1] = key
			print("sdflkasdnf", matchList)
			flagIoTDevice = False
			for index,(key,value) in enumerate(sorting_opt_ISD.items()):
				if IIoT.verifyCPUFree(key) == True:
					flagIoTDevice = True
					IIoT.alterCPUStatus(self.CORE_OCCUPIED,key)

			j = 0

			print("냐",self.task_MEC.getDeadline())
			temp_MECoffloading = totalRemainMEC + MECoffloading_already
			for i in temp_MECoffloading:
				MECoffloadingDict[i] = {'deadline':self.task_MEC.getDeadline()[i]}
				j += 1
			#sortedMECoffloadingDict = dict(sorted(MECoffloadingDict.items(), key=lambda x: x[1]['deadline']))
			print("야호",MECoffloadingDict)

			for i, j in list(MECoffloadingDict.items()):

				print(i)
				if MEC.occupyCPU(i) == True:
					MECoffloadingDict[i]['Policy'] = 2
					#MEC.occupyCPU()

				else:
					CloudOffloading.append(i)
					MECoffloadingDict[i]['Policy'] = 3

			# D2D Task
			for i in range(len(matchList)-1,-1,-1):
				if self.task_D2D1.verifyTaksFinish(systemTime,matchList[i][0]) == True:
					numberTasksCanceledAndConcludedD2D += 1
					IIoT.alterCPUStatus(self.CORE_FREE,matchList[i][1])
					completeTaskD2DIRD.append(matchList[i][0])
					completeTaskD2DISD.append(matchList[i][1])
					matchList.pop(i)

				else:
					processingTaskD2D.append(matchList[i])
					numberOffailureTask += 1
			temp_D2D1Offloading = remainD2Dlink_1_IRD + D2Dlink_1_IRD_already
			temp2_D2D1Offloading = [x for x in temp_D2D1Offloading if x not in completeTaskD2DIRD]
			for i in temp2_D2D1Offloading:
				if self.task_D2D1.checkTaskTime(systemTime,i) == True:
					completeTaskD2DIRD.append(i)
					numberOffailureTask += 1
					print(i)
				else:
					print('이게맞나',i)

			# for i in D2Dlink_1_IRD:
			# 	self.task_D2D1.finalizeTask(systemTime,i)
			# 	if self.task_D2D1.getTaskStatus()[i] == 3:
			# 		completeTaskD2DIRD.append(i)
			# 	print(self.task_D2D1.getTaskStatus()[i],"호로롤ㄹ",i)
			# 	print(systemTime,":",self.task_D2D1.getBaseTime()[i],'+',self.task_D2D1.getDeadline()[i])

			print('집가고싶다',MECoffloadingDict)
			# Server Task
			for key,value in list(MECoffloadingDict.items()):
				if value['Policy'] == 2:
					print("우씨",key)
					#print(self.task_MEC.verifyTaksFinish(systemTime,key))
					if self.task_MEC.verifyTaksFinish(systemTime,key) == True:
						numberTasksCanceledAndConcludedMEC += 1
						MEC.freeCPU()
						completeTaskMEC.append(key)
						MECoffloadingDict.pop(key)

					# elif self.task_MEC.verifyTaksFinish(systemTime,key) == False:
					# 	processingTaskMEC.append(key)
					# 	print("dsfasd",key)
				elif value['Policy'] == 3:
					if self.task_MEC.checkTaskTime(systemTime,key) == True:
						completeTaskMEC.append(key)
						print('ㅇㄴㄻ',key)
						numberOffailureTask += 1


			MECoffloadingDict.clear()
			#마지막에 TASK_CANCELLED횟수와 TASK_CONCLUDED 횟수 세기

			coefficientEnergy = 0.1
			coefficientTime = 0.9
			alpha, beta, gamma = 0.1, 0.1, 0.1
			# scheduler_temp = scheduler()
			# Scheduler_D2D1 = scheduler_temp.sheduler(self.task_D2D1, coefficientEnergy, coefficientTime, alpha,beta,gamma,IIoT,MEC)
			# scheduler_temp = scheduler()
			# Scheduler_D2D2 = scheduler_temp.sheduler(self.task_D2D2, coefficientEnergy, coefficientTime, alpha, beta, gamma, IIoT,MEC)


			temp_D2D1_FAIL = [x for x in temp_D2D1Offloading if x not in completeTaskD2DIRD]
			temp_MEC_FAIL = [x for x in MECoffloading if x not in completeTaskMEC]
			systemTime += 1
			if systemTime == totalRound:
				temp_fail = len(temp_D2D1_FAIL) + len(temp_MEC_FAIL)
				numberOffailureTask += temp_fail
				print(numberOffailureTask,temp_D2D1_FAIL,temp_MEC_FAIL)


	def MABanswer(self):
		if len(self.win_ISD) == 0:
			print("no winner")
		else:
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
		return False

	def awgn(self,sinal):
		regsnr = 54
		sigpower = sum([math.pow(abs(sinal[i]), 2) for i in range(len(sinal))])
		#print(sigpower)
		sigpower = sigpower / len(sinal)
		noisepower = sigpower / (math.pow(10, regsnr / 10))
		noise = math.sqrt(noisepower) * (np.random.uniform(-1, 1, size=len(sinal)))
		#print(noise)
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
			D2D_doubleauction_IRDcandidate[i] = {'bid': task.getBid()[i]}
			j += 1
		j = 0
		for i in D2Dlink_ISD:
			D2D_doubleauction_ISDcandidate[i] = {'ask': service.getAsk()[i]}
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

