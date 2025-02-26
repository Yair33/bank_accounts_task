import random
from flask import Flask, jsonify, request

app = Flask(__name__)

class Account:
    def __init__(self, account_number: str = None, balance: float = 0.0):
        self.account_number = str(account_number) if account_number else str(random.randint(1000, 9999))
        self.balance = balance
    
    def get_balance(self) -> float:
        return self.balance
    
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class AccountManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AccountManager, cls).__new__(cls)
            cls._instance.accounts = {}
        return cls._instance

    def create_account(self, balance: float = 0.0) -> Account:
        account = Account(balance=balance)
        self.accounts[str(account.account_number)] = account
        return account

    def get_account(self, account_number: str) -> Account:
        return self.accounts.get(str(account_number))

# Singleton instance
account_manager = AccountManager()

@app.route('/accounts/create', methods=['POST'])
def create_account():
    data = request.get_json()
    balance = data.get("balance", 0.0)
    
    # Generate a new unique account number
    account_number = str(uuid.uuid4())[:8]  # Shorten UUID for readability
    
    # Create the account
    account = account_manager.create_account(account_number, balance)
    
    return jsonify({"account_number": account.account_number, "balance": account.balance}), 201

@app.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"balance": account.get_balance()})

@app.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data.get("amount", 0.0)
    account.deposit(amount)
    return jsonify({"balance": account.get_balance()})

@app.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    account = account_manager.get_account(account_number)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    data = request.get_json()
    amount = data.get("amount", 0.0)
    if account.withdraw(amount):
        return jsonify({"balance": account.get_balance()})
    return jsonify({"error": "Insufficient balance"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


