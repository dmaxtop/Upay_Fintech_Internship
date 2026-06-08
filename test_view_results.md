**Django Views**
Executing Django CBV Lifecycle Verification Tests...
------------------------------------------------------------
✅ Test 0 (Base View): GET -> 200 (Custom low-level GET response)
                       POST -> 200 (Custom low-level POST response)

✅ Test 1 (TemplateView) Context Verified: page_title = 'Account Dashboard'

C:\Users\i-mumit\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\django\views\generic\list.py:91: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'models.Account'> QuerySet.
  return self.paginator_class(
✅ Test 2 (ListView) Database Query Executed:
   - Pulled 1 account(s) from memory DB.
   - Target Record Found: ACC-111222

✅ Test 3 (CreateView) Pipeline Executed:
   - Status Code: 302 (Redirect to /accounts/)
   - DB Verification: New account created with balance $150.75

✅ Test 4 (UpdateView) Pipeline Executed:
   - Status Code: 302 (Redirect to /accounts/)
   - DB Verification: Refreshed Type -> 'Business Savings', Balance -> $9999.99

✅ Test 5 (DeleteView) Pipeline Executed:
   - Status Code: 302 (Redirect to /accounts/)
   - DB Verification: Record search count for ID 1 is now 0 (Successfully Purged)






**DRF Views**
Executing Verification Tests...
--------------------------------------------------
✅ Approach 1 (APIView) GET Compiled & Executed.
   Status Code: 200
   Data (Before POST): []

✅ Approach 2 (GenericAPIView) POST Compiled & Executed.
   Status Code: 201
   Response Body (Created Data): {'id': 1, 'amount': '100.00', 'timestamp': '2026-06-07T23:46:00.655187-05:00', 'is_reversed': False, 'account': 1}

✅ Approach 1 (APIView) GET Re-Verification Executed.
   Status Code: 200
   Data (After POST): [{'id': 1, 'amount': '100.00', 'timestamp': '2026-06-07T23:46:00.655187-05:00', 'is_reversed': False, 'account': 1}]

✅ Approach 3 (ModelViewSet) GET/List Compiled & Executed.
   Status Code: 200
   Data (Fetches items existing in DB): [{'id': 1, 'amount': '100.00', 'timestamp': '2026-06-07T23:46:00.655187-05:00', 'is_reversed': False, 'account': 1}]

✅ Approach 3 (ModelViewSet) POST/Create Compiled & Executed.
   Status Code: 201
   Response Body (Created Data): {'id': 2, 'amount': '250.50', 'timestamp': '2026-06-07T23:46:00.665509-05:00', 'is_reversed': False, 'account': 1}

