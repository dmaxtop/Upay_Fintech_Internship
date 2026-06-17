import time
from datetime import datetime
from typing import List, Generator

# ==========================================
# 1. THE DECORATOR: Audit & Performance Logger
# ==========================================
def audit_transaction(func):
    """A decorator that audits financial function execution and logs processing speeds."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        # Run the actual function (e.g., deposit or withdraw)
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # args[0] is 'self' (the instance of BankAccount calling the method)
        account_name = args[0].name if args else "Unknown Account"
        print(f"[AUDIT] Operation '{func.__name__}' on {account_name} processed in {execution_time:.6f}s")
        return result
    return wrapper


# ==========================================
# 2. THE MAIN CLASS (With Properties & Dunder Methods)
# ==========================================
class BankAccount:
    """A safe, fully audited financial account blueprint."""
    
    def __init__(self, name: str, initial_balance: float):
        self.name = name 
        self._balance = float(initial_balance) # private-by-convention attribute
        self.transaction_history = [] 
        self._log_transaction("Account creation", initial_balance, "Initial setup")
    
    @property
    def balance(self) -> float: 
        """The getter: allows reading the balance safely."""
        return self._balance
    
    @balance.setter
    def balance(self, amount: float):
        """The setter: intercepts direct assignments and validates them."""
        if amount < 0:
            raise ValueError("Amount should be a non-negative number")
        self._balance = amount

    def _log_transaction(self, transaction_type: str, amount: float, note: str = ""):
        """Internal ledger helper."""
        log = {
            "time": datetime.now().isoformat(),
            "type": transaction_type,
            "amount": amount,
            "note": note
        }
        self.transaction_history.append(log)

    @audit_transaction
    def deposit(self, amount: float):
        """Standard method for depositing money (uses the setter under the hood)."""
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        
        self.balance += amount 
        self._log_transaction("Deposit", amount, "Standard Deposit")

    # --- DUNDER METHODS ---
    def __str__(self) -> str:
        return f"Account Owner: {self.name} | Balance: ${self.balance:.2f}"

    def __repr__(self) -> str:
        return f"BankAccount(name='{self.name}', balance={self.balance})"

    def __add__(self, other) -> 'BankAccount':
        """Merges two bank accounts cleanly."""
        if not isinstance(other, BankAccount):
            raise TypeError("Can only merge BankAccount instances.")
        combined_name = f"Joint: {self.name} & {other.name}"
        return BankAccount(name=combined_name, initial_balance=self.balance + other.balance)

    def __lt__(self, other) -> bool:
        """Enables sorting based on financial balance."""
        if not isinstance(other, BankAccount):
            raise TypeError("Comparison must be between BankAccount instances.")
        return self.balance < other.balance


# ==========================================
# 3. CLASS INHERITANCE
# ==========================================
class SavingsAccount(BankAccount):
    """A specialized bank account that earns interest but restricts withdrawals."""
    
    def __init__(self, name: str, initial_balance: float, interest_rate: float):
        # super().__init__() runs the parent constructor
        super().__init__(name, initial_balance)
        self.interest_rate = interest_rate  # e.g., 0.05 for 5% interest
        self.withdrawal_count = 0
        self.MAX_WITHDRAWALS = 3

    def apply_interest(self):
        """Calculates interest and adds it to the balance."""
        interest_earned = self.balance * self.interest_rate
        self.balance += interest_earned 
        self._log_transaction("Interest Gain", interest_earned, f"Applied {self.interest_rate * 100}% interest")
        print(f"Interest applied! New balance: ${self.balance:.2f}")

    def withdraw(self, amount: float):
        """Custom withdrawal logic with specific savings account rule limits."""
        if self.withdrawal_count >= self.MAX_WITHDRAWALS:
            print("Transaction Rejected: Monthly withdrawal limit reached!")
            return

        if amount > self.balance:
            print("Transaction Rejected: Insufficient funds!")
            return

        self.balance -= amount
        self.withdrawal_count += 1
        self._log_transaction("Withdrawal", amount, f"Withdrawal #{self.withdrawal_count}")
        print(f"Withdrew ${amount:.2f}. Balance remaining: ${self.balance:.2f}")


# ==========================================
# 4. THE GENERATOR: Lazy Ledger Streamer
# ==========================================
def transaction_streamer(history_list: List[dict]) -> Generator[dict, None, None]:
    """
    Yields ledger data one item at a time.
    Prevents high memory usage when evaluating millions of transactions.
    """
    for record in history_list:
        yield record


# ==========================================
# 5. TESTING ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    print("--- 1. Testing Decorator & Basic Class ---")
    user_acc = BankAccount("Alice", 5000.00)
    user_acc.deposit(1250.00) 

    print("\n--- 2. Testing Inheritance (Savings) ---")
    my_savings = SavingsAccount(name="John Doe", initial_balance=1000.0, interest_rate=0.05)
    my_savings.deposit(500) 
    my_savings.apply_interest() 
    my_savings.withdraw(100)

    print("\n--- 3. Testing Generator (Lazy Evaluation) ---")
    # Simulate a bunch of transactions
    for i in range(1, 4):
        user_acc._log_transaction("STREET_CHARGE", 10.50 * i, f"Merchant payment {i}")

    ledger_stream = transaction_streamer(user_acc.transaction_history)
    print(f"Generator Object initiated: {ledger_stream}") 

    print("\nConsuming the generator stream:")
    for transaction in ledger_stream:
        print(f"[{transaction['time']}] {transaction['type']}: ${transaction['amount']}")