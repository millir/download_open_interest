import requests
from bs4 import BeautifulSoup
import logging


url = 'https://www.cftc.gov/dea/futures/deanymesf.htm'



class OpenInterest:
    def __init__(self) -> None:
        self.contract = None
        self.open_interest = None
    
    def add_contract(self, contract: str):
        self.contract = contract

    def add_open_interest(self, open_interest: int):
        self.open_interest = open_interest

    def validate_values_are_set(self):
        if self.contract and self.open_interest:
            return True
        else:
            return False


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


def extract_open_interest(text):
    output = "contract,open_interest\n"

    oi = OpenInterest()    
    
    for line in text.splitlines():

        if 'Code-' in line:
            contract_string = line.split(' - ')[0]  # get contract name before exchange name
            contract_value = contract_string.strip()  # remove any trailing spaces
            oi.add_contract(contract=contract_value)

        if '                  OPEN INTEREST:    ' in line:
            open_interest_string = line.split('OPEN INTEREST:')[-1]  # get number after OPEN INTEREST text
            open_interest_value = open_interest_string.strip().replace(',','')  # remove spaces and comma from number
            oi.add_open_interest(open_interest=open_interest_value)
    
        if oi.validate_values_are_set():
            output += oi.contract + ','
            output += oi.open_interest + '\n'
            oi = OpenInterest()  # overwrite with new instance, for new data

    return output


html = get_html(url)
text = parse(html)
output = extract_open_interest(text)
print(output)
with open("download_open_interest/outputs/open_interests.txt", "w") as text_file:
    text_file.write(output)
