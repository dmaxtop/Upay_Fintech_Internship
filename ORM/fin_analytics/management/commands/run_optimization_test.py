import time
from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from fin_analytics.models import Transaction

class Command(BaseCommand):
    help = 'Tracks the difference between N+1 queries and Optimized Queries.'

    def handle(self, *args, **options):
        if not Transaction.objects.exists():
            self.stdout.write(self.style.ERROR("Database empty. Run: python manage.py run_analytics first."))
            return

        self.stdout.write(self.style.WARNING("\n=== Running Unoptimized N+1 Query Loop ==="))
        reset_queries()
        start_time = time.perf_counter()
        
        # Unoptimized Target N+1
        transactions = Transaction.objects.all()[:100]
        for tx in transactions:
            _sender = tx.sender_account.user.username
            _receiver = tx.receiver_account.account_number if tx.receiver_account else None
            _merchant = tx.merchant.name if tx.merchant else None
            
        unoptimized_time = (time.perf_counter() - start_time) * 1000
        unoptimized_queries_count = len(connection.queries)

        self.stdout.write(f"Total Database Queries Executed: {unoptimized_queries_count}")
        self.stdout.write(f"Total Computation Speed: {unoptimized_time:.2f} ms")


        self.stdout.write(self.style.SUCCESS("\n=== Running Optimized Join Selection ==="))
        reset_queries()
        start_time = time.perf_counter()
        
        # Optimized with select_related
        optimized_transactions = Transaction.objects.select_related(
            'sender_account__user', 
            'receiver_account', 
            'merchant'
        ).all()[:100]
        
        for tx in optimized_transactions:
            _sender = tx.sender_account.user.username
            _receiver = tx.receiver_account.account_number if tx.receiver_account else None
            _merchant = tx.merchant.name if tx.merchant else None

        optimized_time = (time.perf_counter() - start_time) * 1000
        optimized_queries_count = len(connection.queries)

        self.stdout.write(f"Total Database Queries Executed: {optimized_queries_count}")
        self.stdout.write(f"Total Computation Speed: {optimized_time:.2f} ms")
        
        efficiency = ((unoptimized_time - optimized_time) / unoptimized_time) * 100
        self.stdout.write(self.style.SUCCESS(f"\nOptimization results: Reduced database hits by {unoptimized_queries_count - optimized_queries_count} queries and made execution {efficiency:.1f}% faster."))