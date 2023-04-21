import requests
from bs4 import BeautifulSoup

def getSP500SymbolsFromWiki():

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'


    response = requests.get(url)


    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'constituents'})

    sp500_symbols = []
    for row in table.find_all('tr')[1:]: 
        column_data = row.find_all('td') 
        if len(column_data) >= 2: 
            symbol = column_data[0].text.strip()
            sp500_symbols.append(symbol) 

    return sp500_symbols

def nasdaq():
    key = 'QY73AL7RJZDQESXX'
    response = requests.get('https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={key}')

    lines = response.text.splitlines()
    column_names = lines[0].split(',')
    data = []
    for line in lines[1:]:
        values = line.split(',')
        company_dict = {}
        for i in range(len(column_names)):
            company_dict[column_names[i]] = values[i]
        data.append(company_dict)

    NASDAQ_Symbols = []
    for company_dict in data:
        if (company_dict['exchange'] == 'NYSE' or company_dict['exchange'] == 'NASDAQ'):
            NASDAQ_Symbols.append(company_dict['symbol'])
    return NASDAQ_Symbols