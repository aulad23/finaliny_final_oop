from datetime import datetime


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Acc_holder(User):
    def __init__(self, name, email, address, initial_deposit):
        super().__init__(name, email)
        self.address = address
        self.balance = initial_deposit
        self.loaned = 0
        self.transaction_history = []

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                self.record_transaction("Deposit", amount)
                print(f"Successfully deposited {amount} into your account.")
            else:
                print("Deposit amount must be a positive number.")
        except ValueError:
            print("Invalid amount. Please provide a valid number.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be a positive number.")
        elif self.balance >= amount:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            print(f"Withdrawal of {amount} successful.")
        else:
            print("Insufficient balance.")

    def check_balance(self):
        print(f"Hello {self.name},")
        print(f"Your Balance: {self.balance}")

    def transfer_balance(self, amount, recipient):
        if amount <= 0:
            print("Transfer amount must be a positive number.")
        elif self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.record_transaction("Transfer", amount)
            recipient.record_transaction("Received", amount)
            print(f"Successfully transferred {amount} to {recipient.name}.")
            return True
        else:
            print("Insufficient balance. Please refill your account.")
        return False

    def take_loan(self, amount, bank):
        if bank.get_loan_application_status():
            if self.loaned == 0 and amount <= self.balance:
                self.loaned = amount
                self.record_transaction("Loan", amount)
                print(f"{amount} added to your account as a loan successfully.")
            else:
                print(f"You can't request a loan of {amount}.")
        else:
            print(f"Dear {self.name}, loan applications are not being accepted.")

    def record_transaction(self, rr_type, amount):
        transaction = {
            "type": rr_type,
            "amount": amount,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        self.transaction_history.append(transaction)

    def see_transaction_history(self):
        print(f"Hello {self.name},Your are transaction details:\n")
        for transaction in self.transaction_history:
            tr = f"- Type: {transaction['type']}, Amount: {transaction['amount']}, Time: {transaction['time']}"
            print(tr)

    def __repr__(self):
        acc_holder_details = f"Name: {self.name}\n"
        acc_holder_details += f"Balance: {self.balance}\n"
        return acc_holder_details


class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email)
        self.password = password


class Bank:
    acc_number_start = 1100
    loan_application_open = True

    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.admins = {}

    def create_account(self, account):
        account_number = self._generate_acc_no()
        self.accounts[account_number] = account

    def _generate_acc_no(self):
        self.acc_number_start += 1
        return self.acc_number_start

    def _update_total_balance(self):
        return sum(acc.balance for acc in self.accounts.values())

    def _update_total_loan(self):
        return sum(acc.loaned for acc in self.accounts.values())

    def total_bank_balance(self):
        return self._update_total_balance()

    def total_loan_given(self):
        return self._update_total_loan()

    def net_balance(self):
        return self.total_bank_balance() - self.total_loan_given()

    def toggle_loan_on_off(self, password):
        admin = self.admins.get(password)
        if admin:
            self.loan_application_open = not self.loan_application_open
            print(
                "Loan feature has been enabled."
                if self.loan_application_open
                else "Loan feature has been disabled."
            )
        else:
            print("Invalid admin password.")

    def get_loan_application_status(self):
        return self.loan_application_open

    def __repr__(self):
        acc_details = f"Bank: {self.name}\n"
        acc_details += "---------------------------\n"
        for acc_no, acc in self.accounts.items():
            acc_details += f"Account Number: {acc_no}\n"
            acc_details += f"Account Details:\n{acc}\n"
        return acc_details


# Create a bank instance
bank = Bank("My Bank")

# Create an account holder
account_holder = Acc_holder("aulad", "aulad@.com", "1216 mirpur", 1000)

# Create an admin
admin = Admin("Admin", "adminkepawajaina@.com", "password123")

# Add the account holder to the bank's accounts
bank.create_account(account_holder)

# Add the admin to the bank's admins
bank.admins[admin.password] = admin

# Deposit some money into the account holder's account
account_holder.deposit(500)

# Withdraw some money from the account holder's account
account_holder.withdraw(200)

# Transfer money from the account holder's account to another account holder's account
recipient = Acc_holder("jiku ahemad", "jiku@.1216", "bhola,cherfassion", 0)
bank.create_account(recipient)
account_holder.transfer_balance(300, recipient)

# Check the account holder's balance
account_holder.check_balance()

# Take a loan from the bank
account_holder.take_loan(1000, bank)

# Print the bank's account and admin details
print(bank)

# Print the account holder's transaction history
account_holder.see_transaction_history()
