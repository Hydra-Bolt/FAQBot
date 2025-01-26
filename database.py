from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def getFromSupabase(question):

    resp = supabase.table("Questions").select("question, answer(answer)").eq("question", question).execute().data
    return resp[0]['answer']['answer']