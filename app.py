import os, random
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from database import init_db, insert_log, fetch_logs

app = Flask(__name__)
app.secret_key = "cyber_security_pro_key"
init_db()

# --- PROFESSIONAL ML ENGINE ---
class IntruSenseML:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.train_data = np.array([
            [9, 5, 100, 1], [10, 2, 50, 1], [14, 8, 200, 2], 
            [16, 4, 120, 1], [11, 10, 300, 2], [13, 3, 80, 1]
        ])
        self._pretrain()

    def _pretrain(self):
        scaled_data = self.scaler.fit_transform(self.train_data)
        self.model.fit(scaled_data)

    def analyze(self, features):
        scaled_feature = self.scaler.transform([features])
        prediction = self.model.predict(scaled_feature)
        return "CRITICAL" if prediction[0] == -1 else "NORMAL"

analyzer = IntruSenseML()

# --- USERS ---
USERS = {
    "admin": "admin123",

    "abhinav": "password123",
    "aarav": "password123",
    "nukesh": "password123",
    "aditya": "password123",
    "vihaan": "password123",
    "arjun": "password123",
    "sai": "password123",
    "reyansh": "password123",
    "krishna": "password123",
    "ishaan": "password123",
    "shaun": "password123",
    "rohan": "password123",
    "karan": "password123",
    "yash": "password123",
    "manav": "password123",
    "harsh": "password123",
    "tanish": "password123",
    "dev": "password123",

    "aanya": "password123",
    "ananya": "password123",
    "diya": "password123",
    "saanvi": "password123",
    "riya": "password123",
    "kavya": "password123",
    "radha": "password123",
    "isha": "password123",
    "navya": "password123",
    "priya": "password123",
    "shruti": "password123",
    "pooja": "password123",
    "neha": "password123",
    "nikita": "password123",
    "riddhi": "password123",
    "simran": "password123",
    "kriti": "password123"
}

# --- ROUTES ---
@app.route('/')
def index():
    if 'user' in session:
        return redirect(
            url_for('admin_dash' if session['role'] == 'admin' else 'user_dash')
        )
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username').lower()
        pw = request.form.get('password')
        
        if user in USERS and USERS[user] == pw:
            session.update({
                'user': user,
                'role': 'admin' if user == 'admin' else 'user',
                'name': user.capitalize()
            })

            # --- LOG GENERATION ---
            existing_logs = fetch_logs(user)

            if len(existing_logs) < 7:
                for _ in range(7 - len(existing_logs)):

                    hr = random.randint(0, 23)
                    files = random.randint(1, 20)
                    trans = random.randint(20, 400)
                    dev = random.choice([1, 2])

                    anomaly_score = (files * 0.4 + trans * 0.06)
                    

                    if anomaly_score >= 70:
                        sev = "CRITICAL"
                    elif anomaly_score >= 40:
                        sev = "MEDIUM"
                    else:
                        sev = "NORMAL"

                    score = round(anomaly_score / 10, 2)

                    insert_log((user, hr, files, trans, dev, score, sev))

            return redirect(url_for(
                'admin_dash' if session['role'] == 'admin' else 'user_dash'
            ))

        return "Invalid Credentials. <a href='/login'>Try again</a>"

    # ✅ THIS WAS MISSING
    return render_template('login.html')

@app.route('/admin_dashboard')
def admin_dash():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    rows = fetch_logs()

    # Store latest log for each user
    latest_by_user = {}

    for r in rows:
        username = r[1]
        log_id = r[0]

        current_log = {
            'id': log_id,
            'user': username,
            'time': r[2],
            'files': r[3],
            'transfer': r[4],
            'score': r[6],
            'severity': r[7]
        }

        # Keep only the newest log per user
        if username not in latest_by_user or log_id > latest_by_user[username]['id']:
            latest_by_user[username] = current_log

    # Build final overview list: one entry for every user in USERS
    user_overview = []
    for username in USERS.keys():
        if username in latest_by_user:
            user_overview.append({
                'user': username,
                'time': latest_by_user[username]['time'],
                'files': latest_by_user[username]['files'],
                'transfer': latest_by_user[username]['transfer'],
                'score': latest_by_user[username]['score'],
                'severity': latest_by_user[username]['severity']
            })
        else:
            user_overview.append({
                'user': username,
                'time': '--',
                'files': 0,
                'transfer': 0,
                'score': 0,
                'severity': 'NORMAL'
            })

    # Optional: sort by score descending so risky users appear first
    user_overview.sort(key=lambda x: x['score'], reverse=True)

    return render_template(
        'admin_dashboard.html',
        user_overview=user_overview,
        all_users=USERS.keys()
    )

@app.route('/user_dashboard')
def user_dash():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    rows = fetch_logs(session.get('user'))
    
    logs = []
    for r in rows:
        logs.append({
            'time': r[2],
            'files': r[3],
            'transfer': r[4],
            'score': r[6],
            'severity': r[7]
        })
        
    avg = round(sum(l['score'] for l in logs) / len(logs), 2) if logs else 0
    
    current_risk = "STABLE"
    if logs:
        if logs[0]['severity'] == "CRITICAL":
            current_risk = "HIGH"
        elif logs[0]['severity'] == "MEDIUM":
            current_risk = "MEDIUM"
            
    # --- ALERT GENERATION LOGIC (FIXED INSIDE FUNCTION) ---
    alerts = []

    for log in logs:
        time_str = f"{log['time']:02d}:00"

        if log['severity'] == "CRITICAL":
            alerts.append({
                "level": "HIGH",
                "title": "Rapid activity pattern detected",
                "desc": f"{time_str} - Activity spike detected. {log['transfer']}MB transferred."
            })

            alerts.append({
                "level": "HIGH",
                "title": "Sensitive file access detected",
                "desc": f"{time_str} - {log['files']} files accessed in short time."
            })

            if log['transfer'] > 200:
                alerts.append({
                    "level": "HIGH",
                    "title": "Large data transfer activity detected",
                    "desc": f"{time_str} - {log['transfer']}MB transferred."
                })

        elif log['severity'] == "MEDIUM":
            alerts.append({
                "level": "MEDIUM",
                "title": "Unusual activity pattern observed",
                "desc": f"{time_str} - Higher than normal activity detected."
            })

    return render_template(
        'user_dashboard.html',
        logs=logs,
        avg_score=avg,
        risk_level=current_risk,
        alerts=alerts  
    )

@app.route('/api/stats')
def api_stats():
    rows = fetch_logs()

    if not rows:
        return jsonify({
            "trend_labels": [],
            "trend_scores": [],
            "risk_distribution": [0, 0, 0]
        })

    df = pd.DataFrame(rows, columns=['id', 'u', 't', 'f', 'tr', 'd', 's', 'v'])

    # Sort by ID so older-to-newer flow is stable
    df = df.sort_values('id')

    # Use latest 8 logs only, but keep order stable
    recent = df.tail(8)

    return jsonify({
        "trend_labels": [f"Log {i}" for i in range(1, len(recent) + 1)],
        "trend_scores": recent['s'].tolist(),
        "risk_distribution": [
            len(df[df['v'] == 'NORMAL']),
            len(df[df['v'] == 'MEDIUM']),
            len(df[df['v'] == 'CRITICAL'])
        ]
    })
    
@app.route('/api/analyze_manual', methods=['POST'])
def analyze_manual():
    data = request.json
    feat = [
        int(data['hour']),
        int(data['files']),
        int(data['transfer']),
        int(data['device'])
    ]

    sev = analyzer.analyze(feat)

    anomaly_score = (feat[1] * 0.3 + feat[2] * 0.05) / 10
    score = round(anomaly_score, 2)

    if anomaly_score > 6:
        sev = "CRITICAL"
    elif anomaly_score > 3:
        sev = "MEDIUM"
    else:
        sev = "NORMAL"

    return jsonify({"severity": sev, "score": score})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)