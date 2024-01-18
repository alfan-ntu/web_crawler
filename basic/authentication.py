import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://news.ycombinator.com'
USERNAME = ""
PASSWORD = ""

s = requests.Session()

data = {"goto": "news", "acct": USERNAME, "pw": PASSWORD}
r = s.post(f'{BASE_URL}/login', data=data)

soup = BeautifulSoup(r.text, 'html.parser')
if soup.find(id='logout') is not None:
    print('Successfully logged in')
else:
    print('Authentication Error')
