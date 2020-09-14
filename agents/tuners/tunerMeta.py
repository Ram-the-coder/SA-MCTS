from abc import ABC, abstractmethod

# All tuners should extend (inherit from) this class
class TunerMeta(ABC):

    @abstractmethod
    def getParams(self):
        pass

    @abstractmethod
    def updateStatistics(self, reward):
        pass

