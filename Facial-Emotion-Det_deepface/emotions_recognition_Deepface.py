from deepface import DeepFace

## A more simpler way fully using Deepface.

obj = DeepFace.stream(db_path="./database", model_name="DeepFace",detector_backend="opencv",time_threshold=5,frame_threshold=5)
print(obj)