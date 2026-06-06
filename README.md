# FGSN Email Campaign Manager

This repository contains an ultra-simple, single-page Python application designed to blast out HTML emails using standard SMTP and CSV spreadsheets.

## 🚀 Quick Start Guide (For Office PC)

Follow these instructions to clone, install, and run the Campaign Manager on any new Windows or Mac computer.

### 1. Prerequisites
Before starting, ensure the new PC has **Python 3** installed. 
You can download it from [python.org/downloads](https://www.python.org/downloads/). (Make sure to check the box that says "Add Python to PATH" during installation).

### 2. Clone the Repository
Open your Terminal or Command Prompt and run:
```bash
git clone https://github.com/KamleshSingh7461/email-py.git
cd "email py"
```

### 3. Create a Virtual Environment (Optional but Recommended)
This keeps your Python packages isolated.
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Required Packages
Install all necessary dependencies (like Flask and Pandas) using the requirements file:
```bash
pip install -r requirements.txt
```

### 6. Run the Server
Start the local dashboard server:
```bash
python app.py
```

### 7. Send Your Campaigns!
1. Open your web browser (Chrome, Edge, Safari).
2. Go to: **http://localhost:5000**
3. Enter your SMTP details (Host, Port, Email, Password).
   > **Note on Passwords**: If using Gmail, you MUST generate an "App Password" from your Google Account Security settings. Your normal login password will not work for SMTP.
4. Upload your `.csv` or `.xlsx` spreadsheet. (Make sure it has a column named `Email`).
5. Paste your HTML code into the template box.
6. Hit **Send Campaign 🚀**.

---

### Variable Replacements
The script automatically replaces variables in your HTML template with data from your spreadsheet rows:
* `$User` -> Replaced with the `First Name` column.
* `[PHONE NUMBER]` -> Replaced with the `Phone` column.
* `{{City}}` -> Replaced with the `City` column (Works for ANY custom column you add!).
