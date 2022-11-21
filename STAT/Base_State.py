from abc import ABC, abstractmethod

class BaseState(ABC):
    @abstractmethod
    def EnterState(self,currentState):
        pass

    @abstractmethod
    def UpdateState(self,currentState):
        pass
    