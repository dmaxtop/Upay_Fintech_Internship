# High-Performance Django Fintech ORM Sandbox

This project sets up a dedicated Django financial analytics backend designed to showcase complex model relationships, custom manager queries, and advanced programmatic performance tuning against standard database query loops.

## ✨ System Architecture Features

* **Database Schema Robustness**: Implements 5 real-world core tables with strict DB-level `CheckConstraints` (e.g., stopping negative balance variations) and indexing profiles (`timestamp`, `status`, `email`).
* **Encapsulated Logic Layers**: Extracted database query paths to clean `managers.py` definitions.
* **Custom Tooling Framework**: Bundles 15 highly complex queries and performance metric validators directly into Native Django management scripts.

---

## 🚀 Step-by-Step Testing Guide



**Step 1:** Database Structural Migrations
Build your structural framework within the localized DB instance:

cd ORM

# 1. Install your packages safely inside the active venv
pip install django django-debug-toolbar

# 2. Prepare the database structure
python manage.py makemigrations fin_analytics
python manage.py migrate

# 3. Run your deliverables
python manage.py run_analytics
python manage.py run_optimization_test

**Step 2:** Run the 15 Core Deliverable Queries
Execute the core deliverable analytics engine script. This automatically creates a mock financial profile and prints data validation summaries from all 15 advanced query assignments directly to your console terminal:

Bash
python manage.py run_analytics

**Step 3:** Run the Execution Optimization Benchmark
To test the difference between the unoptimized loop (the N+1 issue) and your optimized query setup, execute the benchmarking utility:

Bash
python manage.py run_optimization_test


**QUERY TESTING**

All the query test results included in: 
ORM\Screenshots


