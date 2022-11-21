import cv2


class AI:
    """
        ARCH : CLASS
        modelName : Custom model in the AI/{modelName}
        label : Custom label
    """

    def __init__(self, ARCH, modelName: str, label: list):
        self.arch = ARCH(modelName)
        self.label = label

    def predict(self, frame, threshold=0.7):
        results = self.arch.predict(frame, threshold)
        if (len(results) == 0):
            return None
        cooked = []
        for res in results:
            x = int(res[0]) + int((int(res[2]-res[0])) / 2)
            y = int(res[1]) + int((int(res[3]-res[1])) / 2)
            preditUnit = {
                'point': (x, y),
                'confident': float("{:.2f}".format(res[4])),
                'label': self.label[int(res[-1])]
            }
            if (preditUnit['confident'] >= threshold):
                cooked.append(preditUnit)
        if (len(cooked) != 0):
            return cooked
        return None

    # def _getFrame(self):
    #     cap = cv2.VideoCapture(4)
    #     if (cap.isOpened()):
    #         ret, frame = cap.read()
    #         self.frame = frame

    def _linktest(self):
        try:
            cap = cv2.VideoCapture(4)
            while cap.isOpened():
                ret, frame = cap.read()

                # Make detections
                print(self.predict(frame))

                # cv2.imshow('YOLO', np.squeeze(results.render()))

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            print("Closing...")
            cap.release()
            cv2.destroyAllWindows()
        except:
            print("Shutting down ...")
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    from ARCH.yolov5 import YOLO
    from ARCH.tflite import TFLITE
    Monster = AI(YOLO, 'Monster', ['Monster'])
    print(Monster.predict(cv2.imread('screenshot.png')))

    Status = AI(TFLITE, 'BattleStatus', ['MonsterSelect',
                                         'ReadyBattle',
                                         'Battling',
                                         'BattleFinished'])
    print(Status.predict(cv2.imread('screenshot.png')))

# Monster._linktest()
# label = ['Monster']
# x1y1 x2y2
# result = [[1738.099609375, 567.2819213867188, 1949.12255859375, 670.8003540039062, 0.9459782838821411, 15.0], [601.9906005859375, 564.6598510742188, 811.32177734375, 668.5195922851562, 0.9092075228691101, 15.0], [1499.509521484375, 420.4072265625, 1708.947021484375, 519.988525390625, 0.9076191782951355, 15.0]]
# # # print(len(result))
# for res in result:
#     x = int(res[0]) + int ((int(res[2]-res[0])) / 2)
#     y = int(res[1]) + int ((int(res[3]-res[1])) / 2)

#     print({
#         'point': (x,y),
#         'confident': float("{:.2f}".format(res[4])),
#         'label': label[int(res[-1])-15]
#     })
