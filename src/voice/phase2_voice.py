import os
import asyncio
import pyaudio
import wave
import whisper # Local transcription for 100% MIME stability
import boto3
from dotenv import load_dotenv

load_dotenv()

# Load Whisper once globally
voice_model = whisper.load_model("base")

class VisionaryVoice:
    def __init__(self):
        self.model_id = "amazon.nova-lite-v1:0" 
        self.client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
        self.pa = pyaudio.PyAudio()

    def record_and_transcribe(self, seconds=4):
        print(f"[*] EARS: Listening for {seconds}s...")
        stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * seconds))]
        stream.stop_stream(); stream.close()

        with wave.open("query.wav", 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16)); wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
        
        print("[*] EARS: Transcribing locally...")
        return voice_model.transcribe("query.wav")["text"]

    async def run_session(self):
        user_text = self.record_and_transcribe()
        print(f"[User Said]: {user_text}")
        
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": f"The user asked: {user_text}. Please reply naturally."}]}]
            )
            print(f"Nova: {response['output']['message']['content'][0]['text']}")
        except Exception as e:
            print(f"[!] API Error: {e}")

if __name__ == "__main__":
    asyncio.run(VisionaryVoice().run_session())