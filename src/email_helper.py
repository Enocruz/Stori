import boto3
from botocore.exceptions import ClientError


SENDER = "enocruz@icloud.com"
AWS_REGION = "us-west-2"
SUBJECT = "Your transactions"
CHARSET = "UTF-8"

def send_email(recipient: str, total_balance: float, monthly_transactions: dict, balances: dict) -> str:
    monthly_transactions_html = create_monthly_transactions_html(transactions=monthly_transactions)
    averages_html = create_averages_html(balances=balances)
    html_body = create_body_html(total_balance=total_balance, transactions_html=monthly_transactions_html, averages_html=averages_html)
    return send(recipient=recipient, body_html=html_body)


def send(recipient: str, body_html: str) -> str:            
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
    else:
        print(f"Email sent! Message ID: {response['MessageId']}"),
        return response['MessageId']


def create_body_html(total_balance: float, transactions_html: str, averages_html: str) -> str:
    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
        <h1>Your transactions</h1>
        <p>Here is your summary:
        <br>
        <br>
        Total balance is {total_balance}
        <br>
        {averages_html}
        <br>
        {transactions_html}
        <br>
        <img src="https://files-public-transactions.s3.us-west-2.amazonaws.com/Stori.jpg"/>
    </body>
    </html>
    """      
    return BODY_HTML


def create_monthly_transactions_html(transactions: dict) -> str:
    monthly_t = ""
    for key, value in transactions.items():
        monthly_t += f"<p>Number of transactions in {key}: {value}</p>"
    return monthly_t

def create_averages_html(balances: dict) -> str:
    averages_t = ""
    for transaction_type in balances.keys():
        transactions = balances.get(transaction_type)
        average = transactions.get("amount")/transactions.get("total_transactions")
        averages_t += f"<p>Average {transaction_type} amount: {average}</p>"
    return averages_t