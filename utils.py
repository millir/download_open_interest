import requests
from bs4 import BeautifulSoup
import logging


def get_html(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Error during GET request{e}".format(e))

    text = response.text
    return text


def parse(html):
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
    parsed_text = '\n'.join(chunk for chunk in lines if chunk)  # drop blank lines
    return parsed_text
