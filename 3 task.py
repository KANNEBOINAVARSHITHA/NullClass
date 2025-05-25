from flask import Flask, request, jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(_name_)
DB = 'video_platform.db'

PLAN_DETAILS = {
    "Free": {"minutes": 5, "price": 0},
    "Bronze": {"minutes": 7, "price": 10},
    "Silver": {"minutes": 10, "price": 50},
    "Gold": {"minutes": -1, "price": 100}  # -1 means unlimited
}

# Trigger email with invoice
def send_invoice_email(email, plan, amount):
    msg = MIMEText(f"Thank you for purchasing the {plan} plan.\n\nAmount Paid: ₹{amount}\nEnjoy watching videos for {PLAN_DETAILS[plan]['minutes']} minutes per video.\n\n- Team YouTube Clone")
    msg['Subject'] = f'Invoice - {plan} Plan'
    msg['From'] = 'your-email@example.com'
    msg['To'] = email

    # Setup SMTP server (Use a test SMTP like Mailtrap, Gmail or SendGrid)
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # replace with actual SMTP
        server.starttls()
        server.login("your-email@example.com", "your-password")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.quit()
        print("Invoice email sent!")
    except Exception as e:
        print("Email failed:", e)

# API to upgrade plan
@app.route('/upgrade_plan', methods=['POST'])
def upgrade_plan():
    data = request.json
    email = data['email']
    plan = data['plan']
    
    if plan not in PLAN_DETAILS or PLAN_DETAILS[plan]['price'] == 0:
        return jsonify({"error": "Invalid plan selected"}), 400

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET plan=? WHERE email=?", (plan, email))
        conn.commit()
    
    send_invoice_email(email, plan, PLAN_DETAILS[plan]['price'])
    return jsonify({"message": f"Plan upgraded to {plan}"}), 200

# API to get watch limit
@app.route('/get_watch_limit', methods=['GET'])
def get_watch_limit():
    email = request.args.get('email')
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT plan FROM users WHERE email=?", (email,))
        row = c.fetchone()
        if not row:
            return jsonify({"error": "User not found"}), 404
        plan = row[0]
        return jsonify({
            "plan": plan,
            "watch_limit_minutes": PLAN_DETAILS[plan]['minutes']
        })

if _name_ == '_main_':
    app.run(debug=True)
