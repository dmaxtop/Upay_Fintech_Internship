# **Django Backend & Postman Testing Guide**

## **1\. Starting the Backend Engine**

Open your terminal in the root directory of your project (where manage.py lives) and run the following commands sequentially:

### **Step A: Apply Database Migrations**

_(If changing machines or database files)_ Before launching, ensure your local SQLite schema is completely up to date.


python manage.py migrate

### **Step B: Launch the Local Development Server**

Fire up the local hosting engine. By default, Django maps this to port 8000.

python manage.py runserver

⚠️ **Important:** Keep this terminal window open! If you close it or kill the process using Ctrl + C, your local endpoints will immediately stop responding to Postman.

## **2\. Core Navigation Directory (URLs)**

Once your server reads Starting development server at <http://127.0.0.1:8000/>, use these URL paths to interact with your system layers:

### **The Browser UI Layers**

_(Open directly in Chrome, Edge, or Firefox)_

| **Django Admin Panel**    | <http://127.0.0.1:8000/admin/> | Direct database management dashboard. Log in here first to activate your local session. |

| **Classical Account Hub** | <http://127.0.0.1:8000/api/compare/django/list/> | The server-side rendered HTML template list displaying all current database records.    |

### **The REST API Layers**

_(Best evaluated via Postman)_

| **DRF Account Base**         | <http://127.0.0.1:8000/api/accounts/>               | GET (List all), POST (Create account) 

| **Specific Account Detail**  | <http://127.0.0.1:8000/api/accounts/1/>             | GET (Details), PUT (Replace), PATCH (Modify), DELETE      

| **Custom Action: Freeze**    | <http://127.0.0.1:8000/api/accounts/1/freeze/>      | POST (Toggles target account freeze status)                        |

| **Custom Action: Statement** | <http://127.0.0.1:8000/api/accounts/1/statement/>   | GET (Fetches account details nested with all related ledger lines) |

| **DRF Transaction Base**     | <http://127.0.0.1:8000/api/transactions/>           | GET (List all entries), POST (Deposit/Withdrawal entry)            |

| **Custom Action: Reversal**  | <http://127.0.0.1:8000/api/transactions/1/reverse/> | POST (Rolls back financial amount values safely)  


## **3\. Postman Testing Screenshots**
Navigate to "{base}/Postman_Screenshots" to find the ss

## **4\. Step-by-Step Postman Testing Protocol**

To execute your 19 automated requests cleanly without hitting authentication blockades, follow this workflow:

### **Step 1: Initialize Global Collection Variables**

- Open Postman and select your imported collection: **"Bank Project Complete API Collection"**.
- Click on the **Variables** tab in the main window view.
- Update the **Current Value** column for these keys:
  - **baseUrl**: <http://127.0.0.1:8000>
  - **authUsername**: abcd _(or your configured test username)_
  - **authPassword**: 1234  _(or your configured test password)_
- Click **Save** (Ctrl + S).

### **Step 2: Clear the Classical View CSRF Hurdle**

If you are testing the **Django Template Views** folder and get a 403 Forbidden error:

- Open your browser and navigate to <http://127.0.0.1:8000/api/compare/django/list/>.
- Right-click anywhere -> select **Inspect (F12)** -> Navigate to the **Application** or **Storage** tab.
- Under **Cookies**, select <http://127.0.0.1:8000> and copy the long value string for the csrftoken key.
- Back in Postman's collection variables, paste that string into the **csrfToken** field and save.

### **Step 3: Run and Validate**

Select any target endpoint from your sidebar (e.g., **Get All Accounts**) and hit **Send**. The system handles the authentication handshake automatically behind the scenes, and you will see your formatted database responses return immediately.