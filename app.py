from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

# Load the hidden API key from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Allows index.html to communicate with this server

# Initialize the Groq client securely
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/api/chat', methods=['POST'])
def chat():
    print("🚨 INCOMING REQUEST DETECTED!") # <-- ADD THIS
    try:
        data = request.json
        print(f"🧠 Message received: {data.get('messages')}")
        model = data.get('model', 'llama-3.3-70b-versatile')
        messages = data.get('messages', [])
        
        # Call Groq securely from the backend
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.5,
            max_tokens=1024
        )
        
        reply = chat_completion.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)