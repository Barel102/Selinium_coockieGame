import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import threading

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(10)
driver.maximize_window()

driver.get("https://orteil.dashnet.org/cookieclicker/")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
language = driver.find_element(By.ID, "langSelect-EN")
language.click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'bigCookie')))

lock = threading.Lock()
cookies_count = 0

def product_iteration():
    max_product_iteration = 19
    while True:
        with lock:
            try:
                while max_product_iteration >= 0:
                    product = driver.find_element(By.ID, f"product{max_product_iteration}")
                    if product.is_displayed() and product.is_enabled():
                        product.click()
                    max_product_iteration -= 1
                max_product_iteration = 19 
            except StaleElementReferenceException:
                pass
        time.sleep(10)


def cookie_clicker():
    while True:
        try:
            big_cookie = driver.find_element(By.ID, 'bigCookie')
            big_cookie.click()
        except StaleElementReferenceException:
            pass

products_thread = threading.Thread(target=product_iteration)
cookie_thread = threading.Thread(target=cookie_clicker)

products_thread.start()
cookie_thread.start()

cookie_thread.join()
products_thread.join()

driver.quit()