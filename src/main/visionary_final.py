import asyncio
import os
import pyaudio
import wave
import boto3
import whisper
import pyautogui # For universal screen capture
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Load Whisper model globally
print("[*] Loading local Voice Recognition engine...")
voice_model = whisper.load_model("base")

class VisionaryMaster:
    def __init__(self):
        # Use Nova Pro for high-quality system analysis
        self.model_id = "amazon.nova-pro-v1:0" 
        self.region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.client = boto3.client("bedrock-runtime", region_name=self.region)
        self.pa = pyaudio.PyAudio()
    async def capture_screen(self):
        """
        Uses native Fedora/GNOME screenshot for better security authorization.
        """
        print("[*] EYES: Capturing your actual desktop screen...")
        screenshot_path = "system_screen.png"
        
        # Use a system call to capture the screen natively
        # This bypasses the Xlib Authorization error
        try:
            os.system(f"gnome-screenshot -f {screenshot_path}")
            await asyncio.sleep(1) # Short pause to ensure file is written
            
            with open(screenshot_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"[!] Native capture failed, falling back: {e}")
            # Final fallback to pyautogui
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            with open(screenshot_path, "rb") as f:
                return f.read()
            
    def record_and_transcribe(self, seconds=5):
        print(f"[*] EARS: Recording for {seconds}s... Ask your question!")
        stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * seconds))]
        stream.stop_stream(); stream.close()

        temp_wav = "query.wav"
        with wave.open(temp_wav, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16)); wf.setframerate(16000)
            wf.writeframes(b''.join(frames))
        
        print("[*] EARS: Transcribing locally...")
        return voice_model.transcribe(temp_wav)["text"]

    async def run_visionary(self):
        # 1. Capture Eyes (System Desktop)
        image_bytes = await self.capture_screen()
        
        # 2. Capture Ears
        user_text = self.record_and_transcribe()
        print(f"[User Said]: {user_text}")
        
        if not user_text.strip():
            print("[!] No voice detected.")
            return

        print("[*] BRAIN: Analyzing your screen...")
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{
                    "role": "user",
                    "content": [
                        {"image": {"format": "png", "source": {"bytes": image_bytes}}},
                        {"text": f"The user is visually impaired and asked: '{user_text}'. Describe what is currently on their computer screen."}
                    ]
                }]
            )
            
            answer = response['output']['message']['content'][0]['text']
            print("\n" + "="*40 + "\nVISIONARY RESPONSE:\n" + answer + "\n" + "="*40)
            
        except Exception as e:
            print(f"[!] AWS Error: {e}")

if __name__ == "__main__":
    vm = VisionaryMaster()
    # No more Amazon URL needed; it sees your whole screen!
    asyncio.run(vm.run_visionary())


# import asyncio
# import os
# import io
# import boto3
# import pyautogui
# from botocore.config import Config
# from dotenv import load_dotenv

# load_dotenv()

# class VisionaryLive:
#     def __init__(self):
#         # Using Nova Pro for the most intelligent live reasoning
#         self.model_id = "amazon.nova-pro-v1:0" 
#         self.client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
#         self.is_running = True

#     async def get_live_frame(self):
#         """Captures screen directly into RAM buffer (No file stored)."""
#         buffer = io.BytesIO()
#         screenshot = pyautogui.screenshot()
#         # Resize slightly to reduce latency while maintaining detail
#         screenshot = screenshot.resize((1024, 768)) 
#         screenshot.save(buffer, format="PNG")
#         return buffer.getvalue()

#     async def stream_observation(self):
#         print("[*] LIVE MODE ACTIVE: I am watching your workspace...")
        
#         while self.is_running:
#             # 1. Grab frame from memory
#             frame_bytes = await self.get_live_frame()
            
#             try:
#                 # 2. Use ConverseStream for real-time text output
#                 # This doesn't wait for the whole answer; it streams word-by-word
#                 response = self.client.converse_stream(
#                     modelId=self.model_id,
#                     messages=[{
#                         "role": "user",
#                         "content": [
#                             {"image": {"format": "png", "source": {"bytes": frame_bytes}}},
#                             {"text": "You are a live observer. Briefly describe the current state of my screen in one sentence."}
#                         ]
#                     }],
#                     inferenceConfig={"maxTokens": 100, "temperature": 0.5}
#                 )

#                 print("\r[NOVA]: ", end="", flush=True)
#                 for event in response['stream']:
#                     if 'contentBlockDelta' in event:
#                         print(event['contentBlockDelta']['delta']['text'], end="", flush=True)
#                 print("\n")

#             except Exception as e:
#                 print(f"\n[!] Stream Error: {e}")
            
#             # 3. Control the 'Frame Rate' (e.g., check every 5 seconds)
#             # You can lower this to 2-3s, but mind your AWS costs!
#             await asyncio.sleep(5) 

# if __name__ == "__main__":
#     live_ai = VisionaryLive()
#     try:
#         asyncio.run(live_ai.stream_observation())
#     except KeyboardInterrupt:
#         print("\n[*] Live Mode Deactivated.")