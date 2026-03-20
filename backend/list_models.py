import sys
sys.path.insert(0, ".")
from rag_engine import get_api_key
from google import genai

api_key = get_api_key()
client = genai.Client(api_key=api_key)

print("Available models:")
for m in client.models.list():
    if 'generate' in str(m.supported_actions).lower() or 'flash' in m.name.lower() or 'pro' in m.name.lower():
        print(f"  {m.name}")
