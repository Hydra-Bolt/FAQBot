import os
import requests
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def getFromSupabase(question):
    

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    query = {
        "select": "question, answer(answer)",
        "question": f"eq.{question}"
    }
    response = requests.get(f"{url}/rest/v1/Questions", headers=headers, params=query)
    data = response.json()
    return data[0]['answer']['answer'] if data else None
