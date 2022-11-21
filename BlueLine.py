from AI_Stabilizer import Stabilizer
from ADB_Power import ADB
from time import sleep
from random import choice
from ARCH.tflite import TFLITE
from ARCH.yolov5 import YOLO
from enum import Enum

# BattleStatus



class BattleStatus():
    Pending = 'MonsterSelect'
    Ready = 'ReadyBattle'
    Doing = 'Battling'
    Done = 'BattleFinished'


if __name__ == "__main__":
    Phone = ADB("S8M6R20710001175")
    BattleStatusAI = Stabilizer(TFLITE, 'BattleStatus', ['MonsterSelect',
                                                         'ReadyBattle',
                                                         'Battling',
                                                         'BattleFinished'])
    MonsterAI = Stabilizer(YOLO, 'Monster', ['Monster'])

    while True:

        CurrentState = BattleStatusAI.getStablePredictions()
        if (CurrentState == None):
            print(f"Unheanled Situation wating ...")
            sleep(5)
            continue
        else:
            # prepare the status
            CurrentState = CurrentState[0]

        print(BattleStatus.Pending)
        if (CurrentState['label'] == BattleStatus.Pending):
            # get Monster
            MonsterPredict = MonsterAI.getStablePredictions()
            print(MonsterPredict)
            if (MonsterPredict != None):
                monster = choice(MonsterPredict)
                print(f"Proccessing Monster at {monster['point']}")
                Phone.tap(monster['point'])
                continue
            print("Monster not found..")
            continue

        if (CurrentState['label'] == BattleStatus.Ready):
            # if we have already selected a monster
            print("Current Ready to start a new battle.. Proccessing..")
            Phone.tap(CurrentState['point'])
            continue

        if (CurrentState['label'] == BattleStatus.Doing):
            # if we have already selected a monster
            print(
                "Current we are doing battling ... waiting for battle finished.. Proccessing..")
            sleep(5)
            continue

        if (CurrentState['label'] == BattleStatus.Done):
            # if we have already selected a monster
            # skip first page
            Phone.tap(CurrentState['point'])
            sleep(1)
            # skip second page
            Phone.tap(CurrentState['point'])
            sleep(1)
            # back to the page 
