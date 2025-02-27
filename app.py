"""
app.py
------
This module sets up the Flask application and defines the API routes for managing bank accounts.
It uses the AccountManager from account.py to create accounts, and handle balance, deposit, and withdrawal operations.
"""

from dotenv import load_dotenv
import os
from decimal import Decimal, InvalidOperation
from flask import Flask, jsonify, request
from flask_cors import CORS
from account import AccountManager

load_dotenv()  # Load environment variables from .env

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

app = Flask(__name__)
CORS(app)

# Instantiate a singleton of AccountManager
account_manager = AccountManager()

# Define a maximum allowed amount for deposit/withdrawal (adjust as needed)
MAX_AMOUNT = Decimal('99999999')

@app.route('/accounts', methods=['POST'])
def create_account():
    """
    Create a new bank account with an optional initial balance.
    
    Returns:
        JSON response containing the account number and balance with status code 201.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    balance = data.get("balance", 0.0)
    account = account_manager.create_account(balance=balance)
    return jsonify({"account_number": account.account_number, "balance": account.balance}), 201

@app.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    """
    Retrieve the current balance of the specified account.
    
    Returns:
        JSON response with the balance, or an error if the account is not found.
    """
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"balance": account.get_balance()})

@app.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    """
    Deposit a specified amount into the account.
    
    Validates that the amount is positive, non-zero, does not exceed a maximum value,
    and has at most 2 decimal places. Returns the updated balance or an appropriate error message.
    """
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    if "amount" not in data:
        return jsonify({"error": "Missing 'amount' in request"}), 400

    amount = data.get("amount")
    try:
        d = Decimal(str(amount))
    except InvalidOperation:
        return jsonify({"error": "Deposit failed - Amount must be numeric and have at most 2 decimal places"}), 400

    if d < 0:
        return jsonify({"error": "Amount cannot be negative"}), 400

    if d == 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    if d.as_tuple().exponent < -2:
        return jsonify({"error": "Deposit failed - Amount must have at most 2 decimal places"}), 400

    if d > MAX_AMOUNT:
        return jsonify({"error": "Amount exceeds maximum allowed value"}), 400

    account.deposit(float(d))
    return jsonify({"balance": account.get_balance()})

@app.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    """
    Withdraw a specified amount from the account.
    
    Validates that the amount is positive, non-zero, does not exceed a maximum value,
    and has at most 2 decimal places. Returns the updated balance or an appropriate error message.
    """
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    if "amount" not in data:
        return jsonify({"error": "Missing 'amount' in request"}), 400

    amount = data.get("amount")
    try:
        d = Decimal(str(amount))
    except InvalidOperation:
        return jsonify({"error": "Withdrawal failed - Amount must be numeric and have at most 2 decimal places"}), 400

    if d < 0:
        return jsonify({"error": "Amount cannot be negative"}), 400

    if d == 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    if d.as_tuple().exponent < -2:
        return jsonify({"error": "Withdrawal failed - Amount must have at most 2 decimal places"}), 400

    if d > MAX_AMOUNT:
        return jsonify({"error": "Amount exceeds maximum allowed value"}), 400

    if account.withdraw(float(d)):
        return jsonify({"balance": account.get_balance()})
    return jsonify({"error": "Insufficient balance"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port)
