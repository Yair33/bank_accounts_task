"""
account.py
----------
This module contains the classes for managing bank accounts.

Classes:
    Account: Represents a bank account with an account number and a balance.
    AccountManager: Singleton class to manage multiple Account instances.
"""

import random

class Account:
    """
    Represents a bank account with a unique account number and a balance.

    Attributes:
        account_number (str): A unique identifier for the account.
        balance (float): The current balance of the account.
    """
    def __init__(self, account_number: str = None, balance: float = 0.0):
        """
        Initializes a new Account instance.

        If no account number is provided, a random number between 1000 and 9999 is generated.

        Args:
            account_number (str, optional): The account number. Defaults to None.
            balance (float, optional): The initial balance. Defaults to 0.0.
        """
        self.account_number = str(account_number) if account_number else str(random.randint(1000, 9999))
        self.balance = balance
    
    def get_balance(self) -> float:
        """
        Retrieves the current balance of the account.

        Returns:
            float: The current balance.
        """
        return self.balance
    
    def deposit(self, amount: float) -> None:
        """
        Deposits the specified amount into the account if the amount is greater than zero.

        Args:
            amount (float): The amount to deposit.
        """
        if amount > 0:
            self.balance += amount
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraws the specified amount from the account if sufficient funds are available.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal was successful, False if insufficient funds.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class AccountManager:
    """
    Singleton class for managing multiple bank accounts.

    This class holds a dictionary of accounts and provides methods to create and retrieve accounts.

    Attributes:
        accounts (dict): A mapping from account numbers (str) to Account instances.
    """
    _instance = None

    def __new__(cls):
        """
        Overrides __new__ to implement the singleton pattern.

        Returns:
            AccountManager: The singleton instance of the AccountManager.
        """
        if cls._instance is None:
            cls._instance = super(AccountManager, cls).__new__(cls)
            cls._instance.accounts = {}
        return cls._instance

    def create_account(self, balance: float = 0.0) -> Account:
        """
        Creates a new account with an optional initial balance.

        Args:
            balance (float, optional): The initial balance for the new account. Defaults to 0.0.

        Returns:
            Account: The newly created Account instance.
        """
        account = Account(balance=balance)
        self.accounts[str(account.account_number)] = account
        return account

    def get_account(self, account_number: str) -> Account:
        """
        Retrieves an account by its account number.

        Args:
            account_number (str): The account number to look up.

        Returns:
            Account: The Account instance if found, otherwise None.
        """
        return self.accounts.get(str(account_number))
