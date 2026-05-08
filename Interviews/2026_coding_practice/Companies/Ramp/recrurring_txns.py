"""
2. You are given a list of credit/debit card transactions. 
Each transaction has: transaction_date (YYYY-MM-DD) merchant (string) amount (decimal, positive) currency (string, e.g., USD ) Many transactions are one-off (e.g., small public transit fares), while some are recurring subscriptions/bills (e.g., Netflix). Task Identify recurring transactions and print a summary line per detected recurring pattern, in the form:
"""
from datetime import date
from typing import List
from collections import defaultdict

class Transaction:
    def __init__(self, merchant, amount, transaction_date, currency="USD"):
        self.merchant = merchant
        self.date = date.fromisoformat(transaction_date)
        self.amount = amount
        self.currency = currency

def detect_recurring_subscriptions(transactions: List[Transaction]):
    # Minimum consecutive intervals needed to classify as recurring.
    # Note: In a real app, you might want different thresholds per interval (e.g., 2 for monthly, 4 for weekly)
    MIN_INTERVALS = 2 

    # Group transactions by (merchant, amount) -> list of dates
    grouped_txns = defaultdict(list)
    for t in transactions:
        grouped_txns[(t.merchant, t.amount)].append(t.date)
    
    # Analyze each grouping
    for (merchant, amount), dates in grouped_txns.items():
        # Need at least MIN_INTERVALS + 1 dates to form the required number of intervals
        if len(dates) <= MIN_INTERVALS:
            continue
            
        dates.sort(reverse=True) # Sort latest to earliest

        yearly, monthly, biweekly, weekly = 0, 0, 0, 0

        # Calculate intervals between adjacent dates
        for i in range(len(dates) - 1):
            newer_date = dates[i]
            older_date = dates[i+1]
            
            days_diff = (newer_date - older_date).days
            months_diff = (newer_date.year - older_date.year) * 12 + (newer_date.month - older_date.month)

            if months_diff == 12:
                yearly += 1
            elif months_diff == 1:
                monthly += 1
            elif days_diff == 15:
                biweekly += 1
            elif days_diff == 7:
                weekly += 1
        
        # If any interval counter meets our threshold, flag it!
        if max(yearly, monthly, biweekly, weekly) >= MIN_INTERVALS:
            print(f"Recurring detected -> {merchant} (${amount})")

def main():
    txns = [
        # A monthly subscription (Netflix)
        Transaction("Netflix", 15.99, "2023-01-31"),
        Transaction("Netflix", 15.99, "2023-02-28"),
        Transaction("Netflix", 15.99, "2023-03-31"),
        
        # A one-off transaction
        Transaction("Starbucks", 5.50, "2023-02-14"),
        
        # A weekly subscription (Gym)
        Transaction("Gym", 20.00, "2023-03-01"),
        Transaction("Gym", 20.00, "2023-03-08"),
        Transaction("Gym", 20.00, "2023-03-15"),
        
        # Another one-off transaction
        Transaction("Uber", 25.00, "2023-03-10"),
        
        # Two different AWS bills
        Transaction("AWS", 50.00, "2023-01-05"),
        Transaction("AWS", 50.00, "2023-02-05"),
        Transaction("AWS", 10.00, "2023-01-10"), # separate bill
        Transaction("AWS", 10.00, "2023-02-10"),
    ]
    
    detect_recurring_subscriptions(txns)

if __name__ == "__main__":
    main()