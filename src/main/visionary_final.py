import asyncio
import os
import io
import boto3
import whisper
import pyautogui
import wave
import pyaudio
import subprocess 
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION & PATHS ---
base_dir = Path(__file__).resolve().parent.parent.parent
dotenv_path = base_dir / "config" / ".env"
load_dotenv(dotenv_path=dotenv_path)

print("[*] Loading local Voice Recognition engine...")
voice_model = whisper.load_model("base")

class VisionaryMaster:
    def __init__(self):
        self.region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        # Explicit credentials for Fedora stability
        self.bedrock = boto3.client("bedrock-runtime", region_name=self.region)
        self.polly = boto3.client("polly", region_name=self.region)
        self.model_id = "amazon.nova-pro-v1:0"
        self.pa = pyaudio.PyAudio()

    def speak_and_wait(self, text):
        """Sequential Mouth: Narration that blocks until finished."""
        if not text: return
        clean_text = text.replace('*', '').replace('#', '').replace('-', ' ')
        print(f"\n[*] ASSISTANT: {clean_text}\n")
        
        try:
            response = self.polly.synthesize_speech(
                Text=clean_text, 
                OutputFormat="mp3", 
                VoiceId="Joanna",
                Engine="neural"
            )
            temp_voice = "ai_voice.mp3"
            with open(temp_voice, "wb") as f:
                f.write(response['AudioStream'].read())
            
            # Blocking call ensures we don't capture until speaking is done
            subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_voice])
        except Exception as e:
            print(f"[!] Voice Error: {e}")

    async def listen_for_command(self):
        """USP: Non-stop Ears. Records a 4s window to check for user questions."""
        rate, chunk = 16000, 1024
        stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
        
        print("[*] EARS: Listening for your question...")
        frames = [stream.read(chunk) for _ in range(0, int(rate / chunk * 4))]
        stream.stop_stream(); stream.close()

        temp_wav = "ear_input.wav"
        with wave.open(temp_wav, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16)); wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        
        # Local transcription ensures the AI 'hears' your specific request
        result = voice_model.transcribe(temp_wav, fp16=False)
        return result["text"].strip()

    async def run_visionary_cycle(self):
        print("[*] VISIONARY ONLINE: Personalized Assistant Mode")
        
        while True:
            # STEP 1: Capture (Eyes)
            print("\n[*] STEP 1: Capturing screen...")
            screen = pyautogui.screenshot()
            buffer = io.BytesIO()
            screen.save(buffer, format="PNG")
            
            # STEP 2: Listen (Ears)
            user_query = await self.listen_for_command()
            
            # STEP 3: Analyze (Brain)
            print(f"[*] STEP 2: Thinking... (User Query: '{user_query}')")
            
            # USP: Context-Aware Targeting
            if len(user_query) > 7:
                # If you ask a question, we focus ONLY on that
                prompt = (
                    f"The user asked: '{user_query}'. Answer this question concisely but with "
                    "all necessary detail based on the current screen. Ignore irrelevant info."
                )
            else:
                # If silent, provide a detailed but precise layout summary
                prompt = (
                    "Provide a precise, detailed overview of the active window and main content. "
                    "Focus on what has changed or what is most important for a visually impaired user."
                )

            try:
                response = self.bedrock.converse(
                    modelId=self.model_id,
                    messages=[{"role": "user", "content": [
                        {"image": {"format": "png", "source": {"bytes": buffer.getvalue()}}},
                        {"text": prompt}
                    ]}],
                    inferenceConfig={"maxTokens": 400, "temperature": 0.7}
                )
                
                answer = response['output']['message']['content'][0]['text']
                
                # STEP 4: Speak and Prepare for Next (Mouth)
                self.speak_and_wait(answer)
                
            except Exception as e:
                print(f"[!] Brain Error: {e}")

            # Prepare for immediate next capture
            print("[*] Preparing next snapshot...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    vm = VisionaryMaster()
    try:
        asyncio.run(vm.run_visionary_cycle())
    except KeyboardInterrupt:
        print("\n[*] Visionary Offline.")

# import asyncio
# import os
# import pyaudio
# import wave
# import boto3
# import whisper
# import pyautogui # For universal screen capture
# from botocore.config import Config
# from dotenv import load_dotenv

# load_dotenv()

# # Load Whisper model globally
# print("[*] Loading local Voice Recognition engine...")
# voice_model = whisper.load_model("base")

# class VisionaryMaster:
#     def __init__(self):
#         # Use Nova Pro for high-quality system analysis
#         self.model_id = "amazon.nova-pro-v1:0" 
#         self.region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
#         self.client = boto3.client("bedrock-runtime", region_name=self.region)
#         self.pa = pyaudio.PyAudio()
#     async def capture_screen(self):
#         """
#         Uses native Fedora/GNOME screenshot for better security authorization.
#         """
#         print("[*] EYES: Capturing your actual desktop screen...")
#         screenshot_path = "system_screen.png"
        
#         # Use a system call to capture the screen natively
#         # This bypasses the Xlib Authorization error
#         try:
#             os.system(f"gnome-screenshot -f {screenshot_path}")
#             await asyncio.sleep(1) # Short pause to ensure file is written
            
#             with open(screenshot_path, "rb") as f:
#                 return f.read()
#         except Exception as e:
#             print(f"[!] Native capture failed, falling back: {e}")
#             # Final fallback to pyautogui
#             import pyautogui
#             screenshot = pyautogui.screenshot()
#             screenshot.save(screenshot_path)
#             with open(screenshot_path, "rb") as f:
#                 return f.read()
            
#     def record_and_transcribe(self, seconds=5):
#         print(f"[*] EARS: Recording for {seconds}s... Ask your question!")
#         stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
#         frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * seconds))]
#         stream.stop_stream(); stream.close()

#         temp_wav = "query.wav"
#         with wave.open(temp_wav, 'wb') as wf:
#             wf.setnchannels(1); wf.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16)); wf.setframerate(16000)
#             wf.writeframes(b''.join(frames))
        
#         print("[*] EARS: Transcribing locally...")
#         return voice_model.transcribe(temp_wav)["text"]

#     async def run_visionary(self):
#         # 1. Capture Eyes (System Desktop)
#         image_bytes = await self.capture_screen()
        
#         # 2. Capture Ears
#         user_text = self.record_and_transcribe()
#         print(f"[User Said]: {user_text}")
        
#         if not user_text.strip():
#             print("[!] No voice detected.")
#             return

#         print("[*] BRAIN: Analyzing your screen...")
#         try:
#             response = self.client.converse(
#                 modelId=self.model_id,
#                 messages=[{
#                     "role": "user",
#                     "content": [
#                         {"image": {"format": "png", "source": {"bytes": image_bytes}}},
#                         {"text": f"The user is visually impaired and asked: '{user_text}'. Describe what is currently on their computer screen."}
#                     ]
#                 }]
#             )
            
#             answer = response['output']['message']['content'][0]['text']
#             print("\n" + "="*40 + "\nVISIONARY RESPONSE:\n" + answer + "\n" + "="*40)
            
#         except Exception as e:
#             print(f"[!] AWS Error: {e}")

# if __name__ == "__main__":
#     vm = VisionaryMaster()
#     # No more Amazon URL needed; it sees your whole screen!
#     asyncio.run(vm.run_visionary())

 