from time import sleep
from AI_Stabilizer import Stabilizer
from ARCH.tflite import TFLITE
from ARCH.yolov5 import YOLO
from STAT.Battle_Pending import BattlePending
from STAT.Battle_Doing import BattleDoing
from STAT.Battle_Done import BattleDone
from STAT.Battle_Ready import BattleReady
from ADB_Power import ADB
from random import randint
import vlc


class AutoFixed:
    # x1 y1 x2 y2
    stage_1 = [360, 326, 2210, 1350]
    stage_2 = [426, 556, 2088, 1138]
    stage_3 = [562, 496, 974, 1140]
    stage_4 = [1432, 460, 2088, 1128]
    stage_5 = [1472, 686, 2192, 1000]
    stage_6 = [1044, 750, 1530, 978]

    all_stage = [stage_1, stage_2, stage_3, stage_4, stage_5, stage_6]

    def __init__(self):
        # every time reset the count will
        self.count = 0

    def getFixPoint(self):

        print("Get fix point count =>", self.count)
        if (self.count >= len(self.all_stage)):
            return None
        currentStage = self.all_stage[self.count]

        cookPoint = (randint(currentStage[0], currentStage[2]), randint(
            currentStage[1], currentStage[3]))
        self.count += 1  # increment counter
        return cookPoint

    def getAlert(self):
        print("alert now ... And restart the Pending State")
        p = vlc.MediaPlayer("alert.mp3")
        p.play()
        # reset the counter
        self.count = 0


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
    GenerticAI = Stabilizer(TFLITE, ['GenerticInput'], [
                            'Confirm', 'ItemsRecieved'])
    StatusAI = Stabilizer(TFLITE, ['BattleStatus'], [
        'MonsterSelect', ['ReadyBattle'], 'Battling', 'BattleFinished'])
    MonsterAI = Stabilizer(YOLO, ['Monster/Genertic','Monster/11-24'], ['Monster'])

    # Status click
    CurrentStatusPoint = None

    # rouned counter
    LoadBalancer = 0

    # autofixer
    autoFixMissingTarget = AutoFixed()

    def getCurrentStateAndSetPoint(self, sample=20, threshold=0.7):
        currentPredict = self.StatusAI.getStablePredictions(sample, threshold)
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
        print("_setFSMInitialState called : Now setting the FSM initial state...")
        if (statePredict == None):
            print(f"Unheanled Situation ... Check if we have confirm button")
            # upper the threshold incase in the battle finished state the charater will make a effect to the confirming status
            confirmPredict = self.GenerticAI.getStablePredictions(10,  0.9)
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
    try:
        GM = GameStateManager()
        while True:
            GM.Update()
    except KeyboardInterrupt:
        print("Exiting")
        exit(1)
    except:
        print("unkown exception restarting all state")
        GM = GameStateManager()
        while True:
            GM.Update()
