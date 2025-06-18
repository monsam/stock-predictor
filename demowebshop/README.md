# Cursor AI Demo Web Shop Test Framework

This is a BDD (Behavior Driven Development) test framework for the Demo Web Shop using Python, Selenium, and Pytest-BDD.

## Project Structure

```
├── features/                 # BDD feature files
│   └── demo_shop.feature    # Test scenarios
├── pages/                   # Page Object Models
│   ├── base_page.py        # Base page class
│   ├── register_page.py    # Registration page
│   ├── product_page.py     # Product page
│   └── search_page.py      # Search page
├── steps/                   # Step definitions
│   └── test_demo_shop.py   # Test implementation
├── reports/                 # Test reports
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Git

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/cursor_ai_demo-web-shop-tests.git
cd cursor_ai_demo-web-shop-tests
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

## Running Tests

To run all tests:
```bash
python -m pytest -v --html=reports/report.html
```

To run specific test:
```bash
python -m pytest -v -k "test_name" --html=reports/report.html
```

## Test Scenarios

1. User Registration with Edge Validation
   - Tests email format validation
   - Tests password mismatch validation

2. Out of Stock Item Handling
   - Tests adding out-of-stock items to cart
   - Verifies appropriate error messages

3. Checkout Without Login
   - Tests checkout flow for non-logged-in users
   - Verifies login/register prompts

4. Search Functionality
   - Tests case and symbol sensitivity
   - Verifies search results relevance

5. Newsletter Subscription
   - Tests duplicate email subscription
   - Verifies appropriate messages

6. Rapid Add to Cart
   - Tests multiple rapid clicks
   - Verifies cart quantity handling

7. Cart Persistence
   - Tests cart retention after logout/login
   - Verifies item persistence

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 