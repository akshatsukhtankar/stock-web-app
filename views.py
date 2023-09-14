from datetime import datetime
import requests
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from . import db
from .models import Stock

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    user_stocks = Stock.query.filter_by(user_id=current_user.id).all()
    total = 0
    totalGainLoss_dollar = 0.0
    totalGainLoss_percent = 0.0
    if user_stocks:
        for stock in user_stocks:
            current_price = get_current_price(stock.companyName)
            quantity = float(stock.quantity)
            price = float(current_price)
            stock_value = price * quantity
            total += stock_value
            totalGainLoss_dollar = totalGainLoss_dollar + ((
                stock.quantity * stock.current_price - stock.quantity * stock.purchasePrice))
            totalGainLoss_dollar = round(totalGainLoss_dollar, 2)
        total = round(total, 2)
        update_stock_prices()
        stockCurrent = 0.0
        stockPurchase = 0.0
        for stock in user_stocks:
            stockPurchase = stockPurchase + (stock.quantity * stock.purchasePrice)
            stockCurrent = stockCurrent + (stock.quantity * stock.current_price)
        totalGainLoss_percent = ((stockCurrent - stockPurchase) / (stockPurchase)) * 100
        totalGainLoss_percent = round(totalGainLoss_percent, 2)

    return render_template("home.html", user=current_user, total=total, totalPercent=totalGainLoss_percent,
                           totalDollar=totalGainLoss_dollar)


@views.route('/get-add-stock-form/<symbol>')
@login_required
def get_add_stock_form(symbol):
    return render_template('add_stock_form.html', symbol=symbol)

@views.route('/cash-management', methods=['GET'])
@login_required
def cash_management():
    return render_template('edit_cash_form.html', user=current_user)

@views.route('/deposit-cash', methods=['POST'])
@login_required
def deposit_cash():
    data = request.get_json()
    amount = float(data['amount'])
    if current_user.cash:
        current_user.cash += amount
    else:
        current_user.cash = amount
    db.session.commit()
    return jsonify(message="Cash deposited successfully")

@views.route('/withdraw-cash', methods=['POST'])
@login_required
def withdraw_cash():
    data = request.get_json()
    amount = float(data['amount'])
    if current_user.cash:
        if current_user.cash < amount:
            return jsonify(message="Not enough cash to withdraw")
        else:
            current_user.cash -= amount
    else:
        current_user.cash = amount
    db.session.commit()
    return jsonify(message="Cash withdrawn successfully")


def update_stock_prices():
    user_stocks = Stock.query.filter_by(user_id=current_user.id).all()
    for stock in user_stocks:
        api_key = 'cjl5kl1r01qvr02ibctgcjl5kl1r01qvr02ibcu0'
        stock_symbol = stock.companyName
        endpoint = f'https://finnhub.io/api/v1/quote?symbol={stock_symbol}&token={api_key}'
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            current_price = data['c']
            current_price = float(current_price)
            stock.current_price = round(current_price, 2)
            gainLoss = current_price - stock.purchasePrice
            percent = float((gainLoss / stock.purchasePrice) * 100)
            stock.percent_gain = round(percent, 2)
        else:
            print("well")

    # Commit the changes to the database
    db.session.commit()


def get_current_price(symbol):
    api_key = 'cjl5kl1r01qvr02ibctgcjl5kl1r01qvr02ibcu0'

    endpoint = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'

    # Make the GET request
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        # Extract the current price
        current_price = data['c']
        return current_price
    else:
        print(f'Failed to fetch data. Status code: {response.status_code}')


@views.route('/add-stock', methods=['POST'])
@login_required
def add_stock():
    data = request.get_json()
    symbol = data['symbol']
    name = data['name']
    purchase_price = float(data['purchasePrice'])
    quantity = float(data['quantity'])
    date_string = data['date']

    # Convert the date string to a datetime object
    date = datetime.strptime(date_string, '%Y-%m-%d')

    existing = Stock.query.filter_by(companyName=symbol, user_id=current_user.id).first()

    if existing:
        newQ = quantity + existing.quantity
        newPurchasePrice = (purchase_price * (quantity / newQ)) + (existing.purchasePrice * (existing.quantity / newQ))
        newPurchasePrice = round(newPurchasePrice, 2)
        db.session.delete(existing)
        db.session.commit()
        stock = Stock(
            companyName=name,
            purchasePrice=newPurchasePrice,
            quantity=newQ,
            date=date,
            current_price=get_current_price(name),
            user_id=current_user.id
        )
    else:
        stock = Stock(
            companyName=name,
            purchasePrice=purchase_price,
            quantity=quantity,
            date=date,
            current_price=get_current_price(name),
            user_id=current_user.id
        )
    db.session.add(stock)
    db.session.commit()

    # Return a JSON response
    return jsonify(message="Stock added successfully")


@login_required
@views.route('/sell-stock', methods=['POST'])
def sell_stock():
    # Get data from the request
    data = request.get_json()

    stock = Stock.query.filter_by(user_id=current_user.id, companyName=data['symbol']).first()
    if stock:
        if data['quantity'] > stock.quantity:
            return jsonify({'message': 'Not enough shares to sell'})
        else:
            stock.quantity -= data['quantity']
            if round(stock.quantity,2) == 0.0:
                db.session.delete(stock)
    else:
        return jsonify({'message': 'Stock is not in your portfolio'})

    db.session.commit()