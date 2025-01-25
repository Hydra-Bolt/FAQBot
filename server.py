import os
from flask import Flask, request
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
from gen_from_embed import generateFromEmbeddingsWithoutHistory
from telegram_utils import (
    sendMessage,
)
import openai

app = Flask(__name__)

load_dotenv()
# Constants
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Dictionary to maintain chat history
chat_history = {}

def generate_response_with_chatgpt(question, chat_id):
    history = chat_history.get(chat_id, [])
    history.append(HumanMessage(content=question))

    response, source = generateFromEmbeddingsWithoutHistory(question)
    
    history.append(AIMessage(content=response))
    chat_history[chat_id] = history
    
    return response

def handleMessage(message_data):
    try:
        if "message" in message_data:
            message: dict = message_data["message"]
            chat_id = message["chat"]["id"]
            message_id = message["message_id"]
            username = message["from"]["first_name"]

            text: str = message.get("text", "No text found")

            if text.startswith("/"):
                if text=="/start":
                    response = "¡Bienvenido al FAQ Bot de Vivir de Ingresos Pasivos! Estoy aquí para ayudarte con cualquier pregunta que tengas sobre estrategias de ingresos pasivos, herramientas de inversión y servicios ofrecidos en nuestro sitio web."
                else: 
                    response = "Lo siento, no entiendo ese comando."
                
            else:
                response = generate_response_with_chatgpt(text, chat_id)
            
            sendMessage(response, chat_id)
    except KeyError as e:
        print(f"KeyError: {e}")
        sendMessage("Lo siento, ha ocurrido un error procesando tu mensaje.", chat_id)
    except Exception as e:
        print(f"An error occurred: {e}")
        sendMessage("Lo siento, ha ocurrido un error inesperado.", chat_id)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.get_json()
        handleMessage(message)
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True)
