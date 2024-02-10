# import requests as r
# import json

# data = r.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=PWYULZ530WNLHZZJ')
# json.dump(data.text, open('ibm.json', 'w'))

url1='https://www.google.com/finance/quote/500209:BOM'
url2='https://www.google.com/finance/quote/INFY:NSE'
import requests
from bs4 import BeautifulSoup
import time
ticker=input("Enter the company name: ")
url=f'https://www.google.com/finance/quote/{ticker}:NSE'
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')
class1="YMlKec fxKbKc"

print(soup.find(class_=class1).text)
