# importing csv, os libraries
import csv
import os


# Define user class

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    # Display balance
    def display_balance(self):
        print(f"Your balance is Rs{self.balance}")

    # transaction_history
    def display_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    # withdraw

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn {amount}")
            print(f"Withdrawn successfully. Remaining balance is Rs{self.balance}")
        else:
            print("Invalid withdraw amount or insufficient funds")

    # deposit money
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited {amount}")
            print(f"Deposited successfully. Current balance is Rs{self.balance}")
        else:
            print("Invalid deposit amount.")

    # transfer money
    def transfer(self, recipient, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f"Transferred Rs{amount} to {recipient.user_id}")
            recipient.transaction_history.append(f"Received Rs{amount} from {self.user_id}")
            print("Transfer successfully")
        else:
            print("Invalid transfer amount or insufficient funds")


# creating ATM
class ATM:
    USER_FILE = "users.csv"

    def __init__(self):
        self.users = None
        self.load_users()

    # load user
    def load_users(self):
        if os.path.exists(self.USER_FILE):
            with open(self.USER_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                self.users = [User(row[0], row[1], float(row[2])) for row in reader]
        else:
            self.users = []

    def save_user(self):
        with open(self.USER_FILE, 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User_ID", "PIN", "Balance"])
            for user in self.users:
                writer.writerow([user.user_id, user.pin, user.balance])

    def current_user(self, user_id, pin):
        new_user = User(user_id, pin)
        self.users.append(new_user)
        self.save_user()
        print(f"User {user_id} has entered successfully")

    # check user_id and user pin
    def authenticate_user(self, user_id, pin):
        for user in self.users:
            if user.user_id == user_id and user.pin == pin:
                return user
            return None


def main():
    atm = ATM()

    while True:
        print("\n Choose an option:")
        print("1. Create a new user")
        print("2. Log In")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = input("Set your user ID: ")
            pin = input("Set your PIN: ")
            atm.current_user(user_id, pin)

        elif choice == "2":
            user_id = input("Enter Your user ID: ")
            pin = input("Enter your PIN: ")

            authenticated_user = atm.authenticate_user(user_id, pin)

            if authenticated_user:
                print(f"Welcome {authenticated_user.user_id}!")

                while True:
                    print("\n Choose an option:")
                    print("1. Display Balance")
                    print("2. Display Transaction History")
                    print("3. Withdraw")
                    print("4. Deposit")
                    print("5. Transfer")
                    print("6. Quit")

                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":
                        authenticated_user.display_balance()
                    elif user_choice == "2":
                        authenticated_user.display_transaction_history()
                    elif user_choice == "3":
                        amount = float(input("Enter withdrawal amount: "))
                        authenticated_user.withdraw(amount)
                    elif user_choice == "4":
                        amount = float(input("Enter deposit amount: "))
                        authenticated_user.deposit(amount)
                    elif user_choice == "5":
                        recipient_id = input("Enter recipient's user ID: ")
                        recipient = atm.authenticate_user(recipient_id, pin)

                        if recipient:
                            amount = float(input("Enter transfer amount: "))
                            authenticated_user.transfer(recipient, amount)
                        else:
                            print("Recipient not found")
                    elif user_choice == "6":
                        print("Thank you for using out ATM. Goodbye!")
                        atm.save_user()
                        exit()
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Authentication error. Please check your credentials.")

        elif choice == "3":
            print("Thank you for using out ATM Goodbye!")
            atm.save_user()
            exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
