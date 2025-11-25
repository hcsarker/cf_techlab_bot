# Feedback System - User Guide

## 🎯 Overview

Your chatbot now has a **feedback loop system** that learns from user interactions! Users can rate responses, and admins can review feedback to improve the model.

## ✨ Features Implemented

### 1. **Automatic Conversation Logging** 📝

- Every chat message is saved to SQLite database
- Stores: user message, bot response, confidence score, timestamp, IP, session info

### 2. **User Feedback Buttons** 👍👎

- Each bot response has "Helpful" and "Not Helpful" buttons
- Users can rate responses in real-time
- Feedback is recorded instantly to database

### 3. **Admin Dashboard** 🎛️

- Access: `http://127.0.0.1:5000/admin`
- Real-time statistics:
  - Total conversations
  - Average confidence score
  - Positive/negative feedback counts
  - Low confidence conversation count
  - Feedback rate percentage

### 4. **Admin Features**

- **Low Confidence Tab**: Review conversations where bot was uncertain
- **Negative Feedback Tab**: See responses users disliked
- **Export Training Data**: Download new patterns from positive feedback
- **Auto-refresh**: Updates every 30 seconds

## 🚀 How to Use

### For Users (Chat Interface)

1. Open: `http://127.0.0.1:5000/`
2. Chat with the bot
3. Click 👍 "Helpful" or 👎 "Not Helpful" on any response
4. Feedback is saved instantly

### For Admins (Dashboard)

1. Open: `http://127.0.0.1:5000/admin`
2. View real-time statistics
3. Switch between tabs:
   - **Low Confidence**: See uncertain bot responses
   - **Negative Feedback**: Review user complaints
4. Click "📥 Export Training Data" to download new patterns

## 🔄 Retraining Workflow

### Step 1: Collect Feedback

- Let users chat and provide feedback
- Monitor admin dashboard for patterns

### Step 2: Review & Export

```bash
# Access admin dashboard
http://127.0.0.1:5000/admin

# Click "Export Training Data" button
# File downloaded: training_data_YYYY-MM-DD.json
```

### Step 3: Merge with data.json

```python
# Example: Manually add new patterns to data.json
# Review exported data and add good patterns to appropriate intents
```

### Step 4: Retrain Model

```bash
cd /home/hridoy/Documents/Project/cf_techlab_bot
source /home/hridoy/venv/bin/activate
python train.py
```

### Step 5: Restart Server

```bash
pkill -f "python.*app.py"
python app.py &
```

## 📊 Database Schema

### `conversations` table:

- `id`: Primary key
- `user_message`: What user asked
- `bot_response`: Bot's reply
- `intent_tag`: Predicted intent
- `confidence`: Model confidence (0-1)
- `timestamp`: When conversation happened
- `session_id`: User's session
- `ip_address`: User's IP

### `feedback` table:

- `id`: Primary key
- `conversation_id`: Links to conversation
- `feedback_type`: 'positive' or 'negative'
- `timestamp`: When feedback given

## 🔧 API Endpoints

### `/chat` (POST)

```json
// Request
{"message": "hello"}

// Response
{
  "reply": "Hello friend!",
  "confidence": 0.9998,
  "tag": "greeting",
  "conversation_id": 1
}
```

### `/feedback` (POST)

```json
// Request
{
  "conversation_id": 1,
  "feedback_type": "positive"
}

// Response
{"success": true, "message": "Feedback recorded"}
```

### `/admin/stats` (GET)

```json
{
  "total_conversations": 4,
  "average_confidence": 0.9986,
  "positive_feedback": 1,
  "negative_feedback": 1,
  "low_confidence_count": 0,
  "feedback_rate": 50.0
}
```

### `/admin/low-confidence` (GET)

Returns conversations with confidence < 0.7

### `/admin/negative-feedback` (GET)

Returns conversations with negative feedback

### `/admin/export` (GET)

Returns training data from positive feedback/high confidence conversations

## 💡 Tips

### For Better Results:

1. **Encourage Feedback**: Ask users to rate responses
2. **Review Weekly**: Check admin dashboard regularly
3. **Focus on Negatives**: Prioritize fixing negative feedback
4. **Low Confidence**: Add patterns for uncertain queries
5. **Retrain Monthly**: Update model with new patterns

### Monitoring Low Confidence:

- If confidence < 70%, chatbot returns default response
- Review these in admin dashboard
- Add missing patterns to `data.json`

### Data Quality:

- Export only includes:
  - High confidence (>80%) conversations
  - Positive feedback conversations
- Manual review recommended before adding to training

## 🎨 UI Features

### Chat Interface:

- Modern gradient design
- Dark mode toggle (saved in localStorage)
- Typing indicators
- Message timestamps
- Smooth animations
- Responsive design

### Admin Dashboard:

- Real-time statistics cards
- Color-coded confidence badges
- Tabbed interface
- Auto-refresh
- Export functionality
- Beautiful scrolling lists

## 📈 Success Metrics

Current Performance:

- ✅ 864 total training patterns
- ✅ 99.54% training accuracy
- ✅ 14 intent categories
- ✅ Multilingual support (English/Bangla/Banglish)
- ✅ Feedback system active
- ✅ Admin dashboard operational

## 🔐 Security Notes

⚠️ **Important**:

- Admin dashboard has NO authentication currently
- For production, add password protection:

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@app.route('/admin')
@auth.login_required
def admin_dashboard():
    # protected route
```

## 📞 Support

Issues? Check:

1. Database exists: `chatbot_feedback.db`
2. Server running: `curl http://127.0.0.1:5000/health`
3. Logs: `tail -f chatbot.log`
4. Server logs: `tail -f server.log`

---

**🎉 Congratulations!** Your chatbot can now learn from user feedback! Monitor the admin dashboard and retrain regularly for continuous improvement.
