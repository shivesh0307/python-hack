# Load and preprocess test data using librosa
# Load the model and preprocess test data (similar to training data preprocessing)
import os
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.models import load_model

path='Models/audio_classifier_cnn.h5'
current_directory = os.path.dirname(__file__)
model = load_model(os.path.join(current_directory,r'Models/audio_classifier_cnn.h5'))
def predict_cnn(file_path):
        X_test = []
        MAX_TIME_STEPS=109
        # Load audio file using librosa
        audio, _ = librosa.load(file_path, sr=16000, duration=3)

        # Extract Mel spectrogram using librosa
        mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=16000, n_mels=128)
        mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    
        # Ensure all spectrograms have the same width (time steps)
        if mel_spectrogram.shape[1] < MAX_TIME_STEPS:
            mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, MAX_TIME_STEPS - mel_spectrogram.shape[1])), mode='constant')
        else:
            mel_spectrogram = mel_spectrogram[:, :MAX_TIME_STEPS]

        X_test.append(mel_spectrogram)

        # Convert list to numpy array
        X_test = np.array(X_test)

        # Predict using the loaded model
        y_pred = model.predict(X_test)

        # Convert probabilities to predicted classes
        y_pred_classes = np.argmax(y_pred, axis=1)
        print(y_pred_classes[0])
        type=""
        if y_pred_classes[0]== 1:
            type="human"
        else:
            type="ai" 
             
        return [str(y_pred[0][0]),str(y_pred[0][1]),type]     