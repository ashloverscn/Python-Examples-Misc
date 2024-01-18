import base64
import pandas as pd
from random import randint, choices
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from jinja2 import Template
import ssl
import smtplib
import logging
import time as time
import sys
import pdfkit
import imgkit
import img2pdf
import os
import os.path
import string
from datetime import date
import uuid
import datetime
import threading

def run_authorization_flow():
    cred = flow.run_local_server(port=8080, open_browser=False)
    return cred

if __name__ == '__main__':

    email = 'reagancrane4@gmail.com'
    password = 'Mintsyz@134'
    
    CLIENT_SECRETS_FILE = "./credentials/" + email + ".json"
    SCOPES = ['https://mail.google.com/']
    flow = InstalledAppFlow.from_client_secrets_file("./credentials/" + email + ".json", SCOPES, redirect_uri='http://localhost:8080')
    auth_url, _ =  flow.authorization_url(prompt='consent')
    authorization_thread = threading.Thread(target=run_authorization_flow)
    authorization_thread.start()
    #driver = webdriver.Chrome()
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver = uc.Chrome()
    driver.maximize_window()
    driver.get(auth_url)

    # Wait for the page to load
    time.sleep(3)

    wait = WebDriverWait(driver, 10)

    password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"

    email_element = wait.until(EC.visibility_of_element_located((By.ID, 'identifierId')))
    email_element.send_keys(email)

    email_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#identifierNext > div > button > span'))).click()


    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector))).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#passwordNext > div > button > span').click()

    time.sleep(5)
    
    print(auth_url)
    authorization_thread.join()

    
