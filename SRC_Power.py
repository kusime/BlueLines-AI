import cv2


class SRC:
    def __init__(self):
        pass

    def getCountOfFrames(cap, count=10):
        cap = cv2.VideoCapture(4)
        catched = []

        try:
            for i in range(count):
                # print("Now catching %d frames" % i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    catched.append(frame)
                else:
                    print("Stream is already dead ..")
                    exit(1)
                    return None
            # print(f'{count} frames collected ...')
            cap.release()
            return catched
        except:
            print("Error Occured ... Shutting down ...")
            cap.release()
            return None


if __name__ == "__main__":
    src = SRC()
    frames = src.getCountOfFrames(10)
    print(len(frames))
    frames = src.getCountOfFrames(20)
    print(len(frames))
    src.close()
