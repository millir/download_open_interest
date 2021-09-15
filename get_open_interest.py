from open_interest import OpenInterest
from utils import parse, get_html

url = 'https://www.cftc.gov/dea/futures/deanymesf.htm'


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
    
        # class and validation was done to verify that both contract and open_interest exist in source data
        if oi.validate_values_are_set(): 
            output += oi.contract + ','
            output += oi.open_interest + '\n'
            oi = OpenInterest()  # overwrite with new instance, for new data

    return output


if __name__ == '__main___':
    html = get_html(url)
    text = parse(html)
    output = extract_open_interest(text)
    print(output)
    with open("outputs/open_interests.txt", "w") as text_file:
        text_file.write(output)
