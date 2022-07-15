from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Absolute path to chromedriver.exe
chrome_driver_path = "ABSOLUTE_PATH"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Locate on-page elements via Selenium webdriver
cookie = driver.find_element(By.ID, "cookie")
store_items = driver.find_elements(By.CSS_SELECTOR, '#store div')
item_ids = [item.get_attribute("id") for item in store_items]

timeout = time.time() + 5  # 5 seconds
one_min = time.time() + 60 * 1  # 1 minutes

while True:
    cookie.click()

    # Check every 5 seconds
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert item cost strings to integers
        for price in all_prices[0:8]:
            cookie_cost = int(price.text.split()[-1].replace(",", ""))
            item_prices.append(cookie_cost)

        # Dictionary containing price:id from item_prices
        cookie_upgrades = {item_prices[price]: item_ids[price] for price in range(len(item_prices))}

        # Get Current count of cookie
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        # Loop to find highest affordable upgrade
        for cost, item_id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = item_id

        # Variable containing the highest price (key:)
        highest_price_affordable_item = max(affordable_upgrades)

        # Variable containing the id (:value)  of the highest price (the value)
        highest_item_id = affordable_upgrades[highest_price_affordable_item]

        # Click the highest priced affordable item
        driver.find_element(By.ID, highest_item_id).click()

        # Wait 5 seconds
        timeout = time.time() + 5

        # After 1 minute print the cookies per second
        if time.time() > one_min:
            cookie_per_second = driver.find_element(By.ID, "cps")
            print(cookie_per_second)
            break