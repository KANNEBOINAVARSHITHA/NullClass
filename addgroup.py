from flask import Flask, request, jsonify
import sqlite3

app = Flask(_name_)
DB = 'youtube_groups.db'

# Initialize DB
def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        description TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                        group_id INTEGER,
                        user TEXT,
                        FOREIGN KEY(group_id) REFERENCES groups(id)
                    )''')
        conn.commit()

@app.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    name = data['name']
    description = data.get('description', '')
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO groups (name, description) VALUES (?, ?)", (name, description))
            conn.commit()
            return jsonify({'status': 'Group created'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Group already exists'}), 400

@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.json
    group_name = data['group']
    user = data['user']
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM groups WHERE name=?", (group_name,))
        row = c.fetchone()
        if row:
            group_id = row[0]
            c.execute("INSERT INTO group_members (group_id, user) VALUES (?, ?)", (group_id, user))
            conn.commit()
            return jsonify({'status': 'Member added'}), 200
        else:
            return jsonify({'error': 'Group not found'}), 404

@app.route('/search_groups', methods=['GET'])
def search_groups():
    query = request.args.get('q', '')
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT name, description FROM groups WHERE name LIKE ?", ('%' + query + '%',))
        groups = [{'name': row[0], 'description': row[1]} for row in c.fetchall()]
    return jsonify(groups)

if _name_ == '_main_':
    init_db()
    app.run(debug=True)