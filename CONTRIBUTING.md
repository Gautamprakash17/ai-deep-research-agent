# Contributing to AI Deep Research Agent

Thank you for your interest in contributing to the AI Deep Research Agent! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Reports**: Report issues you encounter
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve README, add examples, or fix typos
- 🔧 **Code Contributions**: Submit pull requests with code improvements
- 🧪 **Testing**: Help test the application and report findings

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Streamlit and AI/ML concepts

### Setup Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-deep-research-agent.git
   cd ai-deep-research-agent
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

4. **Run the application**
   ```bash
   streamlit run deep_research_openai.py
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add new research template for technical analysis
fix: resolve API connection timeout issue
docs: update README with new features
test: add unit tests for research agent
```

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Add tests if applicable
   - Update documentation if needed

3. **Test your changes**
   - Run the application locally
   - Test with different API providers
   - Verify all features work correctly

4. **Submit a pull request**
   - Provide a clear description of changes
   - Include screenshots for UI changes
   - Reference any related issues

## 🐛 Reporting Issues

When reporting bugs, please include:

- **Description**: Clear explanation of the issue
- **Steps to Reproduce**: Detailed steps to recreate the problem
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable

## 💡 Feature Requests

When suggesting features:

- **Description**: Clear explanation of the feature
- **Use Case**: Why this feature would be useful
- **Implementation Ideas**: Any thoughts on how to implement
- **Priority**: High/Medium/Low priority

## 🔧 Development Areas

### High Priority
- [ ] Add more AI providers (Anthropic, Cohere, etc.)
- [ ] Implement research result caching
- [ ] Add support for custom research templates
- [ ] Improve error handling and user feedback

### Medium Priority
- [ ] Add research result comparison tools
- [ ] Implement batch research processing
- [ ] Add research quality scoring
- [ ] Create research result visualization

### Low Priority
- [ ] Add research scheduling
- [ ] Implement research result sharing
- [ ] Add research collaboration features
- [ ] Create mobile-responsive design

## 🧪 Testing

### Manual Testing
- Test with different research topics
- Verify all export formats work
- Test error handling scenarios
- Check UI responsiveness

### Automated Testing
- Add unit tests for core functions
- Add integration tests for API calls
- Add UI tests for Streamlit components

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions
- Include type hints where appropriate
- Document complex algorithms
- Add inline comments for tricky logic

### User Documentation
- Keep README up to date
- Add usage examples
- Document new features
- Provide troubleshooting guides

## 🏷️ Labels

We use the following labels for issues and PRs:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

If you need help:

1. **Check existing issues** for similar problems
2. **Search the documentation** for answers
3. **Create a new issue** with the `question` label
4. **Join discussions** in existing issues

## 🎉 Recognition

Contributors will be recognized in:

- The project README
- Release notes
- GitHub contributors page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the AI Deep Research Agent! 🚀

Your contributions help make this tool better for everyone in the AI research community. 