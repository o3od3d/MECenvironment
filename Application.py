
class Application():

    def __init__(self):
        print("app")
        # self.id
        # # self.rateGeneration                    # micro seconds
        # # self.dataEntrySize                     # bits
        # # self.resultsSize                         # bits
        # # self.computationalLoad              # CPU cycles
        # # self.criticalTaskPercentages  # percentages 0 ~1
        # # self.criticalTaksDeadline        # micro seconds
        # # self.numberOfTask
        # # percentages 0 ~1
        # if self.criticalTaskPercentages > 1 or self.criticalTaskPercentages < 0:
        #     print("app",self.id,"percente out of bounds")
    def application(self, id, rateGeneration, dataEntrySize, resultsSize, computationalLoad, criticalTaskPercentages, criticalTaksDeadline):
        self.id = id
        self.rateGeneration = rateGeneration  # micro seconds
        self.dataEntrySize = dataEntrySize  # bits
        self.resultsSize = resultsSize  # bits
        self.computationalLoad = computationalLoad
        if criticalTaskPercentages > 1 or criticalTaskPercentages < 0:
            print("app",self.id,"percente out of bounds")
        self.criticalTaskPercentages = criticalTaskPercentages  # percentages 0 ~1
        self.criticalTaksDeadline = criticalTaksDeadline  # micro seconds
        self.numberOfTask = 0

    def getID(self):
        return self.id

    def getRateGenerate(self):
        return self.rateGeneration

    def getDataEntrySize(self):
        return self.dataEntrySize

    def getResultSize(self):
        return self.resultsSize

    def getCriticalTaskDeadline(self):
        return self.criticalTaksDeadline

    def getCriticalTaskPercentage(self):
        return self.criticalTaskPercentages

    def getNumberOfTask(self):
        return self.numberOfTask

    def getComputaionWorkload(self):
        return self.computationalLoad

    def setNumberOfTask(self, numberOfTask):
        self.numberOfTask = numberOfTask

    def defineInTaskIsCritical(self, numberOfTask):
        if ((numberOfTask + 1) * self.numberOfTask * self.criticalTaskPercentages) % self.numberOfTask == 0:
            return True
        else:
            return False
