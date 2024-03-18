# To extract Void features from training, development and evaluation data, respectively.
# And save the extracted features and labels into .txt files for further use.

import sys
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as ssig
import scipy.stats as stats
import os
import matplotlib.pyplot as plt
import math
import librosa
from sklearn import svm
from feature_extraction import LinearityDegreeFeatures, HighPowerFrequencyFeatures, extract_lpcc, calc_stft, _stft, load_audio_file


def data_preparation(file_path):
    # Initialize parameters:
    W = 14
    # Peak selection threshold:
    omega = 0.3
    # Number of points in each signal segment (window size):
    nperseg = 512
    # Hop length of the window is 25% nperseg (with 75% overlap):
    noverlap = 512-128
    # Number of FFT points:
    nfft = 2048
    # Calculate the number of segments k in S_pow:
    k = int((nfft/2 + 1) / W)

    # Create an empty Numpy array to store extracted features
    fl = np.zeros((1, 97))
    # ------ Stage 1: Signal transformation ------
    # Read the input signal:
    signal, _ = librosa.load(file_path, sr=16000)

    # Compute STFT for the input signal:
    sig_stft = _stft(signal)

    # Compute S_pow from STFT:
    S_pow = np.sum(np.abs(sig_stft)**2/nfft, axis=1)

    # ------ Stage 2: Feature Extraction ------
    # Calculate the sum of power in each segment (in total k segments):
    power_vec = np.zeros(k)
    for i in np.arange(k):
        power_vec[i] = np.sum(S_pow[i*W:(i+1)*W])
    # Normalize power_vec as power_normal:
    power_normal = power_vec / np.sum(power_vec)

    # Feature 1: FV_LFP - low frequencies power features
    FV_LFP = power_normal[0:48] * 100
    #print(FV_LFP)

    # Feature 2: FV_LDF - signal power linearity degree features
    _, FV_LDF = LinearityDegreeFeatures(power_normal)
    #FV_LDF = np.zeros(2)

    # Feature 3: FV_HPF - high power frequency features
    FV_HPF = HighPowerFrequencyFeatures(FV_LFP, omega)
    #FV_HPF = np.zeros(35)

    # Feature 4: FV_LPC - linear prediction cesptrum coefficients
    FV_LPC = extract_lpcc(file_path, 12)
    #FV_LPC = np.zeros(12)

    # ------ Stage 3: Attack Detection ------
    # Normalize each sub-feature:
    '''
    mean_LFP = np.mean(FV_LFP)
    FV_LFP = (FV_LFP - mean_LFP) / (FV_LFP.max() - FV_LFP.min())
    mean_LDF = np.mean(FV_LDF)
    FV_LDF = (FV_LDF - mean_LDF) / (FV_LDF.max() - FV_LDF.min())
    mean_HPF = np.mean(FV_HPF)
    FV_HPF = (FV_HPF - mean_HPF) / (FV_HPF.max() - FV_HPF.min())
    mean_LPC = np.mean(FV_LPC)
    FV_LPC = (FV_LPC - mean_LPC) / (FV_LPC.max() - FV_LPC.min())
    '''
    # Construct the final feature of length 97 (= 2 + 35 + 12 + 48):
    FV_Void = np.concatenate((FV_LDF, FV_HPF, FV_LPC, FV_LFP))
    #FV_Void = np.concatenate((FV_LDF, FV_LPC))
    '''
    print("Extracted Void feature for {} is:".format(filename))
    print(FV_Void)
    print("--------------------------------------------")
    '''
    fl[0:97] = FV_Void
    print("Feature extraction FINISHED!")
    return fl

    


