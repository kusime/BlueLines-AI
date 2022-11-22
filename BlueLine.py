from time import sleep
from AI_Stabilizer import Stabilizer
from ARCH.tflite import TFLITE
from ARCH.yolov5 import YOLO
from STAT.Battle_Pending import BattlePending
from STAT.Battle_Doing import BattleDoing
from STAT.Battle_Done import BattleDone
from STAT.Battle_Ready import BattleReady
from ADB_Power import ADB


class BattleStatus():
    Pending = 'MonsterSelect'
    Ready = 'ReadyBattle'
    Doing = 'Battling'
    Done = 'BattleFinished'


class GenerticButton():
    Confirm = 'Confirm'
    ItemsRec = 'ItemsRecieved'


class GameStateManager:
    # define the State to fit in with the status AI
    BattleStatus = BattleStatus()
    GenerticButton = GenerticButton()
    # define state
    BattlePending = BattlePending()
    BattleReady = BattleReady()
    BattleDoing = BattleDoing()
    BattleDone = BattleDone()
    Phone = ADB("S8M6R20710001175")
    # use to the handler the genertic situation
    GenerticAI = Stabilizer(TFLITE, 'GenerticInput', [
                            'Confirm', 'ItemsRecieved'])
    StatusAI = Stabilizer(TFLITE, 'BattleStatus', [
        'MonsterSelect', 'ReadyBattle', 'Battling', 'BattleFinished'])
    MonsterAI = Stabilizer(YOLO, 'Monster', ['Monster'])

    # Status click
    CurrentStatusPoint = None

    # rouned counter
    LoadBalancer = 0

    def getCurrentStateAndSetPoint(self,threshold=0.7):
        currentPredict = self.StatusAI.getStablePredictions(20,threshold)
        if (currentPredict != None):
            # extract the status ai return and set current point to this status
            extract = currentPredict[0]
            self.CurrentStatusPoint = extract['point']
            return extract['label']
        return currentPredict

    def waiter(self, timeToWait=2):
        try:
            sleep(timeToWait)
        except KeyboardInterrupt:
            print("Exiting...")
            exit(1)

    def _setFSMInitialState(self):
        statePredict = self.StatusAI.getStablePredictions(10)
        print(statePredict)
        if (statePredict == None):
            print(f"Unheanled Situation ... Check if we have confirm button")
            confirmPredict = self.GenerticAI.getStablePredictions(10,  0.7)
            if (confirmPredict != None):
                extract = confirmPredict[0]
                # click the confirm button
                self.Phone.tap(extract['point'])
            else:
                print("Unkown situation and no confirm reachable try to tap the center")
                self.Phone.tap((1076, 534))
            # the revoke the _setFSMInitialState since the state is not being setted yet
            return self._setFSMInitialState()

        else:
            # prepare the status
            statePredict = statePredict[0]
            self.CurrentStatusPoint = statePredict['point']

        if (statePredict['label'] == BattleStatus.Pending):
            self.currentState = self.BattlePending

        if (statePredict['label'] == BattleStatus.Ready):
            self.currentState = self.BattleReady

        if (statePredict['label'] == BattleStatus.Doing):
            self.currentState = self.BattleDoing

        if (statePredict['label'] == BattleStatus.Done):
            self.currentState = self.BattleDone

    def __init__(self):
        self.currentState = None
        self._setFSMInitialState()
        self.currentState.EnterState(self)

    def Update(self):
        # trigger every frame
        # pass the context to the UpdateState
        self.currentState.UpdateState(self)

    def SwitchState(self, newState):
        # switch state context
        self.currentState = newState
        # Enter the new state pass the state
        self.currentState.EnterState(self)


if __name__ == "__main__":
    GM = GameStateManager()
    while True:
        GM.Update()
