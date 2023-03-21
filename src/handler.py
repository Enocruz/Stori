from datetime import datetime
from email_helper import send_email
from s3_helper import get_file

def handler(event, context):
    try:
        recipient = event.get("recipient")
        file_name = event.get("file")
        transactions_file = get_file(file_name=file_name)
        total_balance, transactions, monthly_transactions = read_transactions(file=transactions_file)
        if not total_balance and not transactions and not monthly_transactions:
            print("Cannot send email, input values are not valid")
            return None
        id = send_email(recipient=recipient, total_balance=total_balance, monthly_transactions=monthly_transactions, balances=transactions)
        return id
    except Exception as e:
        print(e)
        return None


def read_transactions(file) -> tuple[int, dict, dict]:
    transactions = {
        "debit": {"amount": 0, "total_transactions": 0},
        "credit": {"amount": 0, "total_transactions": 0}
    }
    monthly_transactions = {}
    total_balance = 0
    try:
        lines = file.read().decode('utf-8').split()
        # Remove titles
        lines.pop(0)
        for transaction in lines:
            transaction = transaction.split(",")
            new_transaction = format_transaction(transaction=transaction)
            month = new_transaction.get("date").strftime("%B")
            transaction_amount = new_transaction.get("amount")
            transaction_type = "credit" if transaction_amount > 0 else "debit"
            total_balance += transaction_amount
            transactions[transaction_type]["amount"] += transaction_amount
            transactions[transaction_type]["total_transactions"] += 1
            if monthly_transactions.get(month):    
                monthly_transactions[month] += 1
            else:
                monthly_transactions[month] = 1
        return total_balance, transactions, monthly_transactions
    except Exception as e:
        print("Something happened in the parsing")
        print(e)
        return None, None, None
    
def format_transaction(transaction: list) -> dict:
    return {
        "id": int(transaction[0]),
        "date": datetime.strptime(transaction[1], "%d/%m/%y"),
        "amount": float(transaction[-1])
    }