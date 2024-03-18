from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
import librosa,torch
import numpy as np
def predictDeepFake(filename):
# Load the model from the local directory


    model_name = "MattyB95/AST-VoxCelebSpoof-Synthetic-Voice-Detection"

    # Load the model from the local directory
    extractor = AutoFeatureExtractor.from_pretrained(model_name)
   
    # model = AutoModelForAudioClassification.from_pretrained("F:\Hackathon_2024\Server Integration Models\Server Microservice\Models\s2e_model")
    model = AutoModelForAudioClassification.from_pretrained(model_name)

    audio_data, sample_rate = librosa.load(filename, sr=16000)
    audio_features = extractor(audio_data, sampling_rate=16000)
    inputs = {
    "input_values": audio_features.input_values,
    }
        # Convert the list of NumPy arrays to a single NumPy array
    input_values_array = np.array(audio_features["input_values"])

    # Convert the NumPy array to a PyTorch tensor
    inputs["input_values"] = torch.tensor(input_values_array)
    outputs = model(**inputs)
    logits = outputs.logits

    # Interpret results based on model's task (may require additional information)
    # Example (assuming binary classification):
    predicted_class = torch.argmax(logits, dim=-1).item() # Assuming logits have class probabilities
    if predicted_class == 0:
     return "human"
    else:
     return "ai"