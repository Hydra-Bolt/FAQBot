# Contributing to FAQBot

Thank you for your interest in contributing to FAQBot! This document provides guidelines and information for contributors.

## 🚀 Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment following the README instructions
4. Create a new branch for your feature or bug fix

## 🔧 Development Setup

### Prerequisites
- Python 3.10.16+
- Git
- A text editor or IDE

### Installation
1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/FAQBot.git
   cd FAQBot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and configuration
   ```

## 📝 Code Style Guidelines

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Example:
```python
def get_faq_response(question: str, chat_id: int) -> str:
    """
    Generate a response for the given question.
    
    Args:
        question: The user's question
        chat_id: Telegram chat ID for context
        
    Returns:
        Generated response string
    """
    # Implementation here
    pass
```

## 🧪 Testing

Currently, the project doesn't have automated tests. Contributing test coverage would be greatly appreciated!

### Manual Testing
1. Test the Telegram bot functionality
2. Verify the web dashboard works correctly
3. Test API endpoints
4. Check environment variable handling

### Testing Checklist
- [ ] Bot responds to messages correctly
- [ ] Admin dashboard loads and functions
- [ ] FAQ CRUD operations work
- [ ] CSV export functions properly
- [ ] Authentication system works
- [ ] Error handling is appropriate

## 📋 Issue Guidelines

### Reporting Bugs
- Use the GitHub issue tracker
- Include Python version, OS, and dependency versions
- Provide steps to reproduce the issue
- Include relevant error messages and logs

### Requesting Features
- Check existing issues first
- Clearly describe the feature and its benefits
- Provide examples of how it would be used

## 🔄 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Follow the code style guidelines
   - Test your changes thoroughly

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a pull request**:
   - Use a clear, descriptive title
   - Describe what your changes do
   - Reference any related issues
   - Include testing information

### Pull Request Checklist
- [ ] Code follows the style guidelines
- [ ] Changes are tested and working
- [ ] Documentation is updated if needed
- [ ] No sensitive information is committed
- [ ] Branch is up to date with main

## 🚀 Deployment Testing

Before submitting, test your changes in a deployment-like environment:

1. Set all required environment variables
2. Test with actual API keys (use test/development keys)
3. Verify the application starts without errors
4. Test core functionality end-to-end

## 📚 Areas for Contribution

We welcome contributions in these areas:

### High Priority
- [ ] Unit and integration tests
- [ ] Error handling improvements
- [ ] Performance optimizations
- [ ] Documentation improvements

### Medium Priority
- [ ] Multi-language support
- [ ] Rate limiting implementation
- [ ] Analytics and monitoring
- [ ] Database migrations
- [ ] Docker containerization

### Low Priority
- [ ] UI/UX improvements for dashboard
- [ ] Additional export formats
- [ ] Backup and restore functionality
- [ ] Advanced admin features

## 🔒 Security Guidelines

- Never commit API keys, tokens, or sensitive data
- Use environment variables for all configuration
- Validate and sanitize user inputs
- Follow secure coding practices
- Report security issues privately via email

## 📞 Getting Help

- Check the README.md for setup instructions
- Search existing GitHub issues
- Create a new issue for bugs or questions
- Join discussions in existing pull requests

## 📄 License

By contributing to FAQBot, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in the project documentation and release notes. Thank you for helping make FAQBot better!