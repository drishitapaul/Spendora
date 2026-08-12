import requests
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://spendora-0ude.onrender.com"


# =========================
# API TESTS
# =========================

def test_api_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.text == "Backend running"


def test_get_transactions():
    response = requests.get(f"{BASE_URL}/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_valid_transaction():
    payload = {
        "title": "QA Test Expense",
        "amount": 100,
        "type": "expense"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Transaction added"


def test_missing_transaction_fields():
    payload = {
        "title": "Incomplete Transaction"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing fields"


def test_invalid_transaction_type():
    payload = {
        "title": "Invalid Type",
        "amount": 100,
        "type": "invalid"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid type"


def test_invalid_amount():
    payload = {
        "title": "Invalid Amount",
        "amount": "abc",
        "type": "expense"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Amount must be a number"


def test_insights_endpoint():
    response = requests.get(f"{BASE_URL}/insights")

    assert response.status_code == 200

    data = response.json()

    assert "income" in data
    assert "expense" in data
    assert "insight" in data


# =========================
# UI TESTS
# =========================

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


def test_spendora_page_loads(driver):
    driver.get("https://spendora-cyan.vercel.app/")

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "h2")
        )
    )

    assert "Spendora" in driver.page_source


def test_transaction_form_is_visible(driver):
    driver.get("https://spendora-cyan.vercel.app/")

    wait = WebDriverWait(driver, 15)

    title_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Title"]')
        )
    )

    amount_input = driver.find_element(
        By.CSS_SELECTOR,
        'input[placeholder="Amount"]'
    )

    add_button = driver.find_element(
        By.XPATH,
        "//button[text()='Add']"
    )

    assert title_input.is_displayed()
    assert amount_input.is_displayed()
    assert add_button.is_displayed()


def test_add_transaction_from_ui(driver):
    driver.get("https://spendora-cyan.vercel.app/")

    wait = WebDriverWait(driver, 15)

    title_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Title"]')
        )
    )

    amount_input = driver.find_element(
        By.CSS_SELECTOR,
        'input[placeholder="Amount"]'
    )

    title_input.send_keys("Automated QA Test")
    amount_input.send_keys("250")

    driver.find_element(
        By.XPATH,
        "//button[text()='Add']"
    ).click()

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "Automated QA Test"
        )
    )

    assert "Automated QA Test" in driver.page_source
