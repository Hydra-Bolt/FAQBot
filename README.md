# FAQBot - AI-Powered Telegram FAQ Bot

An intelligent FAQ bot designed for Telegram, specifically built for **vivirdeingresospasivos.online** - a platform dedicated to passive income strategies and investment education. The bot leverages advanced AI technologies to provide accurate, context-aware responses about investment strategies, trading services, and platform features.

## 🚀 Features

### Core Functionality
- **AI-Powered Responses**: Utilizes OpenAI's language models with vector embeddings for intelligent, context-aware answers
- **Semantic Search**: Pinecone vector database integration for finding the most relevant FAQ responses
- **Multi-language Support**: Handles both Spanish and English conversations
- **Chat History**: Maintains conversation context for better user experience
- **Telegram Integration**: Native Telegram bot with command support

### Admin Dashboard
- **Web-based Management**: Flask-powered admin interface for FAQ management
- **CRUD Operations**: Create, read, update, and delete FAQ entries
- **Bulk Export**: Download FAQ data as CSV files with UTF-8 support
- **Question Grouping**: Organize multiple questions under single answers
- **Secure Authentication**: Login system with username/password protection

### Investment Strategies Support
The bot provides information about various investment strategies including:
- **A10K Strategy**: Algorithmic Forex trading (minimum $2,000 USD)
- **A100K Strategy**: Conservative long-term strategy (minimum $10,000 USD)
- **VtMarkets Integration**: Broker services and promotions
- **Social Trading**: Community-based trading features

## 🛠 Technology Stack

- **Backend**: Python 3.10+, Flask
- **Database**: Supabase (PostgreSQL)
- **Vector Database**: Pinecone
- **AI/ML**: OpenAI API, LangChain
- **Messaging**: Telegram Bot API
- **Frontend**: HTML/CSS/JavaScript (Admin Dashboard)
- **Deployment**: Heroku-ready with runtime.txt

## 📋 Prerequisites

Before running this project, ensure you have:

- Python 3.10 or higher
- A Telegram Bot Token (from @BotFather)
- OpenAI API key
- Pinecone account and API key
- Supabase project with database setup
- Admin credentials for dashboard access

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hydra-Bolt/FAQBot.git
   cd FAQBot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Telegram Bot Configuration
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_admin_id
   
   # Admin Dashboard Credentials
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   SECRET_KEY=your_flask_secret_key
   
   # Database Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_api_key
   
   # AI Services
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   
   # Server Configuration
   PORT=5000
   ```

4. **Set up Supabase Database:**
   - Create tables for `Questions` and `Answers`
   - Set up proper relationships between questions and answers
   - Configure API access permissions

5. **Initialize Pinecone Index:**
   - Create an index named `faq-bot` in your Pinecone project
   - Ensure the index is configured for text embeddings

6. **Run the application:**
   ```bash
   python server.py
   ```

## 🌍 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | Yes |
| `ADMIN_ID` | Telegram user ID of the admin | Yes |
| `ADMIN_USERNAME` | Username for admin dashboard login | Yes |
| `ADMIN_PASSWORD` | Password for admin dashboard login | Yes |
| `SECRET_KEY` | Flask session secret key | Yes |
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase API key | Yes |
| `OPENAI_API_KEY` | OpenAI API key for language models | Yes |
| `PINECONE_API_KEY` | Pinecone API key for vector operations | Yes |
| `PORT` | Server port (default: 5000) | No |

## 📱 Usage

### For Users (Telegram)
1. Start a conversation with your bot on Telegram
2. Send `/start` to begin interaction
3. Ask questions about investment strategies, platform features, or services
4. The bot will provide AI-powered responses based on the FAQ database

### For Administrators (Web Dashboard)
1. Navigate to `http://your-domain/login`
2. Log in with your admin credentials
3. Access the dashboard to:
   - View all FAQ entries grouped by answers
   - Add new questions and answers
   - Edit existing content
   - Delete outdated information
   - Export data as CSV

### Telegram Commands
- `/start` - Initialize bot conversation
- Regular text messages - Get AI-powered FAQ responses

## 🏗 Project Structure

```
FAQBot/
├── server.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for Heroku
├── faq.json             # Sample FAQ data
├── .gitignore           # Git ignore rules
├── utils/               # Utility modules
│   ├── database.py      # Supabase database operations
│   ├── faq_embeddings.py # Pinecone vector operations
│   ├── gen_from_embed.py # AI response generation
│   └── telegram_utils.py # Telegram API utilities
└── templates/           # HTML templates
    ├── dashboard.html   # Admin dashboard
    └── login.html      # Login page
```

## 🔌 API Endpoints

### Public Endpoints
- `GET/POST /` - Telegram webhook endpoint
- `GET /login` - Admin login page
- `POST /login` - Admin authentication

### Protected Endpoints (require login)
- `GET /dashboard` - Admin dashboard
- `GET /logout` - Admin logout
- `GET /download` - Export FAQ data as CSV
- `POST /add` - Add new FAQ entry
- `POST /update` - Update existing FAQ entry
- `POST /delete` - Delete FAQ entry
- `POST /add_questions` - Add questions to existing answer

## 🚀 Deployment

### Heroku Deployment
1. Create a new Heroku app
2. Set environment variables in Heroku dashboard
3. Connect your GitHub repository
4. Deploy from the main branch

### Manual Deployment
1. Set up a VPS or cloud server
2. Install Python and dependencies
3. Configure environment variables
4. Set up a reverse proxy (nginx recommended)
5. Use a process manager like PM2 or systemd

## ⚠️ Financial Disclaimer

**IMPORTANT**: This bot provides information about investment strategies and financial services. Please note:

- All investment strategies carry inherent risks
- Past performance does not guarantee future results
- The information provided is for educational purposes only
- This is not personalized financial advice
- Always consult with qualified financial professionals before making investment decisions
- The platform operators are not responsible for investment losses
- Performance fees and terms may apply to specific strategies

## 📊 Supported Investment Strategies

### A10K Strategy
- **Type**: Algorithmic Forex trading
- **Minimum Deposit**: $2,000 USD
- **Expected Monthly Benefit**: $130-200 USD
- **Risk Level**: 14% DD (Drawdown)

### A100K Strategy
- **Type**: Conservative long-term compound interest
- **Minimum Deposit**: $10,000 USD
- **Access**: Requires qualification meeting
- **Contact**: @marcbarranco for access

### VtMarkets Active Trader
- **Requirement**: $5,000+ account balance
- **Benefit**: 13% annual promotion
- **Registration**: https://myaccount.vtmarkets.com/fundsGrowthPromotion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📄 License

This project is proprietary and confidential. Unauthorized copying, distribution, or modification is prohibited.

## 🆘 Support

For technical support or questions:
- Create an issue in this repository
- Contact the development team
- Check the FAQ database for common questions

---

**Made with ❤️ for the vivirdeingresospasivos.online community**