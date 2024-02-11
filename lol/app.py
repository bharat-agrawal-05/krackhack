from flask import Flask, render_template, request
import requests,json
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_stock_price(ticker):
    ticker=ticker.replace(" ","")  # Clean and convert ticker to uppercase
    url = f'https://www.google.com/finance/quote/{ticker}:NSE'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price_tag = soup.find(class_='YMlKec fxKbKc')
        if price_tag:
            price = price_tag.text
            return price
        else:
            return f"No price found for {ticker}"
    else:
        return f"Error fetching data for {ticker}. Please try again."


def write_to_json(ticker, price):
    try:
        with open('stock_data.json', 'r') as file:
            data = json.load(file)
    except:
        data = {"stocks": {}, "status": []}

    if ticker.lower() not in data["stocks"]:  # Check for duplicate entries
        data["stocks"][ticker.lower()] = price

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
        print(price)
        write_to_json(ticker, price)
        return price
    else:
        return 'Error fetching data. Please try again.'

@app.route('/b')
def b():
    with open('stock_data.json', 'r') as file:
        data = json.load(file)

    # Convert stock prices to float and handle missing or invalid prices
    for company, price in data['stocks'].items():
        if price.isdigit():
            data['stocks'][company] = float(price)
        elif price.startswith("₹"):  # Handle prices in Indian Rupees format
            data['stocks'][company] = float(price[1:].replace(',', ''))
        else:
            data['stocks'][company] = None  # Set price to None for invalid or missing prices

    print(data)  # Print the data for inspection

    return render_template('b.html', data=data)




@app.route('/store_buy', methods=['POST'])
def store_buy():
    try:
        company_name = request.form['company_name']
        quantity = request.form['quantity']

        with open('stock_data.json', 'r') as file:
            data = json.load(file)

        if 'status' not in data:
            data['status'] = []

        data['status'].append({'company_name': company_name, 'quantity': quantity})

        with open('stock_data.json', 'w') as file:
            json.dump(data, file)

        return 'Buy information stored successfully'
    except Exception as e:
        return str(e), 500







if __name__ == '__main__':
    app.run(debug=True)