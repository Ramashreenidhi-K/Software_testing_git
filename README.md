Web Application Testing Automation:

This Python script automates testing for a web application using Selenium. It reads test cases from a CSV file and performs various actions on the web page, verifying expected outcomes.

Prerequisites
  Python 3.x
  Selenium WebDriver
  ChromeDriver (or other browser driver as needed)
  A CSV file containing test case definitions (see test_assertions.csv for an example)

Installation
  Install required libraries:

  In bash or project terminal:
    pip install selenium

Usage
Prepare your test cases:(basic test case is already there in csv file,if you want to do advanced test case this is how you do it...)
Create a CSV file (e.g., test_assertions.csv) with the following columns:

test_name: A unique identifier for the test case.
expected_outcome: The expected result of the test.
assertion: The type of assertion to perform (e.g., element_text, element_exists, cart_item_count).
Run the script:

Bash
python test_ecommerce.py

Test Cases:
The script currently includes the following test cases:

Test Login with valid credentials
Test adding a product to the cart
Test removing a product from the cart
Test navigating to the About Us page
Test Login with invalid credentials
You can add more test cases to the CSV file to cover different scenarios.

Customization(optional):
Change the WebDriver: Modify setup_driver() to use a different browser driver (e.g., Firefox, Edge).
Adjust test assertions: Modify the assert_condition function to add or customize assertion types.
Add more test cases: Create new test cases in the CSV file and implement corresponding test functions.

Notes:
Explicit waits: The script uses explicit waits to ensure elements are loaded before interacting with them.
Error handling: The script includes basic error handling to catch exceptions and provide informative messages.
Test data: Consider using test data files or configuration settings to manage test data efficiently.
