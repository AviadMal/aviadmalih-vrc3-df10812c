# הוספת לוגיקה חדשה לניהול שגיאות
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

path = f"{os.path.expanduser('~')}/Token.txt"
url = 'http://dvdtfsp:8080/tfs/ComputingSystems_Collection/'
WEBDRIVER_CHROME = f"/usr/bin/chromedriver"


def createToken():

    try:

        if os.path.isfile(path):

            creation_time = os.path.getctime(path)

            creation_datetime = datetime.fromtimestamp(creation_time)

            current_datetime = datetime.now()

            time_difference = current_datetime - creation_datetime

            if time_difference < timedelta(days=90):

                with open(path, 'r') as f:

                    token = f.read() or None

                    if token is None:

                        os.remove(path)

                        return getToken()

                    else:

                        return token

        if 'driver' in locals():

            driver.quit()

    except Exception as e:

        print(f'Error accessing token file: {e}')

        return getToken()

    finally:

        if 'driver' in locals():

            driver.quit()

    return getToken()

def getToken():
    f = open(path, "w")
    c = webdriver.ChromeOptions()

    driver = webdriver.Chrome(WEBDRIVER_CHROME, options=c)
    token_url = f"{url}_usersSettings/tokens"
    driver.get(token_url)

    button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="New Token"]'))
    )
    button.click()

    input_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@aria-label="Name"]'))
    )
    input_field.send_keys("New Token")

    span_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Dropdown1-option"))
    )
    span_element.click()

    span_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains( text(),'90 days')]"))
    )
    span_element.click()

    div_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "__bolt-full"))
    )
    div_element.click()

    span_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Dropdown0-option"))
    )
    span_element.click()

    span_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains( text(),'All accessible organizations')]"))
    )
    span_element.click()

    button_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Create']"))
    )
    button_element.click()

    input_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "__bolt-textfield-input-4"))
    )
    os.system('cls' if os.name == 'nt' else 'clear')
    token = input_element.get_attribute("value")
    driver.quit()
    f.write(token)
    f.close()
    return token