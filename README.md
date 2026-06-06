# FGSN Email Campaign Manager

Welcome! This is a super simple tool that lets you send bulk emails to a list of people using a spreadsheet. You don't need to be a programmer to use it!

---

## 🛠️ How to Setup (Do this once)

### Step 1: Install Python
Your computer needs a free software called **Python** to run this tool.
1. Go to [python.org/downloads](https://www.python.org/downloads/) and click the big yellow "Download Python" button.
2. Open the installer you just downloaded.
3. **CRITICAL:** At the very bottom of the installation screen, check the box that says **"Add Python to PATH"** before you click Install.

### Step 2: Download this Code
1. Scroll to the top of this GitHub page.
2. Click the green **"<> Code"** button.
3. Click **"Download ZIP"**.
4. Extract (unzip) the folder and place it on your Desktop.

### Step 3: Install the Requirements
1. Open your computer's **Terminal** (on Mac) or **Command Prompt** (on Windows).
2. Type `cd Desktop/email-py-main` (or whatever you named the unzipped folder) and press Enter.
3. Type the following command and press Enter:
   ```text
   pip install -r requirements.txt
   ```
   *(This downloads the tiny tools our app needs to run).*

---

## 🚀 How to Run the App (Do this every time you want to send emails)

1. Open your Terminal or Command Prompt.
2. Navigate to the folder where you saved the code (e.g., `cd Desktop/email-py-main`).
3. Type this command and press Enter:
   ```text
   python app.py
   ```
4. Leave that black window open! Now, open your web browser (like Chrome or Edge) and go to:
   **[http://localhost:5000](http://localhost:5000)**

---

## ✉️ How to Use the Dashboard

When you open `http://localhost:5000`, you will see a simple webpage. Here is how to fill it out:

1. **SMTP Settings**: This is how the app logs into your email account to send the messages.
   * **Host:** `smtp.gmail.com` (for Gmail) or your company's SMTP host.
   * **Port:** Usually `587`
   * **Username:** Your email address
   * **Password:** **IMPORTANT FOR GMAIL USERS:** You cannot use your normal password. You must go to your Google Account Security settings, turn on 2-Step Verification, and search for "App Passwords". Generate a 16-letter App Password and paste it here.
2. **Spreadsheet**: Upload your Excel `.xlsx` or `.csv` file. **Make sure one of your column headers is named "Email".**
3. **Template**: Paste your HTML code into the big box. 

### 🌟 Magic Variables
You can make your emails personal! If you put these codes inside your HTML template, the app will automatically replace them for each person:
* Type `$User` in your HTML, and it will be replaced by the person's name (Requires a column named "First Name" in your spreadsheet).
* Type `[PHONE NUMBER]` in your HTML, and it will be replaced by their phone number (Requires a column named "Phone" in your spreadsheet).
* You can do this with **any column!** If you have a column named `City`, just type `{{City}}` in your HTML template!
