import random
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Avg, Sum, Count, Q, F, Case, When, Value, CharField, OuterRef, Subquery
from fin_analytics.models import UserProfile, Account, Transaction, Merchant, Card

class Command(BaseCommand):
    help = 'Seeds mock data and runs 15 advanced fintech ORM queries for validation.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== Seeding Mock Data ==="))
        self.seed_data()
        
        self.stdout.write(self.style.SUCCESS("\n=== Executing 15 ORM Queries ==="))

        # --- LEVEL 1: CONCEPT REPRODUCTION (1 - 5) ---
        
        # Q1: select_related
        accounts_with_users = Account.objects.select_related('user').all()
        self.stdout.write(f"Q1: Loaded {len(accounts_with_users)} accounts with related profiles.")

        # Q2: prefetch_related
        users_with_accounts = UserProfile.objects.prefetch_related('accounts').all()
        self.stdout.write(f"Q2: Loaded {len(users_with_accounts)} users with prefetched accounts.")

        # Q3: F() Expressions
        Account.objects.filter(account_number="ACC0").update(balance=F('balance') - Decimal('10.00'))
        self.stdout.write("Q3: Updated balance safely at DB-level via F() expression.")

        # Q4: Q() Expressions
        flagged_txs = Transaction.objects.filter(Q(status='FAILED') | Q(amount__gt=10000))
        self.stdout.write(f"Q4: Identified {flagged_txs.count()} flagged high-risk/failed transactions.")

        # Q5: Annotations
        accounts_with_card_counts = Account.objects.annotate(total_cards=Count('cards'))
        self.stdout.write(f"Q5: Annotated account ID {accounts_with_card_counts[0].id} with card count: {accounts_with_card_counts[0].total_cards}")

        # --- LEVEL 2: AGGREGATIONS & CROSS-RELATIONS (6 - 10) ---

        # Q6: System Aggregation
        total_ecosystem_liquidity = Account.active_objects.aggregate(total_funds=Sum('balance'))
        self.stdout.write(f"Q6: Total Active System Liquidity: ${total_ecosystem_liquidity['total_funds']}")

        # Q7: Cross-Relational Filter & Aggregation
        unverified_merchant_volume = Transaction.success_objects.filter(
            merchant__is_verified=False
        ).aggregate(total_volume=Sum('amount'))
        self.stdout.write(f"Q7: Unverified Merchant Volume: ${unverified_merchant_volume['total_volume'] or 0}")

        # Q8: Chained Group By Annotation
        avg_balance_by_type = Account.objects.values('account_type').annotate(average_funds=Avg('balance'))
        self.stdout.write(f"Q8: Grouped Breakdown: {list(avg_balance_by_type)}")

        # Q9: Multi-level Deep Filtering
        cards_by_domain = Card.objects.filter(account__user__email__endswith='@upay.com')
        self.stdout.write(f"Q9: Found {cards_by_domain.count()} cards mapped to @upay.com domain users.")

        # Q10: Complex Exclusion with Q()
        dormant_savings = Account.active_objects.filter(~Q(account_type='CHECKING'), balance=0)
        self.stdout.write(f"Q10: Identified {dormant_savings.count()} zero-balance active savings accounts.")

        # --- LEVEL 3: ADVANCED ENTERPRISE LOGIC (11 - 15) ---

        # Q11: Advanced Subqueries
        highest_funded_account_subquery = Account.objects.filter(
            user=OuterRef('pk')
        ).order_by('-balance').values('account_number')[:1]

        users_with_top_account = UserProfile.objects.annotate(
            primary_account_num=Subquery(highest_funded_account_subquery)
        )
        self.stdout.write(f"Q11: Correlated profiles to highest-funded accounts. Sample: {users_with_top_account[0].username} -> {users_with_top_account[0].primary_account_num}")

        # Q12: Conditional Expressions
        high_risk_transactions = Transaction.objects.annotate(
            risk_tier=Case(
                When(amount__gt=50000, status='SUCCESS', then=Value('CRITICAL_AUDIT')),
                When(status='FAILED', then=Value('TECHNICAL_FAILURE')),
                default=Value('NORMAL_ACTIVITY'),
                output_field=CharField(),
            )
        )
        self.stdout.write(f"Q12: Run evaluation complete. Evaluated {high_risk_transactions.count()} transactions into tiered risk matrices.")

        # Q13: Advanced Aggregation Filtering
        account_bi_metrics = Account.objects.annotate(
            successful_outflow=Sum('sent_transactions__amount', filter=Q(sent_transactions__status='SUCCESS')),
            failed_outflow=Sum('sent_transactions__amount', filter=Q(sent_transactions__status='FAILED'))
        )
        self.stdout.write(f"Q13: Single-scan metrics gathered. Sample Acc Outflow: ${account_bi_metrics[0].successful_outflow or 0}")

        # Q14: Temporal Sliding-Window Subquery Aggregation
        past_day_limit = timezone.now() - timedelta(days=1)
        recent_spending_subquery = Transaction.objects.filter(
            sender_account=OuterRef('pk'),
            status='SUCCESS',
            timestamp__gte=past_day_limit
        ).values('sender_account').annotate(total=Sum('amount')).values('total')

        overactive_accounts = Account.objects.annotate(
            recent_spend_total=Subquery(recent_spending_subquery)
        ).filter(recent_spend_total__gt=5000)
        self.stdout.write(f"Q14: Flagged {overactive_accounts.count()} accounts over 24h spending thresholds.")

        # Q15: Complex Coalescing and Multi-Table Join Annotation
        users_total_activity = UserProfile.objects.annotate(
            combined_account_holdings=Sum('accounts__balance'),
            total_initiated_transactions=Count('accounts__sent_transactions')
        ).filter(total_initiated_transactions__gt=0).order_by('-combined_account_holdings')
        self.stdout.write(f"Q15: Ranked complex portfolios. High ranking user: {users_total_activity[0].username if users_total_activity.exists() else 'None'}")

    def seed_data(self):
        # Clear existing tables to ensure deterministic testing
        Card.objects.all().delete()
        Transaction.objects.all().delete()
        Merchant.objects.all().delete()
        Account.objects.all().delete()
        UserProfile.objects.all().delete()

        # Users
        u1 = UserProfile.objects.create(username="alice", email="alice@upay.com")
        u2 = UserProfile.objects.create(username="bob", email="bob@global.com")
        
        # Merchants
        m1 = Merchant.objects.create(name="Stripe Fin", category="Fintech Gateways", is_verified=True)
        m2 = Merchant.objects.create(name="Shadow Escrow", category="Brokers", is_verified=False)

        # Accounts
        acc1 = Account.objects.create(user=u1, account_number="ACC0", account_type="CHECKING", balance=Decimal("15000.00"), is_active=True)
        acc2 = Account.objects.create(user=u1, account_number="ACC1", account_type="SAVINGS", balance=Decimal("45000.00"), is_active=True)
        acc3 = Account.objects.create(user=u2, account_number="ACC2", account_type="CHECKING", balance=Decimal("250.00"), is_active=True)
        acc4 = Account.objects.create(user=u2, account_number="ACC3", account_type="SAVINGS", balance=Decimal("0.00"), is_active=True)

        # Cards
        Card.objects.create(account=acc1, card_number="1111222233334444", expiry_date=date(2029, 12, 31))
        Card.objects.create(account=acc1, card_number="5555666677778888", expiry_date=date(2030, 5, 1))

        # Transactions
        Transaction.objects.create(sender_account=acc1, receiver_account=acc3, amount=Decimal("6000.00"), status="SUCCESS")
        Transaction.objects.create(sender_account=acc2, merchant=m1, amount=Decimal("12000.00"), status="SUCCESS")
        Transaction.objects.create(sender_account=acc3, merchant=m2, amount=Decimal("50.00"), status="FAILED")
        Transaction.objects.create(sender_account=acc1, merchant=m2, amount=Decimal("55000.00"), status="SUCCESS")