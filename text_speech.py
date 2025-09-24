# Syntesize all your text into a Ghanaian language
import os
import requests
from dotenv import load_dotenv
from playsound3 import playsound

# load env variables
load_dotenv()

class TextSpeech:
    def __init__(self, text: str = ""):
        self.text = text
        self.ghana_nlp_key = os.getenv("GHANA_NLP_KEY")
        self.filename = "audio/audio.wav"
        self.tts_url = "https://translation-api.ghananlp.org/tts/v1/synthesize"
        self.tran_url = "https://translation-api.ghananlp.org/v1/translate"

    def save_audio_to_file(self, audio_data: bytes):
        """
        Save audio data to a file.
        """
        try:
            with open(self.filename, "wb") as f:
                f.write(audio_data)
        except Exception as e:
            print(f"Error saving audio file: {e}")
    
    def text_to_speech(self, code: str="tw", speaker_code="twi_speaker_9"):
        """
        Convert text to speech using Ghana NLP TTS API.
        """
        if not self.text or not self.text.strip():
            return None

        # convert to twi/preferred local language if necessary
        if code != "en":
            self.text = self.translate(text=self.text, lan_code=code)

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.ghana_nlp_key
        }

        if code not in ["tw", "ee", "ki"]: # languages currently supported by API
            payload = {"text": self.text, "language": "tw", "speaker_id": speaker_code}
        else:
            payload = {"text": self.text, "language": code, "speaker_id": speaker_code}

        try:
            response = requests.post(self.tts_url, json=payload, headers=headers)
            if response.status_code == 200:
                self.save_audio_to_file(response.content)
        except Exception as e:
            return f"TTS error: {e}"

    def translate(self, text: str, lan_code: str):
        """
        Translate text to specified local language.
        """
        code = f"en-{lan_code}"
        
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.ghana_nlp_key
        }
        
        payload = {
            "in": text,
            "lang": code
        }
        
        try:
            response = requests.post(self.tran_url, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                return str(response.json())
            else:
                print(f"Translation API error: {response.status_code}")
                return text
                
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def play_audio(self):
        """
        Play audio from a file.
        """
        try:
            playsound(self.filename)
        except Exception as e:
            print(f"Error playing audio: {e}")