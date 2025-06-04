from django.http import JsonResponse
from django.conf import settings
import threading
import time
import os
import wave
import sounddevice as sd
import numpy as np
import requests
import subprocess
from .tabs.Product import Product
from .tabs.Client import Client
from .tabs.Invoice import Invoice
from .tabs.Vendor import Vendor
from .tabs.Report import Report
from .constants import *
import joblib
from django.views.decorators.csrf import csrf_exempt
from api.constants import FEATURE_EXTRACTION_LOC
import json
# Global variable to control recording state
recording = False

# Audio settings
FORMAT = np.int16  # Audio format
CHANNELS = 1       # Mono audio
RATE = 44100       # Sample rate
DURATION = 20      # Maximum duration for recording (in seconds)

is_processing = False

tab_model = joblib.load(TAB_MODEL_PATH)

def snapshot_db():
    print("snapshotting the database state")
    
    env = os.environ.copy()
    env["MYSQL_PWD"] = "root"  # Set MySQL password in env variable

    subprocess.run([
        "mysqldump",
        "-u", "root",
        "invoice_assistant"
    ], stdout=open("snapshot.sql", "w"), env=env)

# def restore_db(s):
    

def transcribe_audio(audio_path):

    """Call ffmpeg to convert audio to 16-bit WAV and then run whisper.cpp to transcribe it."""
    snapshot_db()
    try: 
        
        # Step 1: Convert input audio (e.g., MP3) to 16kHz, mono, 16-bit WAV using ffmpeg
        output_wav_path = os.path.join(settings.MEDIA_ROOT, "output.wav")
        
        ffmpeg_command = [
            FFMPEG_EXECUTABLE,
            '-i', audio_path,           # Input file
            '-ar', '16000',              # Set sample rate to 16kHz
            '-ac', '1',                  # Set number of channels to 1 (mono)
            '-c:a', 'pcm_s16le',         # Set audio codec to PCM signed 16-bit little-endian
            output_wav_path              # Output file
        ]
        
        # Run ffmpeg to convert the audio
        
        ffmpeg_result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if ffmpeg_result.returncode != 0:
            raise Exception(f"Error converting audio with ffmpeg: {ffmpeg_result.stderr.decode()}")
        
        print(f"Audio converted to: {output_wav_path}")
        
        language_response = requests.get('http://localhost:8080/api/db/operation?operation=language')

        # Parse the JSON and extract the "status" field
        language = language_response.json().get("status", "").strip()
        print(f"The selected language is: {language}")
        if language == "hi":
            import whisper
            import torch
            os.makedirs(os.path.dirname(TRANSCRIBE_OUTPUT_PATH), exist_ok=True)
            # Load the desired model (large is best for Hindi)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = whisper.load_model("large", device=device)

            # Transcribe with forced Hindi language
            print("\nTranscribing hindi audio...")
            result = model.transcribe(output_wav_path, language="hi")
            print(f"Transcribing result: {result}")
            # Save to output file
            
            with open(TRANSCRIBE_OUTPUT_PATH, "w", encoding="utf-8") as f:
                f.write(result["text"])
            with open(TRANSCRIBE_OUTPUT_PATH, "r", encoding="utf-8") as file:
                transcript = file.read()
        else:
            # Whisper.cpp setup :
            # Step 2: Run whisper.cpp on the converted WAV file
            whisper_command = [
                WHISPER_CPP_EXECUTABLE, 
                '-f', output_wav_path,         # Provide the converted WAV file to whisper
                '--model', MODEL_PATH,          # Specify model path
                '-otxt', TRANSCRIBE_OUTPUT_PATH,       # Output file
                '-l', 'en'              # Specify language
            ]
            

            print("Running command:", " ".join(whisper_command))
            print("\nTranscribing english audio...")
            # Run whisper.cpp to transcribe the audio
            whisper_result = subprocess.run(whisper_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if whisper_result.returncode != 0:
                raise Exception(f"Error running whisper.cpp: {whisper_result.stderr.decode()}")
            
            # Step 3: Read the transcription from the output file
            with open(os.path.join(settings.MEDIA_ROOT,'output.wav.txt'), 'r') as file:
                transcript = file.read()
            
        print(transcript)
    except Exception as e:
        print(str(e))
    #         # Cleanup of media directory    
    try:
        for item in os.listdir(settings.MEDIA_ROOT):
            item_path = os.path.join(settings.MEDIA_ROOT, item)
            os.remove(item_path)    
    except FileNotFoundError:
        print(f"The directory {settings.MEDIA_ROOT} does not exist.")
    except Exception as e:
        print(f"Error clearing {settings.MEDIA_ROOT}: {e}")

    
    requests.post('http://localhost:8080/api/db/transcript',json={"transcript":transcript})
    
    # requests.post('http://localhost:8080/api/db/operation',json={
    #     "operation":"processing",
    #     "status": "true"
    #     })
    # print("JUST SET THE PROCESSING TO TRUE ")
    if language == "hi":
        from googletrans import Translator
        translator = Translator()
        translated = translator.translate(transcript, src='hi', dest='en')
        print(f"Hindi to english transcript: {translated.text}")
        return translated.text
    return transcript


def start_recording():
    """Record audio using sounddevice and save it to a temporary file."""
    global recording
    recording = True

    # Create an empty list to hold the audio frames
    audio_frames = []

    print("Recording started...")
    
    def callback(indata, frames, time, status):
        """Callback function to append the audio frames."""
        if status:
            print(status, file=sys.stderr)
        audio_frames.append(indata.copy())  # Append to the local variable

    # Start recording
    with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=RATE, dtype=FORMAT):
        time.sleep(DURATION)  # Record for DURATION seconds

    # Stop the recording
    recording = False
    print("Recording stopped.")

    # Save recorded audio to a temporary file
    temp_audio_path = os.path.join(settings.MEDIA_ROOT, "temp_recording.wav")
    with wave.open(temp_audio_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(FORMAT).itemsize)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))  # Join frames and write

    # Call the processing function with the recorded file
    handle_recording(temp_audio_path)

def stop_recording():
    """Stop the recording process."""
    global recording
    recording = False
    return JsonResponse({"status": "Recording stopped, processing audio..."})

def handle_recording(audio_path):
    """Process the recorded audio file."""
    
    try:
        # Transcribe the audio using whisper.cpp        
        transcript = transcribe_audio(audio_path)
        print("TRANSCRIPT: ", transcript)
    except Exception as e:
        print(str(e))
        return JsonResponse({'message': str(e)}), 500

    # get the Class (tab) prediction using the pickle file 
    # create object of that Class and call the function appropriate_function()
    # pass the appropriate_function() with the transcript again to get the specific function of that Class (tab)

    TAB_CLASS_MAPPING = {
        "Client": Client,  
        "Product": Product,
        "Report": Report,
        "Invoice": Invoice,        
        "Vendor": Vendor
    }

    print("Classifying tab...")

    
    # if "paid" in transcript or "receive" in transcript or "gave" in transcript or "transferred" in transcript or "received" in transcript or "transfer" in transcript or "lending" in transcript or "lent" in transcript or "money" in transcript or "debt" in transcript or "loan" in transcript:
        # tab_name = "Client"
        # class_to_call = TAB_CLASS_MAPPING[tab_name]  # Get the correct 
        # # instance = getattr(tabs, class_to_call)()  # Instantiate the class 
        # instance = class_to_call()  # Instantiate the class 
        # return instance.appropriate_function(transcript)  # Call the appropriate function 
    
    with open(FEATURE_EXTRACTION_LOC) as f: prompt = f.read()

    prompt += f""" Now extract from: '{transcript}' """

    OLLAMA_URL = "http://localhost:11434/api/generate"

    # API request payload
    data = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }        

    # print(f"\n\nThe prompt is , {prompt} ")

    response = requests.post(OLLAMA_URL, json=data)      
    
    if response.status_code == 200:
        try:
            response_string = response.json().get("response", "").strip()
            print(f"The Tab classification response string is {response_string}")
            output_texts = json.loads(response_string)

            print(f"The output_texts is {output_texts}")
            for output_text in output_texts: 
                try:
                    json_output = output_text
                    print(f"The json_output is {json_output}")
                    tab_name = json_output.get("type","").strip()
                    # tab_name = tab_model.predict([transcript])[0]  # Get the predicted tab name
                    print("The tab classified is: ", tab_name)

                    if tab_name in TAB_CLASS_MAPPING:
                        class_to_call = TAB_CLASS_MAPPING[tab_name]  # Get the correct 
                        # instance = getattr(tabs, class_to_call)()  # Instantiate the class 
                        instance = class_to_call()  # Instantiate the class 
                        instance.appropriate_function(transcript)  # Call the appropriate function  
                
                        requests.post('http://localhost:8080/api/db/operation',json={
                        "operation":"processing",
                        "status": "false"
                        })                 
                    else:
                        print("Error: No matching class found for this tab.")    
                        return JsonResponse({'error': 'No matching class found for this tab.'})
                except Exception as e:
                    print(f"\nERROR proccessing the request: {output_text}")
                    print(e)
        except Exception as e:
            print(f"\n ERROR {e}")

    print("JUST SET THE PROCESSING TO FALSE ")
    return JsonResponse({'message': 'No action taken'})

@csrf_exempt
def recording_control(request):
    """API endpoint to start/stop recording."""
    global recording
    action = request.GET.get("action", "")

    if action == "start" and not recording:
        threading.Thread(target=start_recording, daemon=True).start()
        return JsonResponse({"status": "Recording started"})

    elif action == "stop" and recording:
        return stop_recording()

    return JsonResponse({"status": "Invalid request"})

@csrf_exempt
def recoversnap(request):    
    print("restoring the database to previous state")
    env = os.environ.copy()
    env["MYSQL_PWD"] = "root"

    subprocess.run([
        "mysql",
        "-u", "root",
        "invoice_assistant"
    ], stdin=open("snapshot.sql", "r"), env=env)
    return JsonResponse({"status": "Invalid request"})