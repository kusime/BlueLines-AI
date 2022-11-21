from asyncio import sleep
from AI_Power import AI
from SRC_Power import SRC
import random


class Stabilizer(AI):
    def __init__(self, ARCH, modelName: str, label: list):
        # class inherits from AI to extend its functionality
        super().__init__(ARCH, modelName, label)
        self.src = SRC()

    def getStablePredictions(self, sample=10,threshold=0.6):
        # get  frames
        frames = self.src.getCountOfFrames(sample)
        predictions = []
        # predict every frame
        if (frames == None):
            print("No frames to predict maybe streaming deated")
            exit(1)
        for frame in frames:
            predict = self.predict(frame,threshold)
            if predict != None:
                predictions.append(predict)
        if (len(predictions) == 0):
            # no target was found
            return None
        # since the icon will jump or other , we need to be greedy
        # map the predictions length
        predictions_len = [len(predict) for predict in predictions]
        # get the max unit
        maxPredict = max(predictions_len)
        minPredict = min(predictions_len)
        # filter the predictions that matched the max length
        filtedPredict = [
            predict for predict in predictions if len(predict) == maxPredict]
        # print(f"{sample} of frame.. MaxPredict={maxPredict} MinPredict={minPredict} FiltedPredictCount={maxPredict-minPredict}")
        return random.choice(filtedPredict)


if __name__ == "__main__":
    from ARCH.tflite import TFLITE
    from ARCH.yolov5 import YOLO
    Monster = Stabilizer(YOLO, 'Monster', ['Monster'])
    print(Monster.getStablePredictions())

    Status = Stabilizer(TFLITE, 'BattleStatus', ['MonsterSelect',
                                                 'ReadyBattle',
                                                 'Battling',
                                                 'BattleFinished'])
    print(Status.getStablePredictions())
"""
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1243, 703), 'confident': 0.8, 'label': 'Monster'}, {'point': (1026, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.74, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1243, 702), 'confident': 0.75, 'label': 'Monster'}, {'point': (1026, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.74, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1026, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.74, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1026, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.74, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.75, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2135, 537), 'confident': 0.75, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.75, 'label': 'Monster'}, {'point': (2134, 537), 'confident': 0.75, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}, {'point': (2134, 537), 'confident': 0.75, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2134, 537), 'confident': 0.76, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2134, 537), 'confident': 0.76, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2133, 536), 'confident': 0.77, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2133, 536), 'confident': 0.77, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2134, 536), 'confident': 0.78, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.88, 'label': 'Monster'}, {'point': (2134, 536), 'confident': 0.79, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.76, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (2133, 536), 'confident': 0.79, 'label': 'Monster'}, {'point': (1026, 395), 'confident': 0.77, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (2133, 536), 'confident': 0.8, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.77, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (2132, 537), 'confident': 0.82, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.77, 'label': 'Monster'}]
[{'point': (1932, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (2132, 536), 'confident': 0.83, 'label': 'Monster'}, {'point': (1244, 703), 'confident': 0.79, 'label': 'Monster'}, {'point': (1025, 395), 'confident': 0.78, 'label': 'Monster'}]
[{'point': (1931, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (1243, 705), 'confident': 0.88, 'label': 'Monster'}, {'point': (2132, 537), 'confident': 0.84, 'label': 'Monster'}, {'point': (1024, 395), 'confident': 0.78, 'label': 'Monster'}]
[{'point': (1241, 707), 'confident': 0.93, 'label': 'Monster'}, {'point': (1931, 694), 'confident': 0.89, 'label': 'Monster'}, {'point': (2133, 537), 'confident': 0.85, 'label': 'Monster'}, {'point': (1024, 394), 'confident': 0.78, 'label': 'Monster'}]
"""
