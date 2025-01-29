import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from langchain.schema import HumanMessage, AIMessage, Document
from dotenv import load_dotenv
from utils.database import deleteFromSupabase, getFromSupabase, updateSupabase, insertToSupabase
from utils.gen_from_embed import generateAnswerFromSources
from utils.telegram_utils import sendMessage
from utils.faq_embeddings import getTopK
import json
import traceback

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

load_dotenv(".env")
# Constants
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
ADMIN_ID = os.getenv("ADMIN_ID")


# Dictionary to maintain chat history
chat_history = {}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            user = User(id=username)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def generateResponse(question, chat_id):
    history = chat_history.get(chat_id, [])
    history.append(HumanMessage(content=question))

    if len(history) > 10:
        history = history[-10:]

    sources = getTopK(question, 5)
    print(json.dumps(sources, indent=4, default=str))
    if sources and sources[0][1] > 0.93:
        question = sources[0][0].page_content
        response = getFromSupabase(question)
    else:
        print("No Match Found")
        unique_sources = {source[0].page_content: source for source in sources}.values()
        unique_answers = {getFromSupabase(source[0].page_content): source for source in unique_sources}.keys()
        answers = [Document(page_content=answer) for answer in unique_answers]
        print(json.dumps(answers, indent=4, default=str))
        response = generateAnswerFromSources(question, answers, history)

    history.append(AIMessage(content=response))
    chat_history[chat_id] = history

    return response

def handleMessage(message_data):
    try:
        if "message" in message_data:
            message: dict = message_data["message"]
            chat_id = message["from"]["id"]
            text: str = message.get("text", "No text found")

            if str(chat_id) == ADMIN_ID:
                response = "Welcome, Admin!"
            elif text.startswith("/"):
                if text == "/start":
                    response = "¡Hola! Soy la IA del Club VIP y estoy aquí para ayudarte con cualquier pregunta que tengas sobre las estrategias y servicios que ofrecemos."
                else:
                    response = "Lo siento, no entiendo ese comando."
            else:
                response = generateResponse(text, chat_id)

            sendMessage(response, chat_id)
    except KeyError as e:
        print(f"KeyError: {e}")
        traceback.print_exc()
        sendMessage("Lo siento, ha ocurrido un error procesando tu mensaje.", chat_id)
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        sendMessage("Lo siento, ha ocurrido un error inesperado.", chat_id)

@app.route("/dashboard")
@login_required
def dashboard():
    # Fetch messages from Supabase
    messages = getFromSupabase()  # Adjust this function to fetch all messages

    # Group answers and questions
    grouped_messages = {}
    for question, data in messages.items():
        id = data["id"]
        answer = data["answer"]
        if answer in grouped_messages:
            grouped_messages[answer][1].append(question)
        else:
            grouped_messages[answer] = (id, [question])
            # Sort grouped_messages by the answer id
    sorted_grouped_messages = dict(
        sorted(grouped_messages.items(), key=lambda item: item[1][0])
    )

    return render_template("dashboard.html", messages=sorted_grouped_messages)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    try:
        data = request.get_json()
        id = data.get("id")

        if not id:
            return jsonify({"error": "Invalid input"}), 400

        # Delete the entry from the database
        delete_status = deleteFromSupabase(id)  # Adjust this function to delete the entry

        if delete_status:
            return jsonify({"message": "Deletion successful", "success": True}), 200
        else:
            return jsonify({"error": "Deletion failed", "success": False}), 500
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return jsonify({"error": "An error occurred", "success": False}), 500

@app.route("/update", methods=["POST"])
@login_required
def update():
    try:
        data = request.get_json()
        id = data.get("id")
        answer = data.get("answer")

        if not id or not answer:
            return jsonify({"error": "Invalid input", "success": False}), 400

        # Update the database with the new question and answer
        update_status = updateSupabase(
            id, answer
        )  # Adjust this function to update the database

        if update_status:
            return jsonify({"message": "Update successful", "success": True}), 200
        else:
            return jsonify({"error": "Update failed", "success": False}), 500
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return jsonify({"error": "An error occurred", "success": False}), 500

@app.route("/add", methods=["POST"])
@login_required
def add():
    try:
        data = request.get_json()
        questions = data.get("questions")
        answer = data.get("answer")
        print(questions, answer)

        if not questions or not answer:
            return jsonify({"error": "Invalid input", "success": False}), 400

        add_status = insertToSupabase(
            questions, answer
        )  
        
        if add_status:
            return jsonify({"success": True, "message": "Addition successful"}), 200
        else:
            return jsonify({"error": "Addition failed", "success": False}), 500
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()
        return jsonify({"error": "An error occurred", "success": False}), 500

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.get_json()
        print(message)
        handleMessage(message)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)