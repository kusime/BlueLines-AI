import re
import cv2
from tflite_runtime.interpreter import Interpreter
import numpy as np

# get from frame
CAMERA_WIDTH = 2560
CAMERA_HEIGHT = 1600


def set_input_tensor(interpreter, image):
    """Sets the input tensor."""
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.expand_dims((image-255)/255, axis=0)


def get_output_tensor(interpreter, index):
    """Returns the output tensor at the given index."""
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    # print("------------------------")
    # print(f"{index} =>>",tensor)
    # print("------------------------")
    return tensor


def detect_objects(interpreter, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    # Get all output details
    # [ 1.8703029e-01  4.0526453e-01  1.0575987e+00  8.9424348e-01] ....
    boxes = get_output_tensor(interpreter, 1)
    # [0. 0. 0. 1. 0. 0. 0. 0. 0. 1.]
    classes = get_output_tensor(interpreter, 3)
    # [0.9201271  0.7438971  0.49236536 0.2683063  0.23500252 0.22495505
    scores = get_output_tensor(interpreter, 0)
    count = int(get_output_tensor(interpreter, 2))  # 10.0

    results = []
    for i in range(count):
        if scores[i] >= threshold:
            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }
            results.append(result)
    return results


class TFLITE:
    def __init__(self, modelName):
        # init tflite model
        self.interpreter = Interpreter(f'AI/{modelName}/detect.tflite')
        self.interpreter.allocate_tensors()

        print("---------------------------------\n")
        print(f"TFLITE initialized , target model =>{modelName}")
        print("\n--------------------------------\n")

    def predict(self, frame, threshold=0.7):
        preprocess = cv2.resize(cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB), (320, 320))
        results = detect_objects(self.interpreter, preprocess, threshold)
        cooked_results = []
        for res in results:
            # get raw data
            ymin, xmin, ymax, xmax = res['bounding_box']
            # scale to the screen size
            x1 = max(1, xmin * CAMERA_WIDTH)
            x2 = min(CAMERA_WIDTH, xmax * CAMERA_WIDTH)
            y1 = max(1, ymin * CAMERA_HEIGHT)
            y2 = min(CAMERA_HEIGHT, ymax * CAMERA_HEIGHT)

            build_res = [x1, y1, x2, y2, res['score'], res['class_id']]
            cooked_results.append(build_res)
        return cooked_results
