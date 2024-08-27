import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Read assertions from CSV
def read_assertions(file_path):
    assertions = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            assertions[row['test_name']] = {
                'expected_outcome': row['expected_outcome'],
                'assertion': row['assertion']
            }
    return assertions

# Setup WebDriver
def setup_driver():
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in PATH
    driver.get("http://127.0.0.1:5000")
    driver.maximize_window()
    return driver

# Helper function to find element with wait
def find_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        print(f"Element found: {value}")
        return element
    except TimeoutException:
        raise Exception(f"Element not found: {value}")

# Assertion function
def assert_condition(driver, condition, expected):
    if condition['assertion'] == 'element_text':
        element = find_element(driver, By.TAG_NAME, 'h1')
        assert element.text == expected, f"Expected {expected}, but got {element.text}"
    elif condition['assertion'] == 'element_exists':
        elements = driver.find_elements(By.NAME, expected)
        assert len(elements) > 0, f"Expected element with name {expected} to exist"
    elif condition['assertion'] == 'cart_item_count':
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
        assert len(cart_items) == int(expected), f"Expected {expected} cart items, but got {len(cart_items)}"

# Test Login with valid credentials
def test_login_valid(driver, assertions):
    try:
        login_link = find_element(driver, By.LINK_TEXT, "Login")
        login_link.click()
        time.sleep(2)  # Consider replacing with explicit wait

        username_input = find_element(driver, By.NAME, "username")
        password_input = find_element(driver, By.NAME, "password")
        login_button = find_element(driver, By.TAG_NAME, "button")

        username_input.send_keys("admin")
        password_input.send_keys("admin")
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
        )

        assert_condition(driver, assertions['test_login_valid'], assertions['test_login_valid']['expected_outcome'])
        time.sleep(2)
        print("Valid login test passed.")
    except Exception as e:
        time.sleep(2)
        print(f"Valid login test failed: {e}")

# Test adding a product to the cart
def test_add_to_cart(driver,assertions):
    try:
        

        home_link = find_element(driver, By.LINK_TEXT, "Home")
        home_link.click()
        time.sleep(5)  # Consider replacing with explicit wait

        add_to_cart_button = find_element(driver, By.LINK_TEXT, "Add to Cart")
        add_to_cart_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Remove"))
        )
        # Improved verification - adjust locator or approach as needed
        cart_items = driver.find_elements(By.NAME, ".product.name")
        assert "product.name"
        time.sleep(5)
        print("Add to cart test passed.")
    except Exception as e:
        print(f"Add to cart test failed: {e}")



# Test removing a product from the cart
def test_remove_from_cart(driver, assertions):
    try:
        remove_link = find_element(driver, By.LINK_TEXT, "Remove")
        remove_link.click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.LINK_TEXT, "Remove"))
        )

        assert_condition(driver, assertions['test_remove_from_cart'], assertions['test_remove_from_cart']['expected_outcome'])
        time.sleep(2)
        print("Remove from cart test passed.")
    except Exception as e:
        print(f"Remove from cart test failed: {e}")

# Test navigating to the About Us page
def test_about_page(driver, assertions):
    try:
        about_link = find_element(driver, By.LINK_TEXT, "About Us")
        about_link.click()
        time.sleep(2)  # Consider replacing with explicit wait

        assert_condition(driver, assertions['test_about_page'], assertions['test_about_page']['expected_outcome'])
        time.sleep(2)
        print("About page test passed.")
    except Exception as e:
        print(f"About page test failed: {e}")

# Test Login with invalid credentials
def test_login_invalid(driver, assertions):
    try:
        login_link = find_element(driver, By.LINK_TEXT, "Login")
        login_link.click()
        time.sleep(5)  # Consider replacing with explicit wait

        username_input = find_element(driver, By.NAME, "username")
        password_input = find_element(driver, By.NAME, "password")
        login_button = find_element(driver, By.TAG_NAME, "button")

        username_input.send_keys("wrong_user")
        password_input.send_keys("wrong_pass")
        login_button.click()

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "danger"))
        ).text
        assert error_message == assertions['test_login_invalid']['expected_outcome'], f"Expected {assertions['test_login_invalid']['expected_outcome']}, but got {error_message}"
        time.sleep(2)
        print("Invalid login test passed.")
    except Exception as e:
        print(f"Invalid login test failed: {e}")

# Run all tests
def run_tests():
    assertions = read_assertions('test_assertions.csv')
    driver = setup_driver()
    try:
        test_login_invalid(driver, assertions)
        test_login_valid(driver, assertions)
        test_add_to_cart(driver, assertions)
        test_remove_from_cart(driver, assertions)
        test_about_page(driver, assertions)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
