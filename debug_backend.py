import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env
load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    # Print first few chars to verify it's the new one (if user changed it)
    print(f"API Key starts with: {api_key[:4]}...")

def test_gemini():
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Trying the specific version first
        print("Attempting to generate content with 'gemini-1.5-flash'...")
        response = model.generate_content("Hello, are you working?")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error with 'gemini-1.5-flash': {e}")
        
    try:
        print("Attempting to generate content with 'gemini-flash-latest'...")
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Hello, are you working?")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error with 'gemini-flash-latest': {e}")

if __name__ == "__main__":
    test_gemini()
