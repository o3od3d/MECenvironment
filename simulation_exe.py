import math
import random
import copy
import matplotlib.pyplot as plt
import time
import numpy as np
import numpy.random as nr
from sklearn.preprocessing import minmax_scale
import multiprocessing as mp
from IIoTDevice import IIoTDevice
from MECServer import MECServer
from task import Task
from service import Service
from proposed_double_auction import doubleAuction
from proposed_DTS import proposed_DTS
from no_double_auction import noDoubleAuction
from gaussianTS import gaussianTS
from discountedUCB import DUCB
from existing_DTS import exe_DTS


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
		start = time.time()
		print(start)

		# discount factor
		print(mp.cpu_count())
		gamma_PDTS = 0.99
		gamma_PDTS_D2D2 = 0.99
		gamma_DTS = 0.99
		gamma_DUCB = 0.99
		gamma_gaussian = 0.99
		gamma_gaussian_D2D2 = 0.99
		gamma_DUCB_D2D2 = 0.99
		appList = dict()
		sortedMECoffloadingDict = dict()
		self.taskGenerationRate = 10 * math.pow(10, 4)
		self.taskDataEntrySize = 36.288 * 8 * math.pow(10, 6)
		self.taskResultSize = math.pow(10, 4)
		self.computationalLoadCPUCycles = 20 * math.pow(10, 4)
		deadlineCriticalTasks = 0.5 * math.pow(10, 6)
		self.percentageOfCriticalTasks = 0.1
		numberTasksCanceledAndConcludedD2D1 = 0
		numberTasksCanceledAndConcludedD2D1_gauss = 0
		numberTasksCanceledAndConcludedD2D1_DUCB = 0
		numberTasksCanceledAndConcludedD2D2 = 0
		numberTasksCanceledAndConcludedD2D2_gauss = 0
		numberTasksCanceledAndConcludedD2D2_DUCB = 0
		numberTasksCanceledAndConcludedMEC = 0
		processingTaskD2D = []
		processingTaskMEC = []
		remainMECoffloading = []
		completeTaskD2DIRD = []
		completeTaskD2DIRD_gauss = []
		completeTaskD2DIRD_DUCB = []
		completeTaskD2DISD = []
		completeTaskD2DISD_gauss = []
		completeTaskD2DISD_DUCB = []
		completeTaskD2D2IRD = []
		completeTaskD2D2IRD_gauss = []
		completeTaskD2D2IRD_DUCB = []
		completeTaskD2D2ISD = []
		completeTaskD2D2ISD_gauss = []
		completeTaskD2D2ISD_DUCB = []
		remainD2Dlink_1_IRD = []
		remainD2Dlink_1_ISD = []
		remainD2Dlink_1_ISD_gauss = []
		remainD2Dlink_1_ISD_DUCB = []

		remainD2Dlink_2_ISD = []
		remainD2Dlink_2_ISD_gauss = []
		remainD2Dlink_2_ISD_DUCB = []
		numberOffailureTask = 0
		numberOffailureTask_gauss = 0
		numberOffailureTask_DUCB = 0

		completeTaskMEC = []
		self.NumberOfIoT = 100
		totalRound = 5000
		self.proposed_DTS = proposed_DTS(self.NumberOfIoT,totalRound)
		self.gaussianTS = gaussianTS(self.NumberOfIoT,totalRound)
		self.exe_DTS = exe_DTS(self.NumberOfIoT,totalRound)
		self.DUCB = DUCB(self.NumberOfIoT,totalRound)

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


		self.listOfMECServer = []
		systemTime = 0
		numberOfTaskFailure = 0
		subSystemTime = 10
		numberCreatedTasks = 0
		numberSuccessTasks = 0
		numberOfTaskD2D1 = 0
		numberOfTaskD2D2 = 0
		numberOfTaskMEC = 0
		numberOfTaskD2D1_gauss = 0
		numberOfTaskD2D2_gauss = 0
		numberOfTaskD2D1_DUCB = 0
		numberOfTaskD2D2_DUCB = 0

		self.D2Dlink_1 = []
		self.D2Dlink_1_IRD = []
		self.D2Dlink_1_ISD = []
		self.D2Dlink_2 = []
		self.D2Dlink_2_IRD = []
		self.D2Dlink_2_ISD = []
		self.MECoffloading = []
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
		MECoffloadingDict = {i: {'Policy': 0} for i in self.MECoffloading}
		CloudOffloading = []
		remainD2Dlink_1_IRD = []
		remainD2Dlink_2_IRD = []
		remainD2Dlink_2_IRD_gauss = []
		remainD2Dlink_1_IRD_gauss = []
		remainD2Dlink_2_IRD_DUCB = []
		remainD2Dlink_1_IRD_DUCB = []

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

		# gauss
		remainBid_D2D1_gauss = dict()
		remainStatus_D2D1_gauss = dict()
		remainBid_D2D2_gauss = dict()
		remainStatus_D2D2_gauss = dict()
		remainAsk_D2D1_gauss = dict()
		remainAsk_D2D2_gauss = dict()
		remainStauts_D2D1_ISD_gauss = dict()
		remainStauts_D2D2_ISD_gauss = dict()

		# DUCB
		remainBid_D2D1_DUCB = dict()
		remainStatus_D2D1_DUCB = dict()
		remainBid_D2D2_DUCB = dict()
		remainStatus_D2D2_DUCB = dict()
		remainAsk_D2D1_DUCB = dict()
		remainAsk_D2D2_DUCB = dict()
		remainStauts_D2D1_ISD_DUCB = dict()
		remainStauts_D2D2_ISD_DUCB = dict()

		# regret list
		regretSumOfPDTS = np.zeros(totalRound)
		regretSumOfPDTS_D2D2 = np.zeros(totalRound)
		regretSumOfGauss = np.zeros(totalRound)
		regretSumOfGauss_D2D2 = np.zeros(totalRound)
		regretSumOfDUCB = np.zeros(totalRound)
		regretSumOfDUCB_D2D2 = np.zeros(totalRound)

		# Utility list
		utilityOfIBD_D2D1 = np.zeros(totalRound)
		utilityOfIRD_D2D1 = np.zeros(totalRound)
		utilityOfISD_D2D1 = np.zeros(totalRound)
		utilityOfIBD_D2D2 = np.zeros(totalRound)
		utilityOfIRD_D2D2 = np.zeros(totalRound)
		utilityOfISD_D2D2 = np.zeros(totalRound)
		utilityOfIBD_D2D1_gauss = np.zeros(totalRound)
		utilityOfIRD_D2D1_gauss  = np.zeros(totalRound)
		utilityOfISD_D2D1_gauss  = np.zeros(totalRound)
		utilityOfIBD_D2D2_gauss = np.zeros(totalRound)
		utilityOfIRD_D2D2_gauss = np.zeros(totalRound)
		utilityOfISD_D2D2_gauss = np.zeros(totalRound)
		utilityOfIBD_D2D1_DUCB = np.zeros(totalRound)
		utilityOfIRD_D2D1_DUCB = np.zeros(totalRound)
		utilityOfISD_D2D1_DUCB = np.zeros(totalRound)
		utilityOfIBD_D2D2_DUCB = np.zeros(totalRound)
		utilityOfIRD_D2D2_DUCB = np.zeros(totalRound)
		utilityOfISD_D2D2_DUCB = np.zeros(totalRound)

		remainDeadlined2d1 = dict()
		remainDeadlined2d2 = dict()
		remainDeadlineMEC = dict()
		remainDataSizeD2D1 = dict()
		remainDataSizeD2D2 = dict()
		remainDataSizeMEC = dict()
		remainWorkLoadD2D1 = dict()
		remainWorkLoadD2D2 = dict()
		remainWorkLoadMEC = dict()
		taskGenerateTimeD2D1 = dict()
		taskGenerateTimeD2D2 = dict()
		taskGenerateTimeMEC = dict()
		computationCapD2D1 = dict()
		computationCapD2D2 = dict()

		# GAUSS
		remainDeadlined2d1_gauss = dict()
		remainDeadlined2d2_gauss = dict()
		remainDataSizeD2D1_gauss = dict()
		remainDataSizeD2D2_gauss = dict()
		remainWorkLoadD2D1_gauss = dict()
		remainWorkLoadD2D2_gauss = dict()
		taskGenerateTimeD2D1_gauss = dict()
		taskGenerateTimeD2D2_gauss = dict()
		computationCapD2D1_gauss = dict()
		computationCapD2D2_gauss = dict()

		# DUCB
		remainDeadlined2d1_DUCB = dict()
		remainDeadlined2d2_DUCB = dict()
		remainDataSizeD2D1_DUCB = dict()
		remainDataSizeD2D2_DUCB = dict()
		remainWorkLoadD2D1_DUCB = dict()
		remainWorkLoadD2D2_DUCB = dict()
		taskGenerateTimeD2D1_DUCB = dict()
		taskGenerateTimeD2D2_DUCB = dict()
		computationCapD2D1_DUCB = dict()
		computationCapD2D2_DUCB = dict()

		power = 0.2


		while systemTime != totalRound:
			print('time : ',systemTime,'낄낄',time.time() - start)
			# ---------------------------------------------------------------------------
			#  1. Initiates simulation
			# ---------------------------------------------------------------------------
			if systemTime == 0 or systemTime % subSystemTime == 0:
				if systemTime % subSystemTime == 0:
					remainD2Dlink_1_IRD_DUCB = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD_DUCB))
					remainD2Dlink_2_IRD_DUCB = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD_DUCB))
					remainD2Dlink_1_IRD_gauss = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD_gauss))
					remainD2Dlink_2_IRD_gauss = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD_gauss))
					remainD2Dlink_1_IRD = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD))
					remainD2Dlink_2_IRD = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD))
					totalRemainMEC = list(set(self.MECoffloading) - set(completeTaskMEC))
					numberOffailureTask += (len(totalRemainMEC) + len(remainD2Dlink_1_IRD) + len(remainD2Dlink_2_IRD))
					numberOffailureTask_gauss += (len(totalRemainMEC) + len(remainD2Dlink_1_IRD_gauss) + len(remainD2Dlink_2_IRD_gauss))
					numberOffailureTask_DUCB += (len(totalRemainMEC) + len(remainD2Dlink_1_IRD_DUCB) + len(remainD2Dlink_2_IRD_DUCB))
					print('남은작업', len(totalRemainMEC), totalRemainMEC)
					print('남은작업', len(remainD2Dlink_1_IRD_gauss), remainD2Dlink_1_IRD_gauss)
					print('남은작업', len(remainD2Dlink_2_IRD_gauss), remainD2Dlink_2_IRD_gauss)
					print('남은작업', len(remainD2Dlink_1_IRD_DUCB), remainD2Dlink_1_IRD_DUCB)
					print('남은작업', len(remainD2Dlink_2_IRD_DUCB), remainD2Dlink_2_IRD_DUCB)
					self.D2Dlink_1 = []
					self.D2Dlink_1_IRD = []
					self.D2Dlink_1_ISD = []
					self.D2Dlink_2 = []
					self.D2Dlink_2_IRD = []
					self.D2Dlink_2_ISD = []
					self.MECoffloading = []

					remainD2Dlink_1_IRD = []
					remainD2Dlink_1_ISD = []
					remainD2Dlink_2_IRD = []
					remainD2Dlink_2_ISD = []

					remainD2Dlink_1_IRD_gauss = []
					remainD2Dlink_1_ISD_gauss = []
					remainD2Dlink_2_IRD_gauss = []
					remainD2Dlink_2_ISD_gauss = []

					remainD2Dlink_1_IRD_DUCB = []
					remainD2Dlink_1_ISD_DUCB = []
					remainD2Dlink_2_IRD_DUCB = []
					remainD2Dlink_2_ISD_DUCB = []

					totalRemain = []
					totalRemain2 = []
					totalRemainMEC = []
				rateOfGeneratedTasks = 12  # applicaton1.getRateGenerate()
				IIoT = IIoTDevice()
				IIoT_temp = IIoT.IIoTdevice(self.NumberOfIoT, rateOfGeneratedTasks, self.D2Dlink_1_IRD, self.D2Dlink_2_IRD)
				MEC = MECServer()
				MEC_temp = MEC.MECserver(1)
				MECoffloading_already, D2Dlink_1_already,D2Dlink_2_already,D2Dlink_1_IRD_already,D2Dlink_1_ISD_already,D2Dlink_2_IRD_already,D2Dlink_2_ISD_already = self.initialization(IIoT)

				self.task_D2D1.Task(D2Dlink_1_IRD_already, remainD2Dlink_1_IRD, remainBid_D2D1,
														  remainStatus_D2D1, remainDeadlined2d1, taskGenerateTimeD2D1,
														  remainWorkLoadD2D1, remainDataSizeD2D1, self.taskResultSize,
														  systemTime)
				self.task_D2D2.Task(D2Dlink_2_IRD_already, remainD2Dlink_2_IRD, remainBid_D2D2,
														  remainStatus_D2D2, remainDeadlined2d2, taskGenerateTimeD2D2,
														  remainWorkLoadD2D2, remainDataSizeD2D2, self.taskResultSize,
														  systemTime)


				self.task_D2D1.setPolicy(1, D2Dlink_1_IRD_already)
				self.task_D2D2.setPolicy(1, D2Dlink_2_IRD_already)
				self.task_D2D1_gauss = copy.deepcopy(self.task_D2D1)
				self.task_D2D1_DUCB = copy.deepcopy(self.task_D2D1)
				self.task_D2D2_gauss = copy.deepcopy(self.task_D2D2)
				self.task_D2D2_DUCB = copy.deepcopy(self.task_D2D2)
				self.service_D2D1.Service(D2Dlink_1_ISD_already, remainAsk_D2D1, remainStauts_D2D1_ISD,
										  remainD2Dlink_1_ISD, remainDeadlined2d1, systemTime, computationCapD2D1,
										  remainDataSizeD2D1, self.task_D2D1.getReturnDataSize())
				self.service_D2D2.Service(D2Dlink_2_ISD_already, remainAsk_D2D2, remainStauts_D2D2_ISD,
										  remainD2Dlink_2_ISD, remainDeadlined2d2, systemTime, computationCapD2D2,
										  remainDataSizeD2D2, self.task_D2D2.getReturnDataSize())
				self.service_D2D1_gauss = copy.deepcopy(self.service_D2D1)
				self.service_D2D2_gauss = copy.deepcopy(self.service_D2D2)
				self.service_D2D1_DUCB = copy.deepcopy(self.service_D2D1)
				self.service_D2D2_DUCB = copy.deepcopy(self.service_D2D2)
				D2Dlink_1_IRD_already_gauss = copy.deepcopy(D2Dlink_1_IRD_already)
				D2Dlink_1_ISD_already_gauss = copy.deepcopy(D2Dlink_1_ISD_already)
				D2Dlink_2_IRD_already_gauss = copy.deepcopy(D2Dlink_2_IRD_already)
				D2Dlink_2_ISD_already_gauss = copy.deepcopy(D2Dlink_2_ISD_already)
				D2Dlink_1_already_gauss = copy.deepcopy(D2Dlink_1_already)
				D2Dlink_2_already_gauss = copy.deepcopy(D2Dlink_2_already)
				D2Dlink_1_IRD_already_DUCB = copy.deepcopy(D2Dlink_1_IRD_already)
				D2Dlink_1_ISD_already_DUCB = copy.deepcopy(D2Dlink_1_ISD_already)
				D2Dlink_2_IRD_already_DUCB = copy.deepcopy(D2Dlink_2_IRD_already)
				D2Dlink_2_ISD_already_DUCB = copy.deepcopy(D2Dlink_2_ISD_already)
				D2Dlink_1_already_DUCB = copy.deepcopy(D2Dlink_1_already)
				D2Dlink_2_already_DUCB = copy.deepcopy(D2Dlink_2_already)
				answerOfISD = self.MABanswer(D2Dlink_1_ISD_already,self.service_D2D1.getCompLoad())
				print('정답입니다',answerOfISD)
				answerOfISD_D2D2 = self.MABanswer(D2Dlink_2_ISD_already,self.service_D2D2.getCompLoad())
				print('정답입니다', answerOfISD_D2D2)
				# answerOfISD_gaussian = self.MABanswer()
				# answerOfISD_gaussian_D2D2 =
				# answerOfISD_DUCB =
				# answerOfISD_DUCB_D2D2

			else:
				# D2D 1
				remainD2Dlink_1_IRD = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD))
				remainD2Dlink_1_ISD = list(set(self.D2Dlink_1_ISD) - set(completeTaskD2DISD))
				D2Dlink_1_IRD_already = list(set(self.D2Dlink_1_IRD) - set(remainD2Dlink_1_IRD))
				D2Dlink_1_ISD_already = list(set(self.D2Dlink_1_ISD) - set(remainD2Dlink_1_ISD))
				D2Dlink_1_already = D2Dlink_1_IRD_already + D2Dlink_1_ISD_already
				totalRemain = remainD2Dlink_1_IRD + remainD2Dlink_1_ISD
				completeTaskD2DIRD = []
				completeTaskD2DISD = []

				# D2D 2
				remainD2Dlink_2_IRD = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD))
				remainD2Dlink_2_ISD = list(set(self.D2Dlink_2_ISD) - set(completeTaskD2D2ISD))
				D2Dlink_2_IRD_already = list(set(self.D2Dlink_2_IRD) - set(remainD2Dlink_2_IRD))
				D2Dlink_2_ISD_already = list(set(self.D2Dlink_2_ISD) - set(remainD2Dlink_2_ISD))
				D2Dlink_2_already = D2Dlink_2_IRD_already + D2Dlink_2_ISD_already
				# D2Dlink_2_IRD = completeTaskD2DIRD
				# D2Dlink_2_ISD = completeTaskD2DISD
				# D2Dlink_2 = D2Dlink_2_IRD + D2Dlink_2_ISD
				totalRemain2 = remainD2Dlink_2_IRD + remainD2Dlink_2_ISD
				completeTaskD2D2IRD = []
				completeTaskD2D2ISD = []
				# remainTaskDataSize2 = applicaton2.getDataEntrySize()
				# remainTaskCOMP2 = applicaton2.getComputaionWorkload()

				# D2D 1 -GAUSSIAN
				remainD2Dlink_1_IRD_gauss = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD_gauss))
				remainD2Dlink_1_ISD_gauss = list(set(self.D2Dlink_1_ISD) - set(completeTaskD2DISD_gauss))
				D2Dlink_1_IRD_already_gauss = list(set(self.D2Dlink_1_IRD) - set(remainD2Dlink_1_IRD_gauss))
				D2Dlink_1_ISD_already_gauss = list(set(self.D2Dlink_1_ISD) - set(remainD2Dlink_1_ISD_gauss))
				D2Dlink_1_already_gauss = D2Dlink_1_IRD_already_gauss + D2Dlink_1_ISD_already_gauss
				totalRemain_gauss = remainD2Dlink_1_IRD_gauss + remainD2Dlink_1_ISD_gauss
				completeTaskD2DIRD_gauss = []
				completeTaskD2DISD_gauss = []

				# D2D 2 -GAUSSIAN
				remainD2Dlink_2_IRD_gauss = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD_gauss))
				remainD2Dlink_2_ISD_gauss = list(set(self.D2Dlink_2_ISD) - set(completeTaskD2D2ISD_gauss))
				D2Dlink_2_IRD_already_gauss = list(set(self.D2Dlink_2_IRD) - set(remainD2Dlink_2_IRD_gauss))
				D2Dlink_2_ISD_already_gauss = list(set(self.D2Dlink_2_ISD) - set(remainD2Dlink_2_ISD_gauss))
				D2Dlink_2_already_gauss = D2Dlink_2_IRD_already_gauss + D2Dlink_2_ISD_already_gauss
				totalRemain2_gauss = remainD2Dlink_2_IRD_gauss + remainD2Dlink_2_ISD_gauss
				completeTaskD2D2IRD_gauss = []
				completeTaskD2D2ISD_gauss = []

				# D2D 1 -DUCB
				remainD2Dlink_1_IRD_DUCB = list(set(self.D2Dlink_1_IRD) - set(completeTaskD2DIRD_DUCB))
				remainD2Dlink_1_ISD_DUCB = list(set(self.D2Dlink_1_ISD) - set(completeTaskD2DISD_DUCB))
				D2Dlink_1_IRD_already_DUCB = list(set(self.D2Dlink_1_IRD) - set(remainD2Dlink_1_IRD_DUCB))
				D2Dlink_1_ISD_already_DUCB = list(set(self.D2Dlink_1_ISD) - set(remainD2Dlink_1_ISD_DUCB))
				D2Dlink_1_already_DUCB = D2Dlink_1_IRD_already_DUCB + D2Dlink_1_ISD_already_DUCB
				totalRemain_DUCB = remainD2Dlink_1_IRD_DUCB + remainD2Dlink_1_ISD_DUCB
				completeTaskD2DIRD_DUCB = []
				completeTaskD2DISD_DUCB = []

				# D2D 2 -DUCB
				remainD2Dlink_2_IRD_DUCB = list(set(self.D2Dlink_2_IRD) - set(completeTaskD2D2IRD_DUCB))
				remainD2Dlink_2_ISD_DUCB = list(set(self.D2Dlink_2_ISD) - set(completeTaskD2D2ISD_DUCB))
				D2Dlink_2_IRD_already_DUCB = list(set(self.D2Dlink_2_IRD) - set(remainD2Dlink_2_IRD_DUCB))
				D2Dlink_2_ISD_already_DUCB = list(set(self.D2Dlink_2_ISD) - set(remainD2Dlink_2_ISD_DUCB))
				D2Dlink_2_already_DUCB = D2Dlink_2_IRD_already_DUCB + D2Dlink_2_ISD_already_DUCB
				totalRemain2_DUCB = remainD2Dlink_2_IRD_DUCB + remainD2Dlink_2_ISD_DUCB
				completeTaskD2D2IRD_DUCB = []
				completeTaskD2D2ISD_DUCB = []

				# MEC
				totalRemainMEC = list(set(self.MECoffloading) - set(completeTaskMEC))
				MECoffloading_already = list(set(self.MECoffloading) - set(totalRemainMEC))
				completeTaskMEC = []
				# remainTaskDataSizeMEC = applicaton3.getDataEntrySize()
				# remainTaskCOMPMEC = applicaton3.getComputaionWorkload()
				self.task_D2D1.Task(D2Dlink_1_IRD_already, remainD2Dlink_1_IRD, remainBid_D2D1,
														  remainStatus_D2D1, remainDeadlined2d1, taskGenerateTimeD2D1,
														  remainWorkLoadD2D1, remainDataSizeD2D1, self.taskResultSize,
														  systemTime)
				self.task_D2D2.Task(D2Dlink_2_IRD_already, remainD2Dlink_2_IRD, remainBid_D2D2,
														  remainStatus_D2D2, remainDeadlined2d2, taskGenerateTimeD2D2,
														  remainWorkLoadD2D2, remainDataSizeD2D2, self.taskResultSize,
														  systemTime)
				self.task_D2D1_gauss.Task(D2Dlink_1_IRD_already_gauss,remainD2Dlink_1_IRD_gauss,remainBid_D2D1_gauss,remainStatus_D2D1_gauss,remainDeadlined2d1_gauss,taskGenerateTimeD2D1_gauss,remainWorkLoadD2D1_gauss,remainDataSizeD2D1_gauss,self.taskResultSize,systemTime)
				self.task_D2D2_gauss.Task(D2Dlink_2_IRD_already_gauss,remainD2Dlink_2_IRD_gauss,remainBid_D2D2_gauss,remainStatus_D2D2_gauss,remainDeadlined2d2_gauss,taskGenerateTimeD2D2_gauss,remainWorkLoadD2D2_gauss,remainDataSizeD2D2_gauss,self.taskResultSize,systemTime)
				self.task_D2D1_DUCB.Task(D2Dlink_1_IRD_already_DUCB, remainD2Dlink_1_IRD_DUCB, remainBid_D2D1_DUCB,
										  remainStatus_D2D1_DUCB, remainDeadlined2d1_DUCB, taskGenerateTimeD2D1_DUCB,
										  remainWorkLoadD2D1_DUCB, remainDataSizeD2D1_DUCB, self.taskResultSize,
										  systemTime)
				self.task_D2D2_DUCB.Task(D2Dlink_2_IRD_already_DUCB, remainD2Dlink_2_IRD_DUCB, remainBid_D2D2_DUCB,
										  remainStatus_D2D2_DUCB, remainDeadlined2d2_DUCB, taskGenerateTimeD2D2_DUCB,
										  remainWorkLoadD2D2_DUCB, remainDataSizeD2D2_DUCB, self.taskResultSize,
										  systemTime)

				self.task_D2D1.setPolicy(1, D2Dlink_1_IRD_already)
				self.task_D2D2.setPolicy(1, D2Dlink_2_IRD_already)
				self.task_D2D1_gauss.setPolicy(1, D2Dlink_1_IRD_already_gauss)
				self.task_D2D2_gauss.setPolicy(1, D2Dlink_2_IRD_already_gauss)
				self.task_D2D1_DUCB.setPolicy(1, D2Dlink_1_IRD_already_DUCB)
				self.task_D2D2_DUCB.setPolicy(1, D2Dlink_2_IRD_already_DUCB)
				print("나머지 작업 처리")
				self.service_D2D1.Service(D2Dlink_1_ISD_already, remainAsk_D2D1, remainStauts_D2D1_ISD,
										  remainD2Dlink_1_ISD, remainDeadlined2d1, systemTime, computationCapD2D1,
										  remainDataSizeD2D1, self.task_D2D1.getReturnDataSize())
				self.service_D2D2.Service(D2Dlink_2_ISD_already, remainAsk_D2D2, remainStauts_D2D2_ISD,
										  remainD2Dlink_2_ISD, remainDeadlined2d2, systemTime, computationCapD2D2,
										  remainDataSizeD2D2, self.task_D2D2.getReturnDataSize())
				self.service_D2D1_gauss.Service(D2Dlink_1_ISD_already_gauss, remainAsk_D2D1_gauss, remainStauts_D2D1_ISD_gauss,
										  remainD2Dlink_1_ISD_gauss, remainDeadlined2d1_gauss, systemTime, computationCapD2D1_gauss,
										  remainDataSizeD2D1_gauss, self.task_D2D1_gauss.getReturnDataSize())
				self.service_D2D2_gauss.Service(D2Dlink_2_ISD_already_gauss, remainAsk_D2D2_gauss, remainStauts_D2D2_ISD_gauss,
										  remainD2Dlink_2_ISD_gauss, remainDeadlined2d2_gauss, systemTime, computationCapD2D2_gauss,
										  remainDataSizeD2D2_gauss, self.task_D2D2_gauss.getReturnDataSize())
				self.service_D2D1_DUCB.Service(D2Dlink_1_ISD_already_DUCB, remainAsk_D2D1_DUCB,
												remainStauts_D2D1_ISD_DUCB,
												remainD2Dlink_1_ISD_DUCB, remainDeadlined2d1_DUCB, systemTime,
												computationCapD2D1_DUCB,
												remainDataSizeD2D1_DUCB, self.task_D2D1_DUCB.getReturnDataSize())
				self.service_D2D2_DUCB.Service(D2Dlink_2_ISD_already_DUCB, remainAsk_D2D2_DUCB,
												remainStauts_D2D2_ISD_DUCB,
												remainD2Dlink_2_ISD_DUCB, remainDeadlined2d2_DUCB, systemTime,
												computationCapD2D2_DUCB,
												remainDataSizeD2D2_DUCB, self.task_D2D2_DUCB.getReturnDataSize())
			# ---------------------------------------------------------------------------
			# 2. Tasks are created
			# ---------------------------------------------------------------------------

			self.task_MEC.Task(MECoffloading_already, totalRemainMEC,remainBid_MEC,remainStatus_MEC,remainDeadlineMEC, taskGenerateTimeMEC,
								remainWorkLoadMEC, remainDataSizeMEC,
								self.taskResultSize,systemTime)



			remainDeadlined2d1 = self.task_D2D1.getDeadline()
			remainDeadlined2d2 = self.task_D2D2.getDeadline()
			remainDeadlineMEC = self.task_MEC.getDeadline()
			remainDataSizeD2D1 = self.task_D2D1.getEntryDataSize()
			remainDataSizeD2D2 = self.task_D2D2.getEntryDataSize()
			remainDataSizeMEC = self.task_MEC.getEntryDataSize()
			remainWorkLoadD2D1 = self.task_D2D1.getCompLoad()
			remainWorkLoadD2D2 = self.task_D2D2.getCompLoad()
			remainWorkLoadMEC = self.task_MEC.getCompLoad()
			remainBid_D2D1 = self.task_D2D1.getBid()
			remainStatus_D2D1 = self.task_D2D1.getTaskStatus()
			remainBid_D2D2 = self.task_D2D2.getBid()
			remainStatus_D2D2 = self.task_D2D2.getTaskStatus()
			remainBid_MEC = self.task_MEC.getBid()
			remainStatus_MEC = self.task_MEC.getTaskStatus()
			taskGenerateTimeD2D1 = self.task_D2D1.getBaseTime()
			taskGenerateTimeD2D2 = self.task_D2D2.getBaseTime()
			taskGenerateTimeMEC = self.task_MEC.getBaseTime()

			computationCapD2D1 = self.service_D2D1.getCompLoad()
			computationCapD2D2 = self.service_D2D2.getCompLoad()
			computationCapD2D1_gauss = self.service_D2D1.getCompLoad()
			computationCapD2D2_gauss = self.service_D2D2.getCompLoad()
			computationCapD2D1_DUCB = self.service_D2D1.getCompLoad()
			computationCapD2D2_DUCB = self.service_D2D2.getCompLoad()

			numberOfTaskD2D1 += len(D2Dlink_1_IRD_already)
			numberOfTaskD2D2 += len(D2Dlink_2_IRD_already)
			numberOfTaskMEC += len(MECoffloading_already)

			remainDeadlined2d1_gauss = self.task_D2D1_gauss.getDeadline()
			remainDeadlined2d2_gauss = self.task_D2D2_gauss.getDeadline()
			remainDataSizeD2D1_gauss = self.task_D2D1_gauss.getEntryDataSize()
			remainDataSizeD2D2_gauss = self.task_D2D2_gauss.getEntryDataSize()
			remainWorkLoadD2D1_gauss = self.task_D2D1_gauss.getCompLoad()
			remainWorkLoadD2D2_gauss = self.task_D2D2_gauss.getCompLoad()
			taskGenerateTimeD2D1_gauss = self.task_D2D1_gauss.getBaseTime()
			taskGenerateTimeD2D2_gauss = self.task_D2D2_gauss.getBaseTime()
			remainBid_D2D1_gauss = self.task_D2D1_gauss.getBid()
			remainStatus_D2D1_gauss = self.task_D2D1_gauss.getTaskStatus()
			remainBid_D2D2_gauss = self.task_D2D2_gauss.getBid()
			remainStatus_D2D2_gauss = self.task_D2D2_gauss.getTaskStatus()

			numberOfTaskD2D1_gauss += len(D2Dlink_1_IRD_already_gauss)
			numberOfTaskD2D2_gauss += len(D2Dlink_2_IRD_already_gauss)

			remainDeadlined2d1_DUCB = self.task_D2D1_DUCB.getDeadline()
			remainDeadlined2d2_DUCB = self.task_D2D2_DUCB.getDeadline()
			remainDataSizeD2D1_DUCB = self.task_D2D1_DUCB.getEntryDataSize()
			remainDataSizeD2D2_DUCB = self.task_D2D2_DUCB.getEntryDataSize()
			remainWorkLoadD2D1_DUCB = self.task_D2D1_DUCB.getCompLoad()
			remainWorkLoadD2D2_DUCB = self.task_D2D2_DUCB.getCompLoad()
			taskGenerateTimeD2D1_DUCB = self.task_D2D1_DUCB.getBaseTime()
			taskGenerateTimeD2D2_DUCB = self.task_D2D2_DUCB.getBaseTime()
			remainBid_D2D1_DUCB = self.task_D2D1_DUCB.getBid()
			remainStatus_D2D1_DUCB = self.task_D2D1_DUCB.getTaskStatus()
			remainBid_D2D2_DUCB = self.task_D2D2_DUCB.getBid()
			remainStatus_D2D2_DUCB = self.task_D2D2_DUCB.getTaskStatus()

			numberOfTaskD2D1_DUCB += len(D2Dlink_1_IRD_already_DUCB)
			numberOfTaskD2D2_DUCB += len(D2Dlink_2_IRD_already_DUCB)

			print('task 개수',len(D2Dlink_1_IRD_already),D2Dlink_1_IRD_already)
			print(len(remainD2Dlink_1_IRD),remainD2Dlink_1_IRD)
			print('task 개수', len(D2Dlink_2_IRD_already), D2Dlink_2_IRD_already)
			print(len(remainD2Dlink_2_IRD),remainD2Dlink_2_IRD)
			print(len(MECoffloading_already),MECoffloading_already)
			print('task 개수',len(D2Dlink_1_IRD_already_gauss),D2Dlink_1_IRD_already_gauss)
			print('task 개수',len(D2Dlink_2_IRD_already_gauss),D2Dlink_2_IRD_already_gauss)
			print('task 개수', len(D2Dlink_1_IRD_already_DUCB), D2Dlink_1_IRD_already_DUCB)
			print('task 개수', len(D2Dlink_2_IRD_already_DUCB), D2Dlink_2_IRD_already_DUCB)

			print('연습',D2Dlink_1_ISD_already)
			print(remainD2Dlink_1_ISD)
			print(D2Dlink_2_ISD_already)
			print(remainD2Dlink_2_ISD)
			print(remainWorkLoadD2D1)
			print(remainDataSizeD2D1)

			# self.service_D2D1.Service(D2Dlink_1_ISD_already,remainAsk_D2D1,remainStauts_D2D1_ISD,remainD2Dlink_1_ISD,remainDeadlined2d1, systemTime,remainWorkLoadD2D1,remainDataSizeD2D1,self.task_D2D1.getReturnDataSize())
			# self.service_D2D2.Service(D2Dlink_2_ISD_already,remainAsk_D2D2,remainStauts_D2D2_ISD,remainD2Dlink_2_ISD,remainDeadlined2d2, systemTime,remainWorkLoadD2D2,remainDataSizeD2D2,self.task_D2D2.getReturnDataSize())
			remainStauts_D2D1_ISD = self.service_D2D1.getTaskStatus()
			remainStauts_D2D2_ISD = self.service_D2D2.getTaskStatus()
			remainAsk_D2D1 = self.service_D2D1.getAsk()
			remainAsk_D2D2 = self.service_D2D2.getAsk()

			remainStauts_D2D1_ISD_gauss = self.service_D2D1_gauss.getTaskStatus()
			remainStauts_D2D2_ISD_gauss = self.service_D2D2_gauss.getTaskStatus()
			remainAsk_D2D1_gauss = self.service_D2D1_gauss.getAsk()
			remainAsk_D2D2_gauss = self.service_D2D2_gauss.getAsk()

			remainStauts_D2D1_ISD_DUCB = self.service_D2D1_DUCB.getTaskStatus()
			remainStauts_D2D2_ISD_DUCB = self.service_D2D2_DUCB.getTaskStatus()
			remainAsk_D2D1_DUCB = self.service_D2D1_DUCB.getAsk()
			remainAsk_D2D2_DUCB = self.service_D2D2_DUCB.getAsk()

			# ---------------------------------------------------------------------------
			# 3. Double Auction is started
			# ---------------------------------------------------------------------------
			D2D1_doubleauction_IRDcandidate, D2D1_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(self.D2Dlink_1_IRD, self.D2Dlink_1_ISD,1)
			D2D2_doubleauction_IRDcandidate, D2D2_doubleauction_ISDcandidate = self.matchRoleForDoubleAuction(self.D2Dlink_2_IRD, self.D2Dlink_2_ISD,2)

			self.temp_doubleAuction_D2D1 = doubleAuction()
			win_IRD, self.win_ISD, bid_price, ask_price, K, remainingIRD = self.temp_doubleAuction_D2D1.doubleAuction(D2D1_doubleauction_IRDcandidate,D2D1_doubleauction_ISDcandidate)
			print('가격',bid_price,ask_price)
			self.temp_doubleAuction_D2D2 = doubleAuction()
			win_IRD_D2D2, win_ISD_D2D2, bid_price_D2D2, ask_price_D2D2, K_D2D2, remainingIRD_D2D2 = self.temp_doubleAuction_D2D2.doubleAuction(D2D2_doubleauction_IRDcandidate,D2D2_doubleauction_ISDcandidate)
			print('가격2',bid_price_D2D2,ask_price_D2D2)
			# ---------------------------------------------------------------------------
			# 3-1. Non Double Auction is started
			# ---------------------------------------------------------------------------
			# Gaussian
			# D2D 1
			self.temp_noDoubleAuction = noDoubleAuction()
			win_IRD_noDouble, self.win_ISD_noDouble, bid_price_noDouble, ask_price_noDouble, K_noDouble, remainingIRD_noDouble = self.temp_noDoubleAuction.noDoubleAuntion(D2D1_doubleauction_IRDcandidate,D2D1_doubleauction_ISDcandidate)
			print('가격3',bid_price_noDouble,ask_price_noDouble)

			# D2D 2
			self.temp_noDoubleAuction_D2D2 = noDoubleAuction()
			win_IRD_noDouble_D2D2, win_ISD_noDouble_D2D2, bid_price_noDouble_D2D2, ask_price_noDouble_D2D2, K_noDouble_D2D2, remainingIRD_noDouble_D2D2 = self.temp_noDoubleAuction_D2D2.noDoubleAuntion(D2D2_doubleauction_IRDcandidate,D2D2_doubleauction_ISDcandidate)

			# ---------------------------------------------------------------------------
			# 4. Multi-Armed Bandit is started
			# ---------------------------------------------------------------------------
			# D2D 1
			#answerOfwinISD = self.MABanswer(self.win_ISD)
			answerOfwinISD = self.win_ISD
			for key,value in list(self.win_ISD.items()):
				answerOfwinISD[key]['importance'] = answerOfISD[key]

			if len(answerOfwinISD) == 0:
				print('no winner D2D1_P')
				regretSumOfPDTS[systemTime] = regretSumOfPDTS[systemTime - 1] + 1
			else:
				gamma_PDTS = gamma_PDTS * 0.99
				opt_ISD = self.proposed_DTS.proposed_DTS(answerOfwinISD,gamma_PDTS)
				print('여기여')
				print(self.win_ISD)
				print(opt_ISD)
				regretSumOfPDTS[systemTime] = regretSumOfPDTS[systemTime - 1] + self.regret_analysis(self.win_ISD, opt_ISD)
				for index, (key, value) in enumerate(answerOfwinISD.items()):
					answerOfwinISD[key]['mabResult'] = opt_ISD[key]

				sorting_opt_ISD = dict(sorted(answerOfwinISD.items(), key=lambda x: x[1]['mabResult'],reverse=True))
				matchList_pro = self.matchingIRDISD(win_IRD, sorting_opt_ISD, self.task_D2D1, IIoT)
				utilityOfIBD_D2D1[systemTime], utilityOfIRD_D2D1[systemTime], utilityOfISD_D2D1[
					systemTime] = self.utilityComputation(len(matchList_pro), bid_price, ask_price, self.win_ISD, win_IRD)
				numberOffailureTask, numberTasksCanceledAndConcludedD2D1, completeTaskD2DIRD, completeTaskD2DISD, temp_D2D1Offloading = self.D2DOffloading(
					matchList_pro, self.task_D2D1, systemTime, numberOffailureTask,
					numberTasksCanceledAndConcludedD2D1, IIoT, completeTaskD2DIRD, completeTaskD2DISD,
					remainD2Dlink_1_IRD, D2Dlink_1_IRD_already)
			# D2D 2
			answerOfwinISD_D2D2 = win_ISD_D2D2
			for key, value in list(win_ISD_D2D2.items()):
				answerOfwinISD_D2D2[key]['importance'] = answerOfISD_D2D2[key]

			#answerOfwinISD_D2D2 = self.MABanswer(win_ISD_D2D2)
			if len(answerOfwinISD_D2D2) == 0:
				print('no winner D2D2_P')
				regretSumOfPDTS_D2D2[systemTime] = regretSumOfPDTS_D2D2[systemTime - 1] + 1
			else:
				gamma_PDTS_D2D2 = gamma_PDTS_D2D2 * 0.99
				opt_ISD_D2D2 = self.proposed_DTS.proposed_DTS(answerOfwinISD_D2D2, gamma_PDTS_D2D2)

				regretSumOfPDTS_D2D2[systemTime] = regretSumOfPDTS_D2D2[systemTime - 1] + self.regret_analysis(win_ISD_D2D2, opt_ISD_D2D2)
				for index, (key, value) in enumerate(answerOfwinISD_D2D2.items()):
					answerOfwinISD_D2D2[key]['mabResult'] = opt_ISD_D2D2[key]

				sorting_opt_ISD_D2D2 = dict(sorted(answerOfwinISD_D2D2.items(), key=lambda x: x[1]['mabResult'], reverse=True))
				matchList_pro_D2D2 = self.matchingIRDISD(win_IRD_D2D2, sorting_opt_ISD_D2D2, self.task_D2D2, IIoT)
				utilityOfIBD_D2D2[systemTime], utilityOfIRD_D2D2[systemTime], utilityOfISD_D2D2[
					systemTime] = self.utilityComputation(len(matchList_pro_D2D2), bid_price_D2D2, ask_price_D2D2,
														  win_ISD_D2D2, win_IRD_D2D2)
				numberOffailureTask, numberTasksCanceledAndConcludedD2D2, completeTaskD2D2IRD, completeTaskD2D2ISD, temp_D2D2Offloading = self.D2DOffloading(
					matchList_pro_D2D2, self.task_D2D2, systemTime, numberOffailureTask,
					numberTasksCanceledAndConcludedD2D2, IIoT, completeTaskD2D2IRD, completeTaskD2D2ISD,
					remainD2Dlink_2_IRD, D2Dlink_2_IRD_already)
			# ---------------------------------------------------------------------------
			# 4-1. Multi-Armed Bandit(Gaussian) is started
			# ---------------------------------------------------------------------------
			# D2D 1
			answerOfwinISD_gaussian = self.win_ISD #self.win_ISD_noDouble
			for key, value in list(self.win_ISD.items()):#self.win_ISD_noDouble.items()):
				answerOfwinISD_gaussian[key]['importance'] = answerOfISD[key]

			#answerOfwinISD_gaussian = self.MABanswer(self.win_ISD_noDouble)
			if len(answerOfwinISD_gaussian) == 0:
				print('no winner D2D1_GA')
				regretSumOfGauss[systemTime] = regretSumOfGauss[systemTime - 1] + 1
			else:
				gamma_gaussian = gamma_gaussian * 0.99
				opt_ISD_Gauss = self.exe_DTS.main_DTS(answerOfwinISD_gaussian,gamma_gaussian)
				print('커커',opt_ISD_Gauss)
				regretSumOfGauss[systemTime] = regretSumOfGauss[systemTime - 1] + self.regret_analysis(self.win_ISD,opt_ISD_Gauss)#self.win_ISD_noDouble,opt_ISD_Gauss)
				for index, (key, value) in enumerate(answerOfwinISD_gaussian.items()):
					answerOfwinISD_gaussian[key]['mabResult'] = opt_ISD_Gauss[key]
				sorting_opt_ISD_Gauss = dict(sorted(answerOfwinISD_gaussian.items(), key=lambda x: x[1]['mabResult'],reverse=True))

				matchList_gauss = self.matchingIRDISD(win_IRD,sorting_opt_ISD_Gauss, self.task_D2D1_gauss, IIoT)#win_IRD_noDouble, sorting_opt_ISD_Gauss, self.task_D2D1_gauss, IIoT)

				utilityOfIBD_D2D1_gauss[systemTime], utilityOfIRD_D2D1_gauss[systemTime], utilityOfISD_D2D1_gauss[
				systemTime] = self.utilityComputation(len(matchList_gauss), bid_price, ask_price, self.win_ISD, win_IRD)
													  #bid_price_noDouble, ask_price_noDouble,
													  #self.win_ISD_noDouble, win_IRD_noDouble)

				numberOffailureTask_gauss, numberTasksCanceledAndConcludedD2D1_gauss, completeTaskD2DIRD_gauss, completeTaskD2DISD_gauss, temp_D2D1Offloading_gauss = self.D2DOffloading(
				matchList_gauss, self.task_D2D1_gauss, systemTime, numberOffailureTask_gauss,
				numberTasksCanceledAndConcludedD2D1_gauss, IIoT, completeTaskD2DIRD_gauss, completeTaskD2DISD_gauss,
				remainD2Dlink_1_IRD_gauss, D2Dlink_1_IRD_already_gauss)
			# D2D 2
			answerOfwinISD_gaussian_D2D2 = win_ISD_D2D2#win_ISD_noDouble_D2D2
			for key, value in list(win_ISD_D2D2.items()):#win_ISD_noDouble_D2D2.items()):
				answerOfwinISD_gaussian_D2D2[key]['importance'] = answerOfISD_D2D2[key]

			print('비엇ㄷ나?',answerOfwinISD_gaussian_D2D2)
			#answerOfwinISD_gaussian_D2D2 = self.MABanswer(win_ISD_noDouble_D2D2)
			if len(answerOfwinISD_gaussian_D2D2) == 0:
				print('no winner D2D2_GA')
				regretSumOfGauss_D2D2[systemTime] = regretSumOfGauss_D2D2[systemTime - 1] + 1
			else:
				gamma_gaussian_D2D2 = gamma_gaussian_D2D2 * 0.99
				opt_ISD_Gauss_D2D2 = self.exe_DTS.main_DTS(answerOfwinISD_gaussian_D2D2, gamma_gaussian_D2D2)
				print('커커',opt_ISD_Gauss_D2D2)

				regretSumOfGauss_D2D2[systemTime] = regretSumOfGauss_D2D2[systemTime - 1] + self.regret_analysis(win_ISD_D2D2,opt_ISD_Gauss_D2D2)
					#win_ISD_noDouble_D2D2, opt_ISD_Gauss_D2D2)

				for index, (key, value) in enumerate(answerOfwinISD_gaussian_D2D2.items()):
					answerOfwinISD_gaussian_D2D2[key]['mabResult'] = opt_ISD_Gauss_D2D2[key]
				sorting_opt_ISD_Gauss_D2D2 = dict(
					sorted(answerOfwinISD_gaussian_D2D2.items(), key=lambda x: x[1]['mabResult'], reverse=True))

				matchList_gauss_D2D2 = self.matchingIRDISD(win_IRD_D2D2, sorting_opt_ISD_Gauss_D2D2, self.task_D2D2_gauss,
													  IIoT)#win_IRD_noDouble_D2D2, sorting_opt_ISD_Gauss_D2D2, self.task_D2D2_gauss,IIoT)

				utilityOfIBD_D2D2_gauss[systemTime], utilityOfIRD_D2D2_gauss[systemTime], utilityOfISD_D2D2_gauss[
					systemTime] = self.utilityComputation(len(matchList_gauss_D2D2), bid_price_D2D2,ask_price_D2D2,win_ISD_D2D2,win_IRD_D2D2)#bid_price_noDouble_D2D2, ask_price_noDouble_D2D2,
														  #win_ISD_noDouble_D2D2, win_IRD_noDouble_D2D2)

				numberOffailureTask_gauss, numberTasksCanceledAndConcludedD2D2_gauss, completeTaskD2D2IRD_gauss, completeTaskD2D2ISD_gauss, temp_D2D2Offloading_gauss = self.D2DOffloading(
					matchList_gauss_D2D2, self.task_D2D2_gauss, systemTime, numberOffailureTask_gauss,
					numberTasksCanceledAndConcludedD2D2_gauss, IIoT, completeTaskD2D2IRD_gauss, completeTaskD2D2ISD_gauss,
					remainD2Dlink_2_IRD_gauss, D2Dlink_2_IRD_already_gauss)



			# ---------------------------------------------------------------------------
			# 4-1. Multi-Armed Bandit(DUCB) is started
			# ---------------------------------------------------------------------------
			# D2D 1
			answerOfwinISD_DUCB = self.win_ISD_noDouble
			for key, value in list(self.win_ISD_noDouble.items()):
				answerOfwinISD_DUCB[key]['importance'] = answerOfISD[key]


			#answerOfwinISD_DUCB = self.MABanswer(self.win_ISD_noDouble)
			if len(answerOfwinISD_DUCB) == 0:
				print('no winner D2D1_DUCB')
				regretSumOfDUCB[systemTime] = regretSumOfDUCB[systemTime - 1] + 1
			else:
				gamma_DUCB = gamma_DUCB * 0.99
				opt_ISD_DUCB = self.DUCB.discounted_UCB(answerOfwinISD_DUCB, gamma_DUCB)
				print('커커', opt_ISD_DUCB)
				regretSumOfDUCB[systemTime] = regretSumOfDUCB[systemTime - 1] + self.regret_analysis(
					self.win_ISD_noDouble, opt_ISD_DUCB)
				for index, (key, value) in enumerate(answerOfwinISD_DUCB.items()):
					answerOfwinISD_DUCB[key]['mabResult'] = opt_ISD_DUCB[key]
				sorting_opt_ISD_DUCB = dict(
						sorted(answerOfwinISD_DUCB.items(), key=lambda x: x[1]['mabResult'], reverse=True))
				matchList_DUCB = self.matchingIRDISD(win_IRD_noDouble, sorting_opt_ISD_DUCB, self.task_D2D1_DUCB,
														  IIoT)

				utilityOfIBD_D2D1_DUCB[systemTime], utilityOfIRD_D2D1_DUCB[systemTime], utilityOfISD_D2D1_DUCB[
						systemTime] = self.utilityComputation(len(matchList_DUCB), bid_price_noDouble,
															  ask_price_noDouble,
															  self.win_ISD_noDouble, win_IRD_noDouble)

				numberOffailureTask_DUCB, numberTasksCanceledAndConcludedD2D1_DUCB, completeTaskD2DIRD_DUCB, completeTaskD2DISD_DUCB, temp_D2D1Offloading_DUCB = self.D2DOffloading(
						matchList_DUCB, self.task_D2D1_DUCB, systemTime, numberOffailureTask_DUCB,
						numberTasksCanceledAndConcludedD2D1_DUCB, IIoT, completeTaskD2DIRD_DUCB,
						completeTaskD2DISD_DUCB,
						remainD2Dlink_1_IRD_DUCB, D2Dlink_1_IRD_already_DUCB)
			# D2D 2
			answerOfwinISD_DUCB_D2D2 = win_ISD_noDouble_D2D2
			for key, value in list(win_ISD_noDouble_D2D2.items()):
				answerOfwinISD_DUCB_D2D2[key]['importance'] = answerOfISD_D2D2[key]
			print(win_ISD_noDouble_D2D2)
			print('우ㅏㅣㅁ루아', answerOfwinISD_DUCB_D2D2)


			#answerOfwinISD_DUCB_D2D2 = self.MABanswer(win_ISD_noDouble_D2D2)
			if len(answerOfwinISD_DUCB_D2D2) == 0:
				print('no winner D2D2_DUCB')
				regretSumOfDUCB_D2D2[systemTime] = regretSumOfDUCB_D2D2[systemTime - 1] + 1
			else:
				gamma_DUCB_D2D2 = gamma_DUCB_D2D2 * 0.99
				opt_ISD_DUCB_D2D2 = self.DUCB.discounted_UCB(answerOfwinISD_DUCB_D2D2, gamma_DUCB_D2D2)
				print('커커', opt_ISD_DUCB_D2D2)

				regretSumOfDUCB_D2D2[systemTime] = regretSumOfDUCB_D2D2[systemTime - 1] + self.regret_analysis(
					win_ISD_noDouble_D2D2, opt_ISD_DUCB_D2D2)

				for index, (key, value) in enumerate(answerOfwinISD_DUCB_D2D2.items()):
					answerOfwinISD_DUCB_D2D2[key]['mabResult'] = opt_ISD_DUCB_D2D2[key]
				sorting_opt_ISD_DUCB_D2D2 = dict(
						sorted(answerOfwinISD_DUCB_D2D2.items(), key=lambda x: x[1]['mabResult'], reverse=True))

				matchList_DUCB_D2D2 = self.matchingIRDISD(win_IRD_noDouble_D2D2, sorting_opt_ISD_DUCB_D2D2,
															   self.task_D2D2_DUCB,
															   IIoT)

				utilityOfIBD_D2D2_DUCB[systemTime], utilityOfIRD_D2D2_DUCB[systemTime], utilityOfISD_D2D2_DUCB[
						systemTime] = self.utilityComputation(len(matchList_DUCB_D2D2), bid_price_noDouble_D2D2,
															  ask_price_noDouble_D2D2,
															  win_ISD_noDouble_D2D2, win_IRD_noDouble_D2D2)

				numberOffailureTask_DUCB, numberTasksCanceledAndConcludedD2D2_DUCB, completeTaskD2D2IRD_DUCB, completeTaskD2D2ISD_DUCB, temp_D2D2Offloading_DUCB = self.D2DOffloading(
						matchList_DUCB_D2D2, self.task_D2D2_DUCB, systemTime, numberOffailureTask_DUCB,
						numberTasksCanceledAndConcludedD2D2_DUCB, IIoT, completeTaskD2D2IRD_DUCB,
						completeTaskD2D2ISD_DUCB,
						remainD2Dlink_2_IRD_DUCB, D2Dlink_2_IRD_already_DUCB)

			# ---------------------------------------------------------------------------
			# 5. Matching IRD and ISD
			# ---------------------------------------------------------------------------


			j = 0
			temp_MECoffloading = totalRemainMEC + MECoffloading_already
			for i in temp_MECoffloading:
				MECoffloadingDict[i] = {'deadline':self.task_MEC.getDeadline()[i]}
				j += 1
			#sortedMECoffloadingDict = dict(sorted(MECoffloadingDict.items(), key=lambda x: x[1]['deadline']))
			print("야호",len(MECoffloadingDict),MECoffloadingDict)

			for i, j in list(MECoffloadingDict.items()):
				if MEC.occupyCPU(i) == True:
					MECoffloadingDict[i]['Policy'] = 2
					#MEC.occupyCPU()
				else:
					CloudOffloading.append(i)
					MECoffloadingDict[i]['Policy'] = 3



			# Server Task
			for key,value in list(MECoffloadingDict.items()):
				if value['Policy'] == 2:

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
						numberOffailureTask_gauss += 1


			MECoffloadingDict.clear()
			#마지막에 TASK_CANCELLED횟수와 TASK_CONCLUDED 횟수 세기

			coefficientEnergy = 0.1
			coefficientTime = 0.9
			alpha, beta, gamma = 0.1, 0.1, 0.1
			# scheduler_temp = scheduler()
			# Scheduler_D2D1 = scheduler_temp.sheduler(self.task_D2D1, coefficientEnergy, coefficientTime, alpha,beta,gamma,IIoT,MEC)
			# scheduler_temp = scheduler()
			# Scheduler_D2D2 = scheduler_temp.sheduler(self.task_D2D2, coefficientEnergy, coefficientTime, alpha, beta, gamma, IIoT,MEC)
			print('남은작업2',)
			print('남은작업2', D2Dlink_2_IRD_already)
			print('남은작업2', D2Dlink_2_IRD_already)

			systemTime += 1

			if systemTime == totalRound:
				temp_D2D1_FAIL = [x for x in temp_D2D1Offloading if x not in completeTaskD2DIRD]
				temp_D2D2_FAIL = [x for x in temp_D2D2Offloading if x not in completeTaskD2D2IRD]
				temp_D2D1_FAIL_gauss = [x for x in temp_D2D1Offloading_gauss if x not in completeTaskD2DIRD_gauss]
				temp_D2D2_FAIL_gauss = [x for x in temp_D2D2Offloading_gauss if x not in completeTaskD2D2IRD_gauss]
				temp_D2D1_FAIL_DUCB = [x for x in temp_D2D1Offloading_DUCB if x not in completeTaskD2DIRD_DUCB]
				temp_D2D2_FAIL_DUCB = [x for x in temp_D2D2Offloading_DUCB if x not in completeTaskD2D2IRD_DUCB]
				temp_MEC_FAIL = [x for x in self.MECoffloading if x not in completeTaskMEC]
				temp_fail = len(temp_D2D1_FAIL) + len(temp_D2D2_FAIL) + len(temp_MEC_FAIL)
				temp_fail_gauss = len(temp_D2D1_FAIL_gauss) + len(temp_D2D2_FAIL_gauss) + len(temp_MEC_FAIL)
				temp_fail_DUCB = len(temp_D2D1_FAIL_DUCB) + len(temp_D2D2_FAIL_DUCB) + len(temp_MEC_FAIL)

				numberOffailureTask += temp_fail
				numberOffailureTask_gauss += temp_fail_gauss
				numberOffailureTask_DUCB += temp_fail_DUCB
				sub = numberTasksCanceledAndConcludedMEC + numberTasksCanceledAndConcludedD2D1 + numberTasksCanceledAndConcludedD2D2
				print('gmdkr',sub)
				print(numberOffailureTask,temp_D2D2_FAIL,temp_D2D1_FAIL,temp_MEC_FAIL)
				numberOfTotalTask = numberOfTaskMEC + numberOfTaskD2D1 + numberOfTaskD2D2
				numberOfTotalTask_gauss = numberOfTaskMEC + numberOfTaskD2D1_gauss + numberOfTaskD2D2_gauss
				numberOfTotalTask_DUCB = numberOfTaskMEC + numberOfTaskD2D1_DUCB + numberOfTaskD2D2_DUCB
				print(numberOfTotalTask,numberOfTotalTask_gauss,numberOfTotalTask_DUCB)
				taskFailureProb = numberOffailureTask / numberOfTotalTask
				taskFailureProb_gauss = numberOffailureTask_gauss / numberOfTotalTask_gauss
				taskFailureProb_DUCB = numberOffailureTask_DUCB / numberOfTotalTask_DUCB
				#taskFailureProb_gauss = numberOffailureTask_gauss / numberOfTotalTask_gauss
				print(taskFailureProb,taskFailureProb_gauss,taskFailureProb_DUCB)
				print('===========regret=============')
				print(regretSumOfPDTS)
				print(regretSumOfGauss)
				print('=============D2D2 regret')
				print(regretSumOfPDTS_D2D2)
				print(regretSumOfGauss_D2D2)
				print(utilityOfISD_D2D2)
				print(utilityOfIRD_D2D2)
				print(utilityOfIBD_D2D2)
				print(utilityOfISD_D2D1)
				print(utilityOfIRD_D2D1)
				print(utilityOfIBD_D2D1)
				print(utilityOfISD_D2D2_gauss)
				print(utilityOfIRD_D2D2_gauss)
				print(utilityOfIBD_D2D2_gauss)
				print(utilityOfISD_D2D1_gauss)
				print(utilityOfIRD_D2D1_gauss)
				print(utilityOfIBD_D2D1_gauss)
				self.regretGraphGeneration(regretSumOfPDTS, regretSumOfPDTS_D2D2, regretSumOfGauss,
									  regretSumOfGauss_D2D2, regretSumOfDUCB,regretSumOfDUCB_D2D2,totalRound)
				self.utilityGraphGeneration(utilityOfIBD_D2D1, utilityOfIBD_D2D2, utilityOfIBD_D2D1_gauss, utilityOfIBD_D2D2_gauss, utilityOfIBD_D2D1_DUCB,utilityOfIBD_D2D2_DUCB,totalRound)
				self.utilityGraphGeneration(utilityOfIRD_D2D1, utilityOfIRD_D2D2, utilityOfIBD_D2D1_gauss,
											utilityOfIRD_D2D2_gauss,utilityOfIRD_D2D1_DUCB,utilityOfIRD_D2D2_DUCB, totalRound)
				self.utilityGraphGeneration(utilityOfISD_D2D1, utilityOfISD_D2D2, utilityOfISD_D2D1_gauss,
											utilityOfISD_D2D2_gauss, utilityOfISD_D2D1_DUCB,utilityOfISD_D2D2_DUCB,totalRound)

	def regretGraphGeneration(self,regretSumOfPDTS,regretSumOfPDTS_D2D2,regretSumOfGauss,regretSumOfGauss_D2D2,regretSumOfDUCB,regretSumOfDUCB_D2D2,totalRound):
		Y1 = regretSumOfPDTS + regretSumOfPDTS_D2D2
		# result1 = sum(regretSumOfPDTS) / len(regretSumOfPDTS)
		# result2 = sum(regretSumOfPDTS_D2D2) / len(regretSumOfPDTS_D2D2)
		# total_result = (result1 + result2) / 2
		# avg_result = np.zeros(len(regretSumOfPDTS))
		#
		# for i in range(len(regretSumOfPDTS)):
		# 	temp_avg = (regretSumOfPDTS[i] + regretSumOfPDTS_D2D2[i]) / 2
		# 	avg_result[i] = temp_avg / total_result
		# result11 = sum(regretSumOfGauss) / len(regretSumOfGauss)
		# result22 = sum(regretSumOfGauss_D2D2) / len(regretSumOfGauss_D2D2)
		# total_result1 = (result11 + result22) / 2
		# avg_result1 = np.zeros(len(regretSumOfGauss))
		#
		# for i in range(len(regretSumOfGauss)):
		# 	temp_avg = (regretSumOfGauss[i] + regretSumOfGauss_D2D2[i]) / 2
		# 	avg_result1[i] = temp_avg / total_result1
		# temp = [(regretSumOfPDTS[i] + regretSumOfPDTS_D2D2[i]) / 2 for i in range(len(regretSumOfPDTS))]
		# temp2 = [(regretSumOfGauss[i] + regretSumOfGauss_D2D2[i])/2 for i in range(len(regretSumOfGauss))]
		# Y1 =np.zeros(len(temp))
		# for i in range(len(temp)):
		# 	temp_num = temp[i]
		# 	Y1[i] = 1 / (1 + math.exp(-temp_num))
		# Y2 = np.zeros(len(temp2))
		# for i in range(len(temp2)):
		# 	temp_num = temp2[i]
		# 	Y2[i] = 1 / (1 + math.exp(-temp_num))
		Y2 = regretSumOfGauss + regretSumOfGauss_D2D2
		#Y3 = regretSumOfDUCB + regretSumOfDUCB_D2D2

		plt.grid()
		plt.plot(range(totalRound), Y1)
		plt.plot(range(totalRound), Y2)
		#plt.plot(range(totalRound), Y3)
		plt.legend(['Proposed', 'Gaussian'])
		plt.title('Regret')
		plt.xlabel('Iterations')
		plt.ylabel('accumulate regret')
		plt.show()

	def utilityGraphGeneration(self,pUtility,pUtility2,gUtility,gUtility2,dUtility,dUtility2,totalRound):
		Y1 = pUtility + pUtility2
		Y2 = gUtility + gUtility2
		Y3 = dUtility + dUtility2
		plt.grid()
		plt.plot(range(totalRound), Y1)
		plt.plot(range(totalRound), Y2)
		plt.plot(range(totalRound), Y3)
		plt.legend(['Proposed', 'Gaussian', 'DUCB'])
		plt.title('Utility')
		plt.xlabel('Iterations')
		plt.ylabel('accumulate Utility')
		plt.show()

	def initialization(self,IIoT):

		for i in range(self.NumberOfIoT - 2):
			if IIoT.getPosition()[i] == 1:
				self.D2Dlink_1.append(IIoT.getId()[i+2])
				if IIoT.getRoleIIoT()[i] == 'IRD':
					self.D2Dlink_1_IRD.append(IIoT.getId()[i+2])
				else:
					self.D2Dlink_1_ISD.append(IIoT.getId()[i+2])
			elif IIoT.getPosition()[i] == 2:
				self.D2Dlink_2.append(IIoT.getId()[i+2])
				if IIoT.getRoleIIoT()[i] == 'IRD':
					self.D2Dlink_2_IRD.append(IIoT.getId()[i+2])
				else:
					self.D2Dlink_2_ISD.append(IIoT.getId()[i+2])
			else:
				self.MECoffloading.append(IIoT.getId()[i+2])
		MECoffloading_already = self.MECoffloading
		D2Dlink_1_already = self.D2Dlink_1
		D2Dlink_2_already = self.D2Dlink_2
		D2Dlink_1_IRD_already = self.D2Dlink_1_IRD
		D2Dlink_1_ISD_already = self.D2Dlink_1_ISD
		D2Dlink_2_IRD_already = self.D2Dlink_2_IRD
		D2Dlink_2_ISD_already = self.D2Dlink_2_ISD

		return MECoffloading_already,D2Dlink_1_already,D2Dlink_2_already,D2Dlink_1_IRD_already,D2Dlink_1_ISD_already,D2Dlink_2_IRD_already,D2Dlink_2_ISD_already

	def D2DOffloading(self,matchList,task,systemTime,numberOffailureTask,numberTasksCanceledAndConcludedD2D,IIoT,completeTaskD2DIRD,completeTaskD2DISD,remainD2Dlink_1_IRD,D2Dlink_1_IRD_already):
		for i in range(len(matchList) - 1, -1, -1):
			if task.verifyTaksFinish(systemTime, matchList[i][0]) == True:
				numberTasksCanceledAndConcludedD2D += 1
				IIoT.alterCPUStatus(self.CORE_FREE, matchList[i][1])
				completeTaskD2DIRD.append(matchList[i][0])
				completeTaskD2DISD.append(matchList[i][1])
				matchList.pop(i)

			#else:

				#numberOffailureTask += 1
		temp_D2D1Offloading = remainD2Dlink_1_IRD + D2Dlink_1_IRD_already
		temp2_D2D1Offloading = [x for x in temp_D2D1Offloading if x not in completeTaskD2DIRD]
		for i in temp2_D2D1Offloading:
			if task.checkTaskTime(systemTime, i) == True:
				completeTaskD2DIRD.append(i)
				numberOffailureTask += 1
				print(i)
			else:
				print('이게맞나', i)
		return numberOffailureTask,numberTasksCanceledAndConcludedD2D,completeTaskD2DIRD,completeTaskD2DISD,temp_D2D1Offloading

	def matchingIRDISD(self,win_IRD,sorting_opt_ISD,task,IIoT):
		sortingWinIRD = dict()
		for index, (key, value) in enumerate(win_IRD.items()):
			for i in range(len(task.getDeviceId())):
				if key == task.getDeviceId()[i]:
					sortingWinIRD[key] = {'dataSize': task.getEntryDataSize()[key],
										  'computationWorkload': task.getCompLoad()[key],
										  'deadlineLatency': task.getDeadline()[key]}
					print("sdfasdfasdf", task.getEntryDataSize()[key])
					print(task.getCompLoad()[key])
					print(sortingWinIRD[key]['dataSize'], sortingWinIRD[key]['computationWorkload'])
					sortingWinIRD[key] = {
						'order': sortingWinIRD[key]['dataSize'] * sortingWinIRD[key]['computationWorkload']}
			# continue
		# sortedWinIRD = dict(sorted(sortingWinIRD.items(),key=lambda x: x[1]['order'], reverse=True))
		sortedWinIRDID = list(sortingWinIRD.keys())
		if len(sortedWinIRDID) < len(sorting_opt_ISD):
			matchList = [[0 for n in range(2)] for m in range(len(sortedWinIRDID))]
		else:
			matchList = [[0 for n in range(2)] for m in range(len(sorting_opt_ISD))]
		for index, (key, value) in enumerate(sorting_opt_ISD.items()):
			if index == len(sortedWinIRDID):
				break
			else:
				matchList[index][0] = sortedWinIRDID[index]
				matchList[index][1] = key
		flagIoTDevice = False
		for index, (key, value) in enumerate(sorting_opt_ISD.items()):
			if IIoT.verifyCPUFree(key) == True:
				flagIoTDevice = True
				IIoT.alterCPUStatus(self.CORE_OCCUPIED, key)
		return matchList


	def utilityComputation(self,num, bid, ask, ISD_actualAsk, IRD_actualBid):
		ISD = 0
		IRD = 0
		for key, value in list(ISD_actualAsk.items()):
			ISD += (ask - value['ask'])
			print('ask_isd',key,ask,value['ask'],ISD)
		for key, value in list(IRD_actualBid.items()):
			IRD += (value['bid'] - bid)
			print('bid_ird',key,value['bid'],bid,IRD)
		IBD = num * (bid - ask)
		print(num,IBD,bid-ask)
		return IBD, IRD, ISD

	def MABanswer(self,win_ISD,com):
		if len(win_ISD) == 0:
			print("no winner")
		else:
			power = 0.2
			ISD_BW = 5
			DR = np.zeros(len(win_ISD))
			energy = np.zeros(len(win_ISD))
			#signal = nr.normal(0, 1, len(win_ISD))
			channelGain = nr.normal(0, 0.05, len(win_ISD))
			noise = nr.normal(0,0.05,len(win_ISD))
			#noise = self.awgn(signal)
			temp_importance = []
			# for index, (key, value) in enumerate(win_ISD.items()):
			# 	SNR = ((channelGain[index] ** 2) * power) / (noise[index] ** 2)
			# 	DR[index] = ISD_BW * np.log2(1 + SNR)
			# 	energy[index] = power * (1 / DR[index])
			# 	reward = com[key] / energy[index]
			# 	win_ISD[key]['importance'] = reward
			# 	temp_importance.append(reward)
			i=0
			for index in win_ISD:
				SNR = ((channelGain[i] ** 2) * power) / (noise[i] ** 2)
				DR[i] = ISD_BW * np.log2(1 + SNR)
				energy[i] = power / DR[i]
				reward = com[index] / energy[i]
				#win_ISD[index]['importance'] = reward
				temp_importance.append(reward)
				i += 1
			importance = self.sigmoid(temp_importance,win_ISD)
			#temp_importance = minmax_scale(temp_importance)
			# for i in range(len(temp_importance)):
			# 	if temp_importance[i] > 1:
			# 		temp_importance[i] = 1
			# 	elif temp_importance[i] < 0:
			# 		temp_importance[i] = 0
			# 	else:
			# 		continue
			# for index,(key,value) in enumerate(win_ISD.items()):
			# 	win_ISD[key]['importance'] = temp_importance[index]

			return importance
		return False

	def sigmoid(self,x,win_ISD):
		sig = dict()
		i = 0
		for key in win_ISD:
			sig.setdefault(key,1 / (1 + math.exp(-x[i])))
			i += 1
				#= [1 / (1 + math.exp(-x[i])) for i in range(len(win_ISD))]
		return sig

	# regret function
	def regret_analysis(self,win_ISD, extract_prob):
		maxArm = max(win_ISD.items(), key=lambda x: x[1]['importance'])

		maxArm_value = maxArm[1]['importance']
		print('먐', maxArm_value)
		extract_maxArm = max(extract_prob.values())
		print(extract_maxArm)
		regretSum = abs(maxArm_value - extract_maxArm)
		print('regret',regretSum)
		return regretSum

	# Addictive White Gaussian Noise function
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



sim = SimulationEXE()
sim.main()

