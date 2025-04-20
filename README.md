# Selenium Web Testing Project

## 📋 Overview
This project is a comprehensive web testing suite built with Selenium WebDriver and Python, designed to automate testing of web applications. The project follows the Page Object Model (POM) design pattern and implements best practices for automated testing.

## 🎯 Objectives
- Implement automated testing for web applications using Selenium WebDriver
- Create a robust and maintainable testing framework
- Ensure comprehensive test coverage for critical user flows
- Demonstrate best practices in test automation
- Provide a scalable testing solution that can be extended for future needs

## 🛠️ Technologies Used
- **Python** - Programming language
- **Selenium WebDriver** - Web automation framework
- **Pytest** - Testing framework
- **Page Object Model (POM)** - Design pattern for test automation

## 📦 Project Structure
```
├── tests/                  # Test files
│   ├── test_login_page.py
│   ├── test_products_page.py
│   ├── test_cart_page.py
│   └── test_checkout_pages.py
├── page_objects/           # Page object classes
├── locators/              # Element locators
├── utilities/             # Helper functions and utilities
├── drivers/               # WebDriver executables
└── requirements.txt       # Project dependencies
```

## 🚀 Features
- Automated testing of login functionality
- Product page testing
- Shopping cart operations
- Checkout process validation
- Comprehensive error handling
- Cross-browser testing support

## ⚙️ Prerequisites
- Python 3.x
- pip (Python package manager)
- Web browser (Chrome, Firefox, etc.)
- WebDriver executables

## 🔧 Installation
1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🧪 Running Tests
To run all tests:
```bash
pytest
```

To run specific test files:
```bash
pytest tests/test_login_page.py
```
To run specific test from a specific files:
```bash
pytest tests/test_login_page.py::test_specific
```

## 📝 Test Coverage
The project includes tests for:
- Login functionality with various scenarios
- Product page interactions
- Shopping cart operations
- Checkout process
- Error handling and validation

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
- [Andres Valencia]

## 🙏 Acknowledgments
- Selenium WebDriver team
- Pytest community
- All contributors to this project
