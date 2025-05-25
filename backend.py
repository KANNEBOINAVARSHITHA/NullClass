from flask import Flask, request, jsonify
from datetime import date
import sqlite3

app = Flask(_name_)
DB = 'video_platform.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            is_premium INTEGER DEFAULT 0,
            last_download_date TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            video_title TEXT,
            download_url TEXT,
            download_date TEXT
        )''')
        conn.commit()

@app.route('/download_video', methods=['POST'])
def download_video():
    data = request.json
    email = data['email']
    video_title = data['video_title']
    download_url = data['download_url']

    today = str(date.today())

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT id, is_premium, last_download_date FROM users WHERE email=?", (email,))
        user = c.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id, is_premium, last_date = user

        if not is_premium:
            if last_date == today:
                return jsonify({"error": "Free daily download limit reached. Go premium!"}), 403

        c.execute("INSERT INTO downloads (user_id, video_title, download_url, download_date) VALUES (?, ?, ?, ?)",
                  (user_id, video_title, download_url, today))
        if not is_premium:
            c.execute("UPDATE users SET last_download_date=? WHERE id=?", (today, user_id))
        conn.commit()
        return jsonify({"message": "Video downloaded successfully!"})

@app.route('/go_premium', methods=['POST'])
def go_premium():
    # This will simulate a successful Razorpay payment
    email = request.json['email']
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET is_premium=1 WHERE email=?", (email,))
        conn.commit()
    return jsonify({"message": "Premium activated!"})

@app.route('/user_downloads', methods=['GET'])
def user_downloads():
    email = request.args.get('email')
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (email,))
        row = c.fetchone()
        if not row:
            return jsonify({"error": "User not found"}), 404

        user_id = row[0]
        c.execute("SELECT video_title, download_url, download_date FROM downloads WHERE user_id=?", (user_id,))
        downloads = [{"title": t, "url": u, "date": d} for t, u, d in c.fetchall()]
        return jsonify(downloads)

if _name_ == '_main_':
    init_db()
    app.run(debug=True)
