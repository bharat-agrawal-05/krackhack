from flask import Flask, render_template, request, redirect, url_for
import json
from flask import jsonify
import random

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
from flask import redirect

@app.route('/sell', methods=['POST'])
def sell_stock():
    try:
        company_name = request.form['company_name']
        quantity = int(request.form['quantity'])

        with open('stock_data.json', 'r') as file:
            data = json.load(file)

        if 'status' not in data:
            return 'Error: No stock data found.', 400

        if company_name not in data['stocks']:
            return 'Error: Company not found.', 400

        if data['stocks'][company_name] is None:
            return 'Error: Stock price unavailable.', 400

        if quantity <= 0:
            return 'Error: Invalid quantity.', 400

        # Calculate the total value of the sold stocks
        stock_price = float(data['stocks'][company_name].replace('\u20b9', '').replace(',', ''))
        total_value = stock_price * quantity

        # Calculate the profit/loss at the moment of selling
        bought_price = float(data['stocks'][company_name].replace('\u20b9', '').replace(',', ''))
        profit_loss = total_value - (bought_price * quantity)

        # Deduct the sold stocks from the status
        for idx, item in enumerate(data['status']):
            if item['company_name'] == company_name:
                remaining_quantity = int(item['quantity']) - quantity
                if remaining_quantity <= 0:
                    # Remove the entry if no remaining quantity
                    del data['status'][idx]
                else:
                    # Update quantity if remaining quantity is positive
                    data['status'][idx]['quantity'] = str(remaining_quantity)
                break
        else:
            return 'Error: Company not found in status.', 400

        # Add sold stocks to the sold_stocks list along with profit/loss
        if 'sold_stocks' not in data:
            data['sold_stocks'] = []
        data['sold_stocks'].append({'company_name': company_name, 'quantity_sold': quantity, 'total_price': total_value, 'profit_loss': profit_loss})

        # Update balance (you'll need to have a balance key in your JSON data)
        if 'balance' not in data:
            data['balance'] = 0
        data['balance'] += total_value

        # Update the JSON file with the modified data
        with open('stock_data.json', 'w') as file:
            json.dump(data, file)

        # Redirect to the status page
        return redirect(url_for('b'))

    except Exception as e:
        return str(e), 500

    finally:
        # Clean up resources, if any
        pass



@app.route('/sold_stocks')
def sold_stocks():
    try:
        with open('stock_data.json', 'r') as file:
            data = json.load(file)
        sold_stocks = data.get('sold_stocks', [])
        return render_template('sold_stocks.html', sold_stocks=sold_stocks)
    except:
        return render_template('sold_stocks.html', sold_stocks=[])



@app.route('/selling_log')
def selling_log():
    with open('stock_data.json', 'r') as file:
        data = json.load(file)
    selling_log = data.get('selling_log', [])
    return render_template('selling_log.html', selling_log=selling_log)




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

@app.route('/get_current_price', methods=['POST'])
def get_current_price():
    try:
        company_name = request.form['company_name']
        current_price = get_stock_price(company_name)
        if current_price:
            return jsonify({'price': current_price})
        else:
            return jsonify({'error': f'Error fetching price for {company_name}'})
    except Exception as e:
        return jsonify({'error': str(e)})


def write_to_json(ticker, price):
    try:
        with open('stock_data.json', 'r') as file:
            data = json.load(file)
    except:
        data = {"stocks": {}, "status": []}

    if ticker not in data["stocks"]:  # Check for duplicate entries
        data["stocks"][ticker] = price

    with open('stock_data.json', 'w') as file:
        json.dump(data, file)





@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    ticker = request.form['company_name']
    price = get_stock_price(ticker)
    print(price)
    if price:
        write_to_json(ticker, price)
        return price
    else:
        return 'Error fetching data. Please try again.'

@app.route('/b',methods=['GET'])
def b():
    try:
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
    except:
        return render_template('b.html', data={})

@app.route('/contact')
def contact():
    return render_template('contact.html')



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
    app.run(debug=True,port=8080)