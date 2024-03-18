# Section 5.3
# Contains the extraction process of 4 features used in Void system
# feature extraction

# !pip install pydub

import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as ssig
import scipy.stats as stats
from scipy.signal import find_peaks
import os
import matplotlib.pyplot as plt
import math
import librosa
import librosa
from sklearn import svm
from sklearn import svm
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestCentroid
from pydub import AudioSegment
from data_preparation import data_preparation

current_directory = os.path.dirname(__file__)

def predict(file_path):
    x_eval=data_preparation(file_path)
    # Load the the SVM classifier model:
    file_model = os.path.join(current_directory,r'Models\svm.pkl')
    if os.path.isfile(file_model):
        # Load the extracted features and corresponding labels:
        with open(file_model, 'rb') as f:
            classifier=pickle.load(f)
    else:
        print('Model Not Found')

    # Prediction result of SVM classifier on EVALUATION set of ASVspoof 2017 v2 dataset:
    print("Results")
    result_pred = classifier.predict(x_eval)
    print("predicted result", result_pred)
    return result_pred

if __name__ == '__main__':
    audio_folder = os.path.join(os.getcwd(), 'audio')
    for file in os.listdir(audio_folder):
        # Check if the file has an audio extension
        if file.endswith('.wav') or file.endswith('.mp3') or file.endswith('.ogg'):
            filename = os.path.basename(file)
            file_path = os.path.join(audio_folder, file)
            
            # Determine the file format
            file_format = file.split('.')[-1]

            # Load the audio data
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()

            # Call the predict function with the audio data and file format
            probability = predict(audio_data, file_format)

            print("Probability , fileName" , probability, filename)
