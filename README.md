# FAQBot

A sophisticated AI-powered Telegram bot for answering frequently asked questions with intelligent matching and response generation. The bot uses vector embeddings to find the most relevant FAQ entries and can generate contextual responses using OpenAI's language models.

## 🚀 Features

- **AI-Powered Responses**: Uses OpenAI GPT models for intelligent question answering
- **Vector Similarity Search**: Leverages Pinecone for accurate FAQ matching using embeddings
- **Telegram Integration**: Fully functional Telegram bot with message handling
- **Web Dashboard**: Flask-based admin panel for managing FAQs
- **Database Integration**: Supabase backend for storing questions and answers
- **Admin Authentication**: Secure login system for FAQ management
- **Multi-language Support**: Supports Spanish language interactions
- **Chat History**: Maintains conversation context for better responses
- **CSV Export**: Download FAQ data in CSV format
- **Real-time Updates**: Live FAQ management with instant updates

## 📋 Prerequisites

- Python 3.10.16 or higher
- Telegram Bot Token (from [@BotFather](https://core.telegram.org/bots#botfather))
- OpenAI API Key
- Pinecone Account and API Key
- Supabase Account and API credentials

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hydra-Bolt/FAQBot.git
   cd FAQBot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Telegram Bot Configuration
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_user_id
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # Pinecone Configuration
   PINECONE_API_KEY=your_pinecone_api_key
   
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   
   # Flask Configuration
   SECRET_KEY=your_flask_secret_key
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   PORT=5000
   ```

## ⚙️ Configuration

### Setting up Telegram Bot

1. Message [@BotFather](https://core.telegram.org/bots#botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token to your `.env` file
4. Get your Telegram user ID by messaging [@userinfobot](https://t.me/userinfobot)

### Setting up Pinecone

1. Create an account at [Pinecone](https://pinecone.io)
2. Create a new index named `faq-bot`
3. Use the following settings:
   - Dimensions: 1536 (for OpenAI embeddings)
   - Metric: cosine
4. Copy your API key to the `.env` file

### Setting up Supabase

1. Create a project at [Supabase](https://supabase.com)
2. Create the following tables:
   
   **Questions table:**
   ```sql
   CREATE TABLE Questions (
     id SERIAL PRIMARY KEY,
     question TEXT NOT NULL,
     answer_id INTEGER REFERENCES Answers(id)
   );
   ```
   
   **Answers table:**
   ```sql
   CREATE TABLE Answers (
     id SERIAL PRIMARY KEY,
     answer TEXT NOT NULL
   );
   ```

3. Copy your project URL and anon key to the `.env` file

## 🚦 Usage

### Starting the Application

1. **Run the Flask server**
   ```bash
   python server.py
   ```

2. **Set up webhook for Telegram bot**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-domain.com/"}'
   ```

### Using the Telegram Bot

1. Start a conversation with your bot on Telegram
2. Send `/start` to initialize the bot
3. Ask any question related to your FAQ content
4. The bot will respond with relevant answers or generate responses based on available information

### Using the Web Dashboard

1. Navigate to `http://localhost:5000/login`
2. Login with your admin credentials
3. Manage FAQs from the dashboard:
   - View all FAQ entries
   - Add new questions and answers
   - Edit existing entries
   - Delete outdated information
   - Export data as CSV

## 🔌 API Endpoints

### Bot Webhook
- **POST** `/` - Receives Telegram webhook messages

### Authentication
- **GET/POST** `/login` - Admin login page
- **GET** `/logout` - Logout endpoint

### Dashboard
- **GET** `/dashboard` - FAQ management interface

### FAQ Management
- **POST** `/add` - Add new FAQ entry
- **POST** `/update` - Update existing FAQ
- **POST** `/delete` - Delete FAQ entry
- **POST** `/add_questions` - Add questions to existing answer

### Data Export
- **GET** `/download` - Export FAQ data as CSV

## 📁 Project Structure

```
FAQBot/
├── server.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── faq.json             # Sample FAQ data
├── .env                 # Environment variables (create this)
├── .gitignore           # Git ignore rules
├── utils/               # Utility modules
│   ├── database.py      # Supabase database operations
│   ├── faq_embeddings.py # Pinecone vector operations
│   ├── gen_from_embed.py # AI response generation
│   └── telegram_utils.py # Telegram bot utilities
└── templates/           # HTML templates
    ├── dashboard.html   # Admin dashboard
    └── login.html      # Login page
```

## 🔧 Development Setup

### Adding New FAQs

1. **Via Web Dashboard**: Use the admin interface to add questions and answers
2. **Via API**: Send POST requests to `/add` endpoint
3. **Programmatically**: Use the database utility functions

### Customizing Responses

Modify the response generation logic in `utils/gen_from_embed.py`:
- Adjust the similarity threshold in `server.py` (currently 0.93)
- Customize the prompt templates
- Modify the chat history length (currently 10 messages)

### Adding New Languages

1. Update the welcome message in `server.py`
2. Modify response templates in `utils/gen_from_embed.py`
3. Update the dashboard templates if needed

## 🧪 Testing

To test the bot functionality:

1. **Test Telegram Integration**:
   ```bash
   # Send a test message to your bot
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
        -H "Content-Type: application/json" \
        -d '{"chat_id": "<YOUR_CHAT_ID>", "text": "Test message"}'
   ```

2. **Test Web Dashboard**:
   - Navigate to the login page
   - Verify authentication works
   - Test FAQ CRUD operations

3. **Test API Endpoints**:
   ```bash
   # Test health check
   curl http://localhost:5000/
   ```

## 🚀 Deployment

### Heroku Deployment

1. **Install Heroku CLI** and login
2. **Create a new Heroku app**:
   ```bash
   heroku create your-faq-bot
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set OPENAI_API_KEY=your_openai_key
   # ... set all other environment variables
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Set webhook**:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://your-faq-bot.herokuapp.com/"}'
   ```

### Railway/Render Deployment

Follow similar steps but use the respective platform's deployment guides and environment variable configuration methods.

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes and commit**:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 coding standards
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly
- Ensure environment variables are properly documented

### Areas for Contribution

- [ ] Add unit tests
- [ ] Implement rate limiting
- [ ] Add support for file uploads in FAQs
- [ ] Implement multi-language support
- [ ] Add analytics and usage statistics
- [ ] Improve error handling and logging
- [ ] Add Docker containerization
- [ ] Implement backup and restore functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions, suggestions, or support:

- **Project Repository**: [https://github.com/Hydra-Bolt/FAQBot](https://github.com/Hydra-Bolt/FAQBot)
- **Issues**: [GitHub Issues](https://github.com/Hydra-Bolt/FAQBot/issues)
- **Telegram**: Contact the bot admin for technical support

## 🙏 Acknowledgments

- [OpenAI](https://openai.com) for providing the language models
- [Pinecone](https://pinecone.io) for vector search capabilities
- [Supabase](https://supabase.com) for the database infrastructure
- [LangChain](https://langchain.com) for the AI framework
- [Flask](https://flask.palletsprojects.com) for the web framework
- [Telegram Bot API](https://core.telegram.org/bots/api) for bot integration

---

⭐ **Star this repository if you found it helpful!**