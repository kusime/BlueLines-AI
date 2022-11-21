import torch


class YOLO:
    def __init__(self, modelName, mode="best"):
        self.model = torch.hub.load(
            repo_or_dir='/home/kusime/Desktop/AI/YOLO-Drowsiness-Detection/yolov5',
            model='custom',
            path=f'AI/{modelName}/{mode}.pt',
            source='local', force_reload=True)

        print("---------------------------------\n")
        print(f"YOLO initialized , target model =>{modelName}")
        print("\n--------------------------------\n")

    def predict(self, frame, threshold=0.7):
        # [x1 , y1 , x2 , y2 , score , label + 15]
        results = self.model(frame).xyxy[0].cpu().tolist()
        for res in results:
            res[-1] -= 15
        return results
