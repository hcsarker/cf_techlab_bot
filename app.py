from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import json
import random
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load model and data
try:
    model = load_model('chatbot_model.h5')
    tokenizer, encoder = pickle.load(open('tokenizer.pkl', 'rb'))
    data = json.load(open('data.json'))
    logging.info("Model and data loaded successfully")
except Exception as e:
    logging.error(f"Error loading model/data: {str(e)}")
    raise

@app.route('/')
def index():
    """Serve the main chat interface"""
    return send_from_directory('static', 'index.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None
    }), 200

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with improved error handling and confidence threshold"""
    try:
        # Validate request
        if not request.json or 'message' not in request.json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        msg = request.json['message'].strip()
        
        if not msg:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Log incoming message
        logging.info(f"Received message: {msg}")
        
        # Process message
        seq = tokenizer.texts_to_sequences([msg])
        padded = pad_sequences(seq, maxlen=model.input_shape[1], padding='post')
        
        # Get prediction with confidence
        pred = model.predict(padded, verbose=0)
        confidence = np.max(pred)
        tag_index = np.argmax(pred)
        tag = encoder.inverse_transform([tag_index])[0]
        
        logging.info(f"Predicted tag: {tag}, Confidence: {confidence:.2f}")
        
        # Confidence threshold - if too low, return default response
        if confidence < 0.5:
            response = "I'm not quite sure about that. Could you please rephrase or ask something else? You can ask about our services, pricing, contact info, or portfolio!"
            logging.warning(f"Low confidence ({confidence:.2f}) for message: {msg}")
        else:
            # Find and return response for the predicted intent
            response = None
            for intent in data['intents']:
                if intent['tag'] == tag:
                    response = random.choice(intent['responses'])
                    break
            
            if not response:
                response = "Sorry, I didn't understand that. Please try asking about our services, pricing, or contact information."
        
        return jsonify({
            'reply': response,
            'confidence': float(confidence),
            'tag': tag
        })
    
    except Exception as e:
        logging.error(f"Error processing chat: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'reply': 'Sorry, something went wrong. Please try again.'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logging.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
