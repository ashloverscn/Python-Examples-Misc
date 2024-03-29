
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import undetected_chromedriver as uc
import random
import string
import os

#service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)
driver = uc.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

email, password = 'reagancrane4@gmail.com', 'Mintsyz@134'
projectId = 'annular-accord-409813'

############################################################################
driver.get('https://console.cloud.google.com/')
time.sleep(3)
password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"
email_element = wait.until(EC.visibility_of_element_located((By.ID, 'identifierId')))
email_element.send_keys(email)
email_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#identifierNext > div > button > span'))).click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector))).send_keys(password)
driver.find_element(By.CSS_SELECTOR, '#passwordNext > div > button > span').click()
############################################################################
driver.get(f'https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={projectId}&login=true')
time.sleep(3)
#enabled_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="enable this API"]')))
#enabled_button.click()
#enabled_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Enable']")))
#enabled_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="enable this API"]')))
enabled_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cfc-flex-grow-content']//*[@aria-label='enable this API']")))
while True:
    try:
        enabled_button.click()
    except Exception as e:
        break
time.sleep(5)
driver.quit()
