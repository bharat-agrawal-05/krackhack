from flask import Flask, render_template, request
import requests,json
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_stock_price(ticker):
    ticker = ticker.replace(" ", "")
    url = f'https://www.google.com/finance/quote/{ticker}:NSE'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        class_name = "YMlKec fxKbKc"
        price = soup.find(class_=class_name).text
        return price
    else:
        return None

def write_to_json(ticker, price):
    with open('stock_data.json', 'r') as file:
        data = json.load(file)

    data.update({ticker: price})
    with open('stock_data.json', 'w') as file:
        json.dump(data, file)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    ticker = request.form['company_name']
    price = get_stock_price(ticker)
    if price:
        write_to_json(ticker, price)
        return price
    else:
        return 'Error fetching data. Please try again.'

@app.route('/view_data',methods=['GET'])
def view_data():
    with open('stock_data.json', 'r') as file:
        data = json.load(file)

    render_template('status.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)