import os
# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0=all, 1=info, 2=warning, 3=error
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN messages

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import json
import random
import logging
from datetime import datetime
import database

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

# Initialize database
database.init_db()

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
        
        # Log conversation to database
        conversation_id = database.log_conversation(
            user_message=msg,
            bot_response=response,
            intent_tag=tag,
            confidence=float(confidence),
            session_id=request.headers.get('User-Agent', 'unknown')[:100],
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'reply': response,
            'confidence': float(confidence),
            'tag': tag,
            'conversation_id': conversation_id
        })
    
    except Exception as e:
        logging.error(f"Error processing chat: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'reply': 'Sorry, something went wrong. Please try again.'
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """Handle user feedback on bot responses"""
    try:
        if not request.json or 'conversation_id' not in request.json or 'feedback_type' not in request.json:
            return jsonify({'error': 'Invalid request format'}), 400
        
        conversation_id = request.json['conversation_id']
        feedback_type = request.json['feedback_type']
        
        if feedback_type not in ['positive', 'negative']:
            return jsonify({'error': 'Invalid feedback type'}), 400
        
        database.add_feedback(conversation_id, feedback_type)
        logging.info(f"Feedback received: {feedback_type} for conversation {conversation_id}")
        
        return jsonify({'success': True, 'message': 'Feedback recorded'})
    
    except Exception as e:
        logging.error(f"Error processing feedback: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin/stats', methods=['GET'])
def admin_stats():
    """Get statistics for admin dashboard"""
    try:
        stats = database.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logging.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin/low-confidence', methods=['GET'])
def admin_low_confidence():
    """Get conversations with low confidence"""
    try:
        threshold = float(request.args.get('threshold', 0.7))
        limit = int(request.args.get('limit', 50))
        conversations = database.get_low_confidence_conversations(threshold, limit)
        return jsonify(conversations)
    except Exception as e:
        logging.error(f"Error getting low confidence conversations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin/negative-feedback', methods=['GET'])
def admin_negative_feedback():
    """Get conversations with negative feedback"""
    try:
        limit = int(request.args.get('limit', 50))
        conversations = database.get_negative_feedback_conversations(limit)
        return jsonify(conversations)
    except Exception as e:
        logging.error(f"Error getting negative feedback: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin/export', methods=['GET'])
def admin_export():
    """Export training data from positive feedback"""
    try:
        training_data = database.export_training_data()
        return jsonify(training_data)
    except Exception as e:
        logging.error(f"Error exporting training data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """Admin dashboard to review feedback and low confidence conversations"""
    return send_from_directory('static', 'admin.html')

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
