import os
import requests
from dotenv import load_dotenv

from utils.faq_embeddings import insertFAQ

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def getFromSupabase(question=None):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    if question:
        query = {
            "select": "question, answer(answer)",
            "question": f"eq.{question}"
        }
    else:
        query = {
            "select": "id, question, answer(id, answer)"
        }
    response = requests.get(f"{url}/rest/v1/Questions", headers=headers, params=query)
    data = response.json()
    if question:
        return {
            "id": data[0]['id'],
            "answer": data[0]['answer']['answer']
        } if data else None
    else:
        return {
            item['question']: {
                'q_id': item['id'],
                "id":  item['answer']['id'],
                "answer": item['answer']['answer']
            } for item in data
        }

def updateSupabase(answer_id, new_answer):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "answer": new_answer
    }
    query = {
        "id": f"eq.{answer_id}"
    }
    response = requests.patch(f"{url}/rest/v1/Answers", headers=headers, params=query, json=data)
    return response.status_code == 204  # 204 No Content indicates success

def insertToSupabase(questions, answer):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    data = {
        "answer": answer
    }
    response = requests.post(f"{url}/rest/v1/Answers", headers=headers, json=data)
    if response.status_code == 201:
        answer_id = response.json()[0]['id']
        for question in questions:
            question_data = {
                "question": question,
                "answer": answer_id
            }
            question_response = requests.post(f"{url}/rest/v1/Questions", headers=headers, json=question_data)
            if question_response.status_code != 201:
                return False
            insertFAQ(question)
        return True
    return False