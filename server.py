from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere 
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
CORS(app)

api_key = os.getenv("COHERE_API_KEY")
print(f"API Key: {api_key}")  
co = cohere.Client(api_key)

@app.route('/')
def home():
    return 'Welcome to the Chatbot Server'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message=request.json.get('message')
        print(f"User Message: {user_message}")

        response=co.generate(
            model='command',
            prompt=user_message,
            max_tokens=200,
            temperature=0.7
        )


        bot_reply=response.generations[0].text.strip()
        print(f"Bot Reply: {bot_reply}")

        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, something went wrong. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
