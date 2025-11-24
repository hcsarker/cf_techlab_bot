from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np, pickle, json, random

app = Flask(__name__)

model = load_model('chatbot_model.h5')
tokenizer, encoder = pickle.load(open('tokenizer.pkl', 'rb'))
data = json.load(open('data.json'))

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message']
    
    seq = tokenizer.texts_to_sequences([msg])
    padded = pad_sequences(seq, maxlen=model.input_shape[1], padding='post')
    
    pred = model.predict(padded)
    tag = encoder.inverse_transform([np.argmax(pred)])[0]

    for intent in data['intents']:
        if intent['tag'] == tag:
            return jsonify({'reply': random.choice(intent['responses'])})

    return jsonify({"reply": "Sorry, I didn't understand that."})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
