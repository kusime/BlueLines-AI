from abc import ABC, abstractmethod

class BaseState(ABC):
    @abstractmethod
    def EnterState(self,game):
        pass

    @abstractmethod
    def UpdateState(self,game):
        pass
    