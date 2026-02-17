import requests
import os
from src.config import Config

def test_hf():
    token = Config.HF_TOKEN
    print(f"Testing HF Token: {token[:4]}...{token[-4:]}")
    
    # Test 2: SVD Video
    model = "stabilityai/stable-video-diffusion-img2vid-xt"
    
    urls_to_test = [
        f"https://router.huggingface.co/hf-inference/models/{model}",
        f"https://router.huggingface.co/models/{model}",
        f"https://api-inference.huggingface.co/models/{model}"
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    # SVD needs data inputs usually, but for URL check simple json might trigger 400 not 404 if found
    payload = {"inputs": "A cat", "parameters": {}} 
    
    print(f"\nTesting Model: {model}")
    
    for url in urls_to_test:
        print(f"\nTrying URL: {url}")
        try:
            response = requests.post(url, headers=headers, json=payload)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Success! Image bytes received.")
                break
            else:
                print("Error Response:")
                print(response.text[:200])
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_hf()
