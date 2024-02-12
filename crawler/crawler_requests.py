import requests
from bs4 import BeautifulSoup as bs



def static_crawl(url: str):
    response = requests.get(url)

    html_text = response.text
    html = bs(html_text, 'html.parser')

    result = html.find_all("div", class_='se-main-container')
    print(result)
