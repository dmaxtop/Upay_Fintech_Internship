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

