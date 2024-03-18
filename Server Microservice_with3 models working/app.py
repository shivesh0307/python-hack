from flask import Flask, render_template, request,redirect
from speec2emotion import predict
from noiseIntensityDetection import findIntensity
from deepfakeDetection import predictDeepFake
from predict import predict as predictLive
from speechToText import recognize_from_file
from deepfake_cnn import predict_cnn
 
import tempfile
import os
import time
   

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
  return redirect("/voice/analyze")


@app.route("/ping", methods=["GET"])
def ping():
  return "pong", 200

@app.route("/voice/analyze", methods=["GET", "POST"])
def voice_analyze():
  if request.method == "GET":
    return render_template("voice_form.html")
  elif request.method == "POST":
    audio_file = request.files.get("audio_file")
    print(audio_file)
    if audio_file: 
      
      start_time=time.time()
      app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save the uploaded file to the same directory as app.py
      file_path = os.path.join(app_dir, audio_file.filename)
      audio_file.save(file_path)
      audio_data=audio_file.read()
      
      try:   
        intensity=findIntensity(file_path)
      except Exception as e:
        print("Intensity function error",e)
        intensity="Error in Intensity call"
      try:
        emotion=predict(file_path)
      except Exception as e:
        print("EMotion prediction function error",e)
        emotion="Error in Emotion prediction call"
      try:
        # ans=predictDeepFake(file_path)
        [pf,pr,ans]=predict_cnn(file_path)
        print(type(pf),pr)
      except Exception as e:
        print("Deepfake prediction function error",e)
        ans="Error in Deepfake prediction call"
      
        # audio_data = audio_file.read()
        # Export the audio to WAV format
      try:
        live=predictLive(file_path)[0]
      except Exception as e:
        print("Livliness prediction function error",e)
        live="Error in liveliness prediction call"

      try:
       language, text, msg=recognize_from_file(file_path)
      except Exception as e:
        print("Speech to Text function error",e)
        language="Error in speech to text call"
        text="Error in speech to text call"
        msg="Error"

      #text="dummy"
      end_time=time.time()
      try:
        if os.path.exists(file_path):
            print("file removed")
            os.remove(file_path)
      except:
        print("Error deleting mp3 file")
      filename = audio_file.filename
      detectedVoice= "False" if (text is None or text == "") else "True"
      detectedVoice = text
      print("detectedVoice",detectedVoice)
      return {
              "status":"success",
              "analysis":{ 
                "detectedVoice":detectedVoice,
                "voiceType":ans,
                
                "confidenceScore":{
                  "aiProbability":pf,
                  "humanProbability":pr,
                },
                "additionalInfo":{
                  "emotionalTone":emotion,
                  "backgroundNoiseLevel":intensity,
                  "language":language,
                  "text": text,
                  "liveliness":(1-live),
                }
              },
              "responseTime":end_time-start_time,
              "fileName": filename,
            }
    else:
      return "No audio file uploaded.", 400

if __name__ == "__main__":
  app.run(debug=True)  