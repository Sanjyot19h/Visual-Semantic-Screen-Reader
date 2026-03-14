import os
import asyncio
import boto3
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

MODEL_ID = "amazon.nova-pro-v1:0" 
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
TARGET_URL = "https://www.amazon.com/dp/B09B8YG2YW"

async def capture_screen(url):
    print(f"[*] EYES: Navigating to {url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        await page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        
        try:
            # wait_until="load" ensures the base page is there
            await page.goto(url, wait_until="load", timeout=60000)
            await asyncio.sleep(6) # Essential for dynamic Amazon content
            screenshot_bytes = await page.screenshot(type="png")
            await browser.close()
            return screenshot_bytes
        except Exception as e:
            print(f"[!] Browser Error: {e}")
            await browser.close()
            return None

def analyze_with_nova(image_bytes):
    if not image_bytes: return
    client = boto3.client("bedrock-runtime", region_name=REGION)
    prompt = "Describe this product, its price, and the location of the 'Add to Cart' button for a visually impaired user."
    
    try:
        response = client.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"image": {"format": "png", "source": {"bytes": image_bytes}}}, {"text": prompt}]}]
        )
        print("\n" + "="*40 + "\nNOVA ANALYSIS:\n" + response['output']['message']['content'][0]['text'] + "\n" + "="*40)
    except Exception as e:
        print(f"[!] Bedrock Error: {e}")

async def main():
    img_data = await capture_screen(TARGET_URL)
    analyze_with_nova(img_data)

if __name__ == "__main__":
    asyncio.run(main())