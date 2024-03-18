import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import noisereduce as nr
from pydub import AudioSegment
import librosa
def findIntensity(path):
    # Load the audio file
    audio, sr = librosa.load(path, sr=None)

    # Perform noise reduction using noisereduce library
    reduced_noise = nr.reduce_noise(y=audio, sr=sr)

    # Calculate the noise signal
    noise_signal = audio - reduced_noise

    # Perform Fourier Transform on the original signal
    fft_data_original = np.fft.fft(audio)

    # Perform Fourier Transform on the denoised signal
    fft_data_denoised = np.fft.fft(reduced_noise)

    # Perform Fourier Transform on the noise signal
    fft_data_noise = np.fft.fft(noise_signal)
    
    # Calculate the maximum absolute amplitude of the noise signal and the original signal
    An = np.max(np.abs(noise_signal))
    Ao = np.max(np.abs(audio))
    
    # Determine the intensity based on the ratio of noise amplitude to original signal amplitude
    if An > 0.66 * Ao:
        return "high"
    elif An > 0.4 * Ao:
        return "medium"
    else:
        return "low"
