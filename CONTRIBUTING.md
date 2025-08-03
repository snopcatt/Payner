# Contributing to Payner Toolkit

Thank you for your interest in contributing to the Payner Toolkit! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- **Be respectful and inclusive** to all contributors regardless of background
- **Focus on constructive feedback** when reviewing code or discussing features
- **Maintain professional communication** in all interactions
- **Respect the ethical use** of security tools - only for authorized testing

## Ways to Contribute

### 🐛 Bug Reports

If you find a bug, please create an issue with:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Error messages or logs** if applicable

### 💡 Feature Requests

For new features or enhancements:

- **Describe the feature** and its benefits
- **Explain the use case** and why it's needed
- **Consider backwards compatibility**
- **Discuss potential implementation** approaches

### 🔧 Code Contributions

We welcome code contributions! Please follow these guidelines:

#### Before You Start

1. **Check existing issues** to avoid duplicate work
2. **Create an issue** to discuss major changes
3. **Fork the repository** and create a feature branch
4. **Follow coding standards** outlined below

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/payner-toolkit.git
cd payner-toolkit

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest bandit
```

#### Coding Standards

**Python Code:**
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Include **docstrings** for functions and classes
- Keep functions **focused and small**
- Use **meaningful variable names**

**Shell Scripts:**
- Use **shellcheck** for validation
- Include **error handling**
- Use **proper quoting** for variables
- Add **comments** for complex logic

**Documentation:**
- Update **README.md** if needed
- Add **docstrings** to new functions
- Update **CHANGELOG.md** for notable changes
- Include **usage examples** where helpful

#### Testing

Before submitting:

```bash
# Run syntax checks
python -m py_compile tools/*.py
bash -n *.sh

# Run security scan
bandit -r tools/

# Test functionality
./payner.sh  # Basic functionality test
```

#### Commit Guidelines

Use clear, descriptive commit messages:

```
feat: add SSL certificate validation to Thor tool
fix: resolve packet collector interface selection bug
docs: update installation guide for CentOS
style: format code according to PEP 8
refactor: improve error handling in network scanner
test: add unit tests for Batman load testing
```

#### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Test thoroughly** on different systems if possible
4. **Update documentation** as needed
5. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if UI changes
   - Testing information

### 📚 Documentation

Help improve documentation by:

- **Fixing typos or unclear sections**
- **Adding examples and use cases**
- **Translating content** (if multilingual support is added)
- **Creating video tutorials** or guides

### 🧪 Testing

Contribute to testing by:

- **Testing on different Linux distributions**
- **Reporting compatibility issues**
- **Creating test cases**
- **Improving automated testing**

## Development Workflow

### Branching Strategy

- **`main`** - Stable release branch
- **`develop`** - Integration branch for new features
- **`feature/feature-name`** - Feature development branches
- **`hotfix/issue-description`** - Critical bug fixes

### Release Process

1. Features merged to `develop`
2. Testing and integration on `develop`
3. Release candidate created
4. Final testing and documentation
5. Merge to `main` and tag release

## Security Considerations

When contributing to security tools:

- **Never include real credentials** in code or examples
- **Use placeholder data** in documentation
- **Consider ethical implications** of new features
- **Add appropriate warnings** for dangerous operations
- **Follow responsible disclosure** for security issues

## Tool-Specific Guidelines

### Batman (Load Testing)
- Consider server impact and rate limiting
- Add safeguards against accidental DoS
- Validate URL formats and protocols

### Network Scanners (O'Azis, MILKO)
- Implement proper error handling for network timeouts
- Add stealth mode options where appropriate
- Consider IPv6 support for new features

### Packet Collector
- Ensure proper handling of network interfaces
- Add filtering options for specific protocols
- Consider privacy implications of packet capture

## Getting Help

If you need help:

- **Read the documentation** in the `/docs` folder
- **Check existing issues** for similar problems
- **Create a discussion** for questions
- **Join community channels** (if available)

## Recognition

Contributors will be recognized in:

- **CHANGELOG.md** for notable contributions
- **README.md** acknowledgments section
- **Release notes** for major contributions

## Legal Notes

By contributing, you agree that:

- Your contributions will be licensed under the same MIT License
- You have the right to submit the work
- Your contributions are your original creation
- You understand the ethical use requirements

## Questions?

Feel free to reach out by:

- **Creating an issue** for discussion
- **Contacting maintainers** directly
- **Participating in community discussions**

Thank you for helping make Payner Toolkit better! 🎵
