# Contributing to CF TechLab Bot

Thank you for your interest in contributing to the CF TechLab Bot project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with a clear title and description
3. Include steps to reproduce the problem (for bugs)
4. Add relevant labels and screenshots if applicable

### Contributing Code

1. **Fork the Repository**

   - Fork the project to your GitHub account
   - Clone your fork locally:
     ```bash
     git clone https://github.com/your-username/cf_techlab_bot.git
     cd cf_techlab_bot
     ```

2. **Set Up Development Environment**

   - Create a virtual environment:
     ```bash
     python3.11 -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Create a Branch**

   - Create a new branch for your feature or fix:
     ```bash
     git checkout -b feature/your-feature-name
     ```

4. **Make Your Changes**

   - Write clean, readable code
   - Follow Python PEP 8 style guidelines
   - Add comments where necessary
   - Update documentation if needed

5. **Test Your Changes**

   - Run the training script if you modified model code:
     ```bash
     python train.py
     ```
   - Test the Flask application:
     ```bash
     python app.py
     ```
   - Test the chat endpoint manually or with curl

6. **Commit Your Changes**

   - Write clear, descriptive commit messages:
     ```bash
     git add .
     git commit -m "Add: Brief description of your changes"
     ```

7. **Push and Create Pull Request**
   - Push to your fork:
     ```bash
     git push origin feature/your-feature-name
     ```
   - Open a Pull Request on the main repository
   - Describe your changes clearly in the PR description
   - Link any related issues

### Code Style Guidelines

- Use meaningful variable and function names
- Keep functions small and focused on a single task
- Add docstrings to functions and classes
- Follow PEP 8 for Python code formatting
- Keep lines under 100 characters when possible

### Adding New Intents

To add new chatbot intents:

1. Edit `data.json` and add your intent:

   ```json
   {
     "tag": "new_intent",
     "patterns": ["example question 1", "example question 2"],
     "responses": ["response 1", "response 2"]
   }
   ```

2. Retrain the model:

   ```bash
   python train.py
   ```

3. Test the new intent through the chat interface

### Improving the UI

If you want to enhance the frontend:

1. Edit `static/index.html`
2. Test the changes by running the Flask server
3. Ensure the UI is responsive and accessible
4. Consider cross-browser compatibility

## Development Guidelines

### Project Structure

```
cf_techlab_bot/
├── app.py              # Flask application
├── train.py            # Model training script
├── data.json           # Intent data
├── chatbot_model.h5    # Trained model (generated)
├── tokenizer.pkl       # Tokenizer data (generated)
└── static/
    └── index.html      # Web interface
```

### Testing Checklist

Before submitting a PR, ensure:

- [ ] Code runs without errors
- [ ] New features are tested manually
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] Code follows project style guidelines

## Getting Help

If you have questions or need help:

- Open an issue with the "question" label
- Reach out to the maintainers
- Check existing documentation and issues

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Help create a welcoming environment for all contributors

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CF TechLab Bot! 🚀
