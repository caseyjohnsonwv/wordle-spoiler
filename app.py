import email
import json
import logging
from datetime import datetime
from smtplib import SMTP, SMTPException
from selenium import webdriver
import boto3
import env

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%Y-%m-%d %I:%M:%S')

wordle_url = 'https://www.powerlanguage.co.uk/wordle/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
wd = webdriver.Chrome(options=chrome_options)
wd.get(wordle_url)
solution = json.loads(wd.execute_script("return window.localStorage.getItem('gameState');")).get('solution')
if solution is None:
    logging.error("Failed to retrieve solution")
    exit()

today = datetime.today().strftime('%Y-%m-%d')
solution = str(solution).upper()
spoiler = f"Today's Wordle solution ({today}) is {solution}"
logging.info(spoiler)

client = boto3.client('ses', aws_access_key_id=env.SES_KEY, aws_secret_access_key=env.SES_SECRET)
client.send_email(
    Destination = {'ToAddresses':[env.MAILTO]},
    Message = {
        'Body':{'Text':{'Data':spoiler, 'Charset':'UTF-8'}},
        'Subject':{'Data':solution, 'Charset':'UTF-8'},
    },
    Source = 'caseyjohnson.emailbot@gmail.com',
)
logging.info(f"Email sent to {env.MAILTO}")