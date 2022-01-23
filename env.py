from dotenv import load_dotenv
load_dotenv()

from os import getenv
SES_KEY = getenv('SES_KEY')
SES_SECRET = getenv('SES_SECRET')
MAILTO = getenv('MAILTO') or 'caseyjohnson.emailbot@gmail.com'