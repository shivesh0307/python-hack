from speec2emotion import predict
from noiseIntensityDetection import findIntensity
from deepfakeDetection import predictDeepFake
from deepfake_cnn import predict_cnn
path=r'F:\Hackathon_2024\DeepFakeModel\DeepFake\CancelCard.mp3'
print("started")
# print(findIntensity(path))
print(predict(path))
print(predict_cnn(path))
