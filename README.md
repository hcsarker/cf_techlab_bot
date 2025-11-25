# CF TechLab AI Assistant 🤖

A modern, AI-powered chatbot built with Flask and TensorFlow for CF TechLab. Features a beautiful responsive UI with dark mode, multilingual support (English & Bangla), and intelligent intent recognition.

## 🌟 Features

- **Smart AI Chatbot**: TensorFlow/Keras-based intent classification with 99.5%+ accuracy
- **860+ Training Patterns**: Comprehensive multilingual dataset covering all business queries
- **Modern UI**: Responsive chat interface with message bubbles, timestamps, and smooth animations
- **Dark Mode**: Toggle between light and dark themes with preference persistence
- **Multilingual**: Supports both English and Bangla (Banglish) queries
- **User Feedback System** 👍👎: Rate responses to improve the bot
- **Admin Dashboard** 🎛️: Monitor performance, review feedback, and export training data
- **Conversation Logging**: SQLite database tracking all interactions
- **Auto-learning Ready**: Export new patterns from user feedback for continuous improvement
- **Real-time Typing Indicator**: Shows when the bot is "thinking"
- **Confidence Threshold**: Falls back to helpful suggestions for unclear queries
- **CORS Enabled**: Can be integrated with external applications
- **Health Check Endpoint**: Monitor server status
- **Comprehensive Logging**: Track all interactions for analytics
- **Mobile Responsive**: Works perfectly on all device sizes

## 📋 Prerequisites

- Python 3.10, 3.11, or 3.12 (TensorFlow not yet available for 3.13)
- pip package manager
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/hcsarker/cf_techlab_bot.git
cd cf_techlab_bot
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Train the Model (Optional)

The repository includes a pre-trained model. To retrain:

```bash
python train.py
```

This will create:

- `chatbot_model.h5` - Trained model
- `tokenizer.pkl` - Tokenizer and encoder

### 5. Run the Application

```bash
python app.py
```

The server will start at: **http://127.0.0.1:5000/**

## 📡 API Endpoints

### Home

- **GET** `/` - Serves the chat interface

### Health Check

- **GET** `/health`
- Returns server status and timestamp

```bash
curl http://127.0.0.1:5000/health
```

### Chat

- **POST** `/chat`
- Send messages and get AI responses

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

**Response:**

```json
{
  "reply": "Assalamualaikum! How may I help you?",
  "confidence": 0.9968,
  "tag": "greeting",
  "conversation_id": 1
}
```

### Feedback System

**Submit User Feedback**

- **POST** `/feedback`

```bash
curl -X POST http://127.0.0.1:5000/feedback \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 1, "feedback_type": "positive"}'
```

**Admin Dashboard**

- **GET** `/admin` - Visual dashboard with statistics
- **GET** `/admin/stats` - Get performance metrics
- **GET** `/admin/low-confidence` - Review uncertain responses
- **GET** `/admin/negative-feedback` - See user complaints
- **GET** `/admin/export` - Export training data

```bash
# Access dashboard
http://127.0.0.1:5000/admin

# Get statistics via API
curl http://127.0.0.1:5000/admin/stats
```

📖 **Full Documentation**: See [FEEDBACK_SYSTEM.md](FEEDBACK_SYSTEM.md) for detailed guide on using the feedback system, admin dashboard, and retraining workflow.

## 🌐 Embed Chatbot in Your Website

The chatbot can be easily embedded in any website!

### Quick Embed (Iframe):

```html
<iframe
  src="http://127.0.0.1:5000/widget"
  style="position: fixed; bottom: 0; right: 0; width: 100%; height: 100%; border: none; z-index: 999999; pointer-events: none;"
>
</iframe>
```

### Features:

- ✅ **User Information Collection** - Collects name, mobile, email before chat
- ✅ **Session Tracking** - Links all conversations to user
- ✅ **Database Storage** - Saves user info in `user_info` table
- ✅ **Minimizable Widget** - Professional floating chat button
- ✅ **Mobile Responsive** - Works on all devices

### Widget Demo:

- Test widget: http://127.0.0.1:5000/widget
- Embed demo: `embed_demo.html`

📖 **Complete Guide**: See [EMBED_GUIDE.md](EMBED_GUIDE.md) for detailed embedding instructions, customization options, and production deployment.

## 🎨 Chatbot Capabilities

The bot understands queries about:

- 👋 **Greetings** - hello, hi, assalamualaikum
- 💼 **Services** - software development, web apps, mobile apps
- 💰 **Pricing** - cost estimates, quotations
- 📞 **Contact** - phone, email, address
- 🕐 **Office Hours** - availability, working hours
- 📍 **Location** - office address
- 👥 **Team** - about the company
- 💻 **Technologies** - tech stack, programming languages
- 💳 **Payment** - payment methods (Bkash, Nagad, etc.)
- 🎯 **Portfolio** - previous projects, case studies
- ⭐ **Testimonials** - client reviews
- ⏰ **Timeline** - project duration estimates
- 🛠️ **Support** - maintenance, bug fixes
- ✨ **Custom Projects** - custom solution inquiries

## 🌐 Deployment to https://cftechlab.hcsarker.me/

### Option 1: Using Gunicorn (Recommended)

1. Install Gunicorn:

```bash
pip install gunicorn
```

2. Create a systemd service file `/etc/systemd/system/cfbot.service`:

```ini
[Unit]
Description=CF TechLab Chatbot
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/cf_techlab_bot
Environment="PATH=/path/to/cf_techlab_bot/venv/bin"
ExecStart=/path/to/cf_techlab_bot/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

3. Start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start cfbot
sudo systemctl enable cfbot
```

### Option 2: Using Nginx as Reverse Proxy

1. Configure Nginx `/etc/nginx/sites-available/cftechlab`:

```nginx
server {
    listen 80;
    server_name cftechlab.hcsarker.me;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/cftechlab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d cftechlab.hcsarker.me
```

### Option 4: Docker Deployment

1. Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
```

2. Build and run:

```bash
docker build -t cf-techlab-bot .
docker run -d -p 5000:5000 --name cfbot cf-techlab-bot
```

## 🗂️ Project Structure

```
cf_techlab_bot/
├── app.py                 # Flask application with API endpoints
├── train.py               # Model training script
├── data.json              # Intent data (patterns & responses)
├── chatbot_model.h5       # Trained TensorFlow model
├── tokenizer.pkl          # Tokenizer and label encoder
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── chatbot.log            # Application logs (generated)
└── static/
    └── index.html         # Chat UI (responsive, dark mode)
```

## 🛠️ Development

### Adding New Intents

1. Edit `data.json`:

```json
{
  "tag": "new_intent",
  "patterns": ["pattern 1", "pattern 2"],
  "responses": ["response 1", "response 2"]
}
```

2. Retrain the model:

```bash
python train.py
```

3. Restart the server

### Modifying the UI

Edit `static/index.html` to customize:

- Colors and themes
- Layout and styling
- Chat bubble design
- Animations

## 📊 Logs

Application logs are saved to `chatbot.log`:

- Incoming messages
- Predicted intents and confidence scores
- Errors and warnings

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

- **Live Site**: https://cftechlab.hcsarker.me/
- **Repository**: https://github.com/hcsarker/cf_techlab_bot

## 💬 Support

For issues or questions:

- 📧 Email: support@cftechlab.com
- 📞 Phone: +8801XXXXXXXXX
- 🌐 Website: https://cftechlab.hcsarker.me/

---

Made with ❤️ by CF TechLab
