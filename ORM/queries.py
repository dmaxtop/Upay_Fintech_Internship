from django.db.models import Avg, Sum, Count, Q, F, Case, When, Value, CharField, OuterRef, Subquery
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from myapp.models import UserProfile, Account, Transaction, Merchant, Card

# ==========================================
# LEVEL 1: CONCEPT REPRODUCTION (1 - 5)
# ==========================================

# Q1: select_related (SQL JOIN to fetch single-value relationships instantly)
# Fetches accounts and attaches their user profiles in a single query instead of executing N queries.
accounts_with_users = Account.objects.select_related('user').all()

# Q2: prefetch_related (Separate query multi-value JOIN for Reverse Lookups/Many-to-Many)
# Fetches all users and maps their multiple related bank accounts efficiently.
users_with_accounts = UserProfile.objects.prefetch_related('accounts').all()

# Q3: F() Expressions (Update balance database-side without pulling data into Python memory)
# Solves race conditions by safely subtracting an amount directly at the SQL level.
Account.objects.filter(account_number="ACC123").update(balance=F('balance') - Decimal('50.00'))

# Q4: Q() Expressions (Complex OR/AND logical filtering)
# Finds transactions that either failed or are greater than $10,000.
flagged_txs = Transaction.objects.filter(Q(status='FAILED') | Q(amount__gt=10000))

# Q5: Annotations (Calculate dynamic fields on-the-fly per record row)
# Attaches a dynamically generated field 'total_cards' to each individual account.
accounts_with_card_counts = Account.objects.annotate(total_cards=Count('cards'))


# ==========================================
# LEVEL 2: AGGREGATIONS & CROSS-RELATIONS (6 - 10)
# ==========================================

# Q6: System Aggregation (Summing up global ecosystem values)
# Calculates the total liquid balance held across all active bank accounts.
total_ecosystem_liquidity = Account.active_objects.aggregate(total_funds=Sum('balance'))

# Q7: Cross-Relational Filter & Aggregation
# Finds the total volume of successful transactions processed by unverified merchants.
unverified_merchant_volume = Transaction.success_objects.filter(
    merchant__is_verified=False
).aggregate(total_volume=Sum('amount'))

# Q8: Chained Group By Annotation
# Groups accounts by account_type and returns the average balance for each bucket type.
avg_balance_by_type = Account.objects.values('account_type').annotate(average_funds=Avg('balance'))

# Q9: Multi-level Deep Filtering
# Finds all credit cards connected to a user profile matching a specific email domain.
cards_by_domain = Card.objects.filter(account__user__email__endswith='@upay.com')

# Q10: Complex Exclusion with Q()
# Finds active accounts that do not have checking status and do not possess any balance.
dormant_savings = Account.active_objects.filter(~Q(account_type='CHECKING'), balance=0)


# ==========================================
# LEVEL 3: ADVANCED ENTERPRISE LOGIC (11 - 15)
# ==========================================

# Q11: Advanced Subqueries (OuterRef referencing outer scope execution)
# For every user profile, fetch the account number of their highest-funded bank account.
highest_funded_account_subquery = Account.objects.filter(
    user=OuterRef('pk')
).order_by('-balance').values('account_number')[:1]

users_with_top_account = UserProfile.objects.annotate(
    primary_account_num=Subquery(highest_funded_account_subquery)
)

# Q12: Conditional Expressions (Case-When processing logic inside SQL)
# Labels transactions dynamically based on risk indicators.
high_risk_transactions = Transaction.objects.annotate(
    risk_tier=Case(
        When(amount__gt=50000, status='SUCCESS', then=Value('CRITICAL_AUDIT')),
        When(status='FAILED', then=Value('TECHNICAL_FAILURE')),
        default=Value('NORMAL_ACTIVITY'),
        output_field=CharField(),
    )
)

# Q13: Advanced Aggregation Filtering (Django 2.0+ Filter parameter inside calculations)
# Annotates each account with their total successful volume vs failed volume in one single database scan.
account_bi_metrics = Account.objects.annotate(
    successful_outflow=Sum('sent_transactions__amount', filter=Q(sent_transactions__status='SUCCESS')),
    failed_outflow=Sum('sent_transactions__amount', filter=Q(sent_transactions__status='FAILED'))
)

# Q14: Temporal Sliding-Window Subquery Aggregation
# Identifies accounts that have spent more than $5,000 within the last 24 hours.
past_day_limit = timezone.now() - timedelta(days=1)
recent_spending_subquery = Transaction.objects.filter(
    sender_account=OuterRef('pk'),
    status='SUCCESS',
    timestamp__gte=past_day_limit
).values('sender_account').annotate(total=Sum('amount')).values('total')

overactive_accounts = Account.objects.annotate(
    recent_spend_total=Subquery(recent_spending_subquery)
).filter(recent_spend_total__gt=5000)

# Q15: Complex Coalescing and Multi-Table Join Annotation
# Finds the total amount a user has ever interacted with across both direct transfers and merchant settlements.
users_total_activity = UserProfile.objects.annotate(
    combined_account_holdings=Sum('accounts__balance'),
    total_initiated_transactions=Count('accounts__sent_transactions')
).filter(total_initiated_transactions__gt=0).order_by('-combined_account_holdings')