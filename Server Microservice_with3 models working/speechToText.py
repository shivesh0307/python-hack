import os
import azure.cognitiveservices.speech as speechsdk
import wave
import contextlib
import subprocess

speechkey = "1b8e33a2ea1548829b589bdfd8d9aaff"
region="eastus"

from pydub import AudioSegment

import subprocess 
  

def convert_mp3_to_wav(mp3_file, wav_file):
    # convert mp3 to wav file 
    subprocess.call(['ffmpeg', '-i', mp3_file, 
                 wav_file])


def recognize_from_file(audio_file):
    errorMessage=""
    try:
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        audio_file_wav = os.path.splitext(audio_file)[0] + ".wav"
        convert_mp3_to_wav(audio_file, audio_file_wav)
        auto_detect_source_language_config =speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "es-ES", "zh-CN"])
        speech_config = speechsdk.SpeechConfig(subscription=speechkey, region=region)
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_wav)
        print("HEHE")
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            auto_detect_source_language_config=auto_detect_source_language_config, 
            audio_config=audio_config)
        print("HEHE")
        print("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(speech_recognition_result)
        detected_language = auto_detect_source_language_result.language

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        print("Language", detected_language)
        speech_recognizer=None
        del speech_recognizer
        # if os.path.exists(audio_file_wav):
        #     os.remove(audio_file_wav)
    except Exception as e: 
        print("An error occurred during speech recognition:", e)
        errorMessage=e
    finally:
        # Clean up: delete the generated WAV file
        try:
            if os.path.exists(audio_file_wav):
                os.remove(audio_file_wav)
        except Exception as e:
            print("An error occurred while deleting the WAV file:", e)
            errorMessage = "Error deleting WAV file: " + str(e)

    return detected_language , speech_recognition_result.text, errorMessage



if __name__ == "__main__":
    recognize_from_file(r"C:\Users\Shivesh\Desktop\repo\hackathon\sherlocked\code\Server Microservice_with3 models working\audio2.wav")
    convert_mp3_to_wav(r"C:\Users\Shivesh\Desktop\repo\hackathon\sherlocked\code\Server Microservice_with3 models working\ElevenLabs_2024-03-14T08_24_47_Charlie.mp3",r"C:\Users\Shivesh\Desktop\repo\hackathon\sherlocked\code\Server Microservice_with3 models working\ElevenLabs_2024-03-14T08_24_47_Charlie.wav")
    recognize_from_file(r"C:\Users\Shivesh\Desktop\repo\hackathon\sherlocked\code\Server Microservice_with3 models working\ElevenLabs_2024-03-14T08_24_47_Charlie.wav")