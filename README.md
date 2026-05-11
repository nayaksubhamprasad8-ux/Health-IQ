# 🛡️ Health IQ — Health Insurance Comparison System

Health IQ is a web application that helps users browse, compare, and understand Indian health insurance plans. It supports user authentication, plan browsing across 60 plans from 12 insurers, and a side-by-side plan comparison tool.

---

## 📁 Project Structure

```
healthiq/
├── app.py                  # Main Flask application
├── users.json              # Stores registered user accounts
├── Data/
│   └── Health_IQ_60_Pure_Health_Plans_Detailed.csv   # All 60 insurance plans
├── templates/
│   ├── login.html          # Sign in / Sign up page
│   ├── index.html          # Home page
│   ├── plans.html          # Browse all plans
│   └── compare.html        # Side-by-side plan comparison
└── static/
    ├── css/
    │   ├── login.css
    │   ├── index.css
    │   ├── plans.css
    │   └── compare.css
    └── images/
        ├── logo.png
        └── icon.png
```

---

## ⚙️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python, Flask                     |
| Templating| Jinja2 (built into Flask)         |
| Frontend  | HTML5, CSS3                       |
| Data      | CSV file (60 plans), JSON (users) |
| Session   | Flask session (cookie-based)      |

No database, no JavaScript framework, no external services — just Flask.

---

## 🚀 How to Run

**1. Install Flask**
```bash
pip install flask
```

**2. Run the app**
```bash
python app.py
```

**3. Open in browser**
```
http://localhost:5000
```

---

## 🔐 Authentication

- Users can **Sign Up** with name, email, and password
- Credentials are stored in `users.json`
- **Sign In** checks email and password against stored accounts
- Flask `session` keeps the user logged in across pages
- All pages except login redirect to `/login` if not authenticated
- **Logout** clears the session and redirects to login

---

## 📄 Pages & Routes

| Route       | Method | Description                                      |
|-------------|--------|--------------------------------------------------|
| `/`         | GET    | Redirects to home if logged in, else login       |
| `/login`    | GET    | Shows the Sign In / Sign Up page                 |
| `/signin`   | POST   | Validates credentials and starts session         |
| `/signup`   | POST   | Registers new user and starts session            |
| `/logout`   | GET    | Clears session and redirects to login            |
| `/home`     | GET    | Home / landing page                              |
| `/plans`    | GET    | Browse all 60 insurance plans                    |
| `/compare`  | GET    | Side-by-side comparison of 2 or 3 selected plans |

---

## 📊 Plans Data

The CSV file contains **60 health insurance plans** from **12 Indian insurers**:

- Star Health and Allied Insurance
- HDFC ERGO General Insurance
- ICICI Lombard General Insurance
- Bajaj Allianz General Insurance
- Niva Bupa Health Insurance
- Aditya Birla Health Insurance
- Care Health Insurance
- Tata AIG General Insurance
- Reliance General Insurance
- ManipalCigna Health Insurance
- National Insurance Company
- Oriental Insurance Company

**Each plan includes:**

| Field                        | Description                          |
|------------------------------|--------------------------------------|
| Company                      | Insurer name                         |
| Plan_Name                    | Unique plan identifier               |
| Plan_Type                    | Individual / Family / Senior         |
| Annual_Premium               | Yearly cost (₹)                      |
| Monthly_Premium              | Monthly cost (₹)                     |
| Coverage_Limit               | Maximum coverage amount (₹)          |
| Waiting_Period_Years         | Initial waiting period               |
| Claim_Settlement_Ratio_%     | % of claims settled by insurer       |
| Network_Hospitals            | Number of cashless hospitals         |
| Rating                       | Plan rating out of 5                 |
| Reviews_Count                | Number of user reviews               |
| Wellness_Benefit             | Yes / No                             |
| Review_Text                  | Sample user review                   |

---

## 🔍 How Plan Comparison Works

1. On the **Plans** page, tick the checkbox on 2 or 3 plan cards
2. Click **Compare Selected Plans**
3. The selected plan names are sent to `/compare` as query parameters
4. Flask filters the CSV data to find matching plans
5. The **Compare** page renders them in a table, attribute by attribute

> Selecting fewer than 2 or more than 3 plans shows an error message.

---

## 🏷️ Popular Badge Logic

On the Plans page, any plan with a **Rating of 4.5 or above** automatically receives the green **Popular** badge. This is handled dynamically in `plans.html` using Jinja2:

```html
{% if plan.Rating|float >= 4.5 %}
<span class="badge">Popular</span>
{% endif %}
```

---

## 📝 Notes

- Passwords are stored in plain text in `users.json` — this is fine for a college project but should use hashing (e.g. `werkzeug.security`) for production use
- Always run `python app.py` from inside the `healthiq/` folder so relative file paths work correctly
- The app runs in debug mode by default (`debug=True`) — turn this off for any public deployment

---

## 👨‍💻 Developers

**Subham Prasad Nayak**  
**Vishwanath Prasad**  
Health IQ — Insurance Comparison System  
© 2026
