from time import time
from os import environ
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException

load_dotenv()

USER_AGENT = environ["USER_AGENT"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"user-agent={USER_AGENT}")

driver =  webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker/")

driver_wait = WebDriverWait(driver, 10)

language = driver_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="langSelect-EN"]')))
language.click()

accept_cookies = driver_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cc_btn_accept_all')))
accept_cookies.click()

cookie = driver_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="bigCookie"]')))

timer_for_game = time() + 60*5
while time() < timer_for_game:
    timeout = time() + 20
    while time() < timeout:
        cookie.click()

    number_of_cookies = float(driver.find_element(By.ID, "cookies")
                              .text.split()[0]
                              .replace(",", ""))
    characters = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")

    for index in range(len(characters)-1, -1, -1):
        price = float(driver.find_element(By.ID, f"productPrice{index}").text
                      .replace(",", ""))
        if number_of_cookies >= price:
            character = driver.find_element(By.ID, f"product{index}")
            try:
                driver.implicitly_wait(1)
                character.click()
            except Exception as e:
                try:
                    character = driver.find_element(By.ID, f"product{index-1}")
                    driver.implicitly_wait(1)
                    character.click()
                except IndexError:
                    print("Index is out of a range")

    driver.implicitly_wait(1)
    perks = driver.find_elements(By.CSS_SELECTOR, ".crate.enabled")
    for perk in perks:
        try:
            perk.click()
            driver.implicitly_wait(1)
        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:
            pass

driver.implicitly_wait(2)
cookies_per_second = driver.find_element(By.ID, "cookiesPerSecond").text
print(f"Cookies {cookies_per_second}")

driver.quit()