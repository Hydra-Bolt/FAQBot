import os
import requests
from dotenv import load_dotenv

from utils.faq_embeddings import deleteFAQ, insertFAQ

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

def getFromSupabase(question=None):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    query = {
        "select": "question, answer(answer)"
    }
    
    if question:
        query["question"] = f"eq.{question}"
    else:
        query["select"] = "id, question, answer(id, answer)"
    
    response = requests.get(f"{url}/rest/v1/Questions", headers=headers, params=query)
    data = response.json()
    
    if question:
        return data[0]['answer']['answer'] if data else None
    else:
        return {
            item['question']: {
                'q_id': item['id'],
                "id": item['answer']['id'],
                "answer": item['answer']['answer']
            } for item in data
        }

def updateSupabase(id, new_val, table):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    data = {}
    if table == "Answers":
        data["answer"] = new_val
    elif table == "Questions":
        data["question"] = new_val
    
    query = {
        "id": f"eq.{id}"
    }
    
    response = requests.patch(f"{url}/rest/v1/{table}", headers=headers, params=query, json=data)
    
    if response.status_code == 200 and table == "Questions":
        # Delete old FAQ entry and insert new one
        if not insertFAQ([str(id)], [new_val]):
            return False
    
    return response.status_code == 200  # 200 OK indicates success when using return=representation

def insertToSupabase(questions, answer):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    # Insert the answer
    answer_data = {"answer": answer}
    answer_response = requests.post(f"{url}/rest/v1/Answers", headers=headers, json=answer_data)
    
    if answer_response.status_code != 201:
        return False
    
    answer_id = answer_response.json()[0]['id']
    
    # Insert the questions
    question_data = [{"question": question, "answer": answer_id} for question in questions]
    question_response = requests.post(f"{url}/rest/v1/Questions", headers=headers, json=question_data)
    
    if question_response.status_code != 201:
        return False
    
    question_ids = [str(item['id']) for item in question_response.json()]
    if not insertFAQ(question_ids, questions):
        print("Failed to insert FAQ entries")
        return False
    
    return True

def insertQuestionToSupabase(id, new_questions):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    # Insert the questions
    question_data = [{"question": question, "answer": id} for question in new_questions]
    question_response = requests.post(f"{url}/rest/v1/Questions", headers=headers, json=question_data)

    if question_response.status_code != 201:
        return False
    
    question_ids = [str(item['id']) for item in question_response.json()]
    if not insertFAQ(question_ids, new_questions):
        print("Failed to insert FAQ entries")
        return False
    
    return True

def deleteFromSupabase(id, table):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    if table == "Answers":
        # Delete questions associated with the answer
        question_query = {"answer": f"eq.{id}"}
        question_response = requests.delete(f"{url}/rest/v1/Questions", headers=headers, params=question_query)
        
        if question_response.status_code != 200:
            print("Failed to delete questions")
            return False

        question_ids = [str(item['id']) for item in question_response.json()]
        if not deleteFAQ(question_ids):
            print("Failed to delete FAQ entries")
            return False

        # Delete the answer
        answer_query = {"id": f"eq.{id}"}
        answer_response = requests.delete(f"{url}/rest/v1/Answers", headers=headers, params=answer_query)
        
        if answer_response.status_code != 200:
            print("Failed to delete answers")
            return False

    elif table == "Questions":
        # Delete the question by id
        question_query = {"id": f"eq.{id}"}
        question_response = requests.delete(f"{url}/rest/v1/Questions", headers=headers, params=question_query)
        
        if question_response.status_code != 200:
            print("Failed to delete question")
            return False
            
        # Delete the FAQ entry
        if not deleteFAQ([str(id)]):
            print("Failed to delete FAQ entry")
            return False

    return True
