"""This Program is a simple termianl based Budget Tracker based on OOPs concepts.
It has following features:
1. Add Transaction (Income/Expense)
2. Show All Transactions
3. Calculate Balance
4. Monthly Summary(Income/Expense for a given month)
The data is stored in a CSV file using pandas library for easy data manipulation and retrieval.
get_int and get_float functions are used to handle user input and ensure valid data types are entered in a loop.
"""

from datetime import date
import pandas as pd 

STORAGE_FILE = "Projects/BudgetManager/storage.csv"

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid amount(only numbers).")

class Budget:
    def __init__(self):
        try:
            self.__df = pd.read_csv(STORAGE_FILE)
        except FileNotFoundError:
            self.__df = pd.DataFrame(columns=["Amount", "Type", "Date", "Notes"])

    def add_transaction(self, transaction_date=date.today()):
        transaction_type = ""
        while transaction_type not in ["Income", "Expense"]:
            transaction_type = input("Enter transaction type (income/expense): ").strip().capitalize()
            if transaction_type not in ["Income", "Expense"]:
                print("Invalid input! Please enter 'income' or 'expense'.")

        amount = get_float("Enter amount: ")
        notes = input("Enter notes (Optional): ").title() or "—"

        self.to_csv(amount, transaction_type, notes, transaction_date)
        print(f"{transaction_type} of {amount:.2f} recorded successfully on {transaction_date}.")


    def show_transactions(self):
        print(" All Transactions ".center(60, "="))
        if self.__df.empty:
            print("No transactions recorded yet.")
            return

        headers = ["Date", "Type", "Amount", "Notes"]
        col_widths = [12, 10, 15, 15]
        header_row = " | ".join(h.center(w) for h, w in zip(headers, col_widths))
        print(header_row)
        print("-" * len(header_row))

        for _, row in self.__df.iterrows():
            date = str(row["Date"])[:10].center(col_widths[0])
            t_type = str(row["Type"]).center(col_widths[1])
            amount = f"${row['Amount']:,.2f}".center(col_widths[2])
            notes = str(row["Notes"]).center(col_widths[3])
            print(f"{date} | {t_type} | {amount} | {notes}")


    def calculate_balance(self):
        self.__df['Amount'] = pd.to_numeric(self.__df['Amount'], errors='coerce').fillna(0)
        totals = self.__df.groupby('Type')['Amount'].sum().fillna(0)
        income = totals.get('Income', 0.0)
        expense = totals.get('Expense', 0.0)
        
        balance = income - expense
        print(f"Your Current Balance is: {balance:,.2f}")
    
    def monthly_summary(self):
        month = get_int("Enter month (1-12): ")           
        year = get_int("Enter year (e.g., 2025): ")
        
        date_c = f"{month:02d}-{year}"
        print(f"Summary for {date_c}".center(50, "="))
        
        self.__df['Date'] = pd.to_datetime(self.__df['Date'], errors='coerce')
        self.__df = self.__df.dropna(subset=['Date'])  
        
        self.__df['Period'] = self.__df['Date'].dt.to_period('M')
        period_key = pd.Period(f"{year}-{month:02d}")
        
        if period_key in self.__df['Period'].unique():
            monthly_data = self.__df.groupby('Period').get_group(period_key)
            print(monthly_data)
        else:
            print("No records found for that month.")


    def to_csv(self , amount , transaction_type, notes , transaction_date=date.today()):
        new_row = {
            "Amount": amount,
            "Type": transaction_type,
            "Date": transaction_date,
            "Notes": notes
        }
        self.__df.loc[len(self.__df)] = new_row
        self.__df.to_csv(STORAGE_FILE, index=False)

def main():
    budget = Budget()
    
    while True:
        print("\n Budget Manager ".center(48))
        print("1. Add Transaction")
        print("2. Show All Transactions")
        print("3. Calculate Balance")
        print("4. Monthly Summary")
        print("5. Exit")
        
        choice = get_int("Choose an option (1-5): ")
        
        if choice == 1:
            budget.add_transaction()
        elif choice == 2:
            budget.show_transactions()
        elif choice == 3:
            budget.calculate_balance()
        elif choice == 4:
            budget.monthly_summary()
        elif choice == 5:
            print("Exiting Budget Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

