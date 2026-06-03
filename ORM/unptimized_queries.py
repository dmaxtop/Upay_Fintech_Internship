from sqlalchemy import Transaction
# BAD: This triggers an "N+1 Problem" execution loop.
# It makes 1 query to get the transactions, then loops through them making 3 brand-new database hits PER ROW to fetch foreign keys.



transactions = Transaction.objects.all()[:100]
for tx in transactions:
    print(tx.sender_account.user.username)  # Implicit DB Hit!
    print(tx.receiver_account.account_number)  # Implicit DB Hit!
    print(tx.merchant.name)  # Implicit DB Hit!