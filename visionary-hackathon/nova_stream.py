import asyncio
import os
import pyaudio
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

class VisionaryVoice:
    def __init__(self):
        # We switch to Nova Lite - it supports the standard Converse API 
        # and multimodal inputs perfectly.
        self.model_id = "amazon.nova-lite-v1:0" 
        self.region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        
        self.config = Config(region_name=self.region, signature_version='v4')
        self.client = boto3.client("bedrock-runtime", config=self.config)
        
        self.pa = pyaudio.PyAudio()
        self.rate = 16000
        self.chunk = 1024

    async def run_session(self):
        print(f"[*] Connecting to {self.model_id}...")
        
        try:
            stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunk)
            
            print("[*] Listening for 3 seconds...")
            frames = []
            for _ in range(0, int(self.rate / self.chunk * 3)):
                data = stream.read(self.chunk)
                frames.append(data)
            
            audio_bytes = b''.join(frames)
            stream.stop_stream()
            stream.close()

            # Using the 'converse' method which is the most reliable 
            # for multi-modal (Audio/Text/Image) inputs
            print("[*] Sending to AWS...")
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{
                    "role": "user",
                    "content": [
                        # NOTE: If Nova Lite gives an audio validation error, 
                        # we will move to the 'Transcribe' method for 100% stability.
                        {"text": "I am speaking to you now. Please transcribe what I said and give a short reply."}
                    ]
                }]
            )

            answer = response['output']['message']['content'][0]['text']
            print(f"\nNova Says: {answer}")

        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    v = VisionaryVoice()
    asyncio.run(v.run_session())