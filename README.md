# 🛡️ IntruSense – AI-Based Insider Threat Detection System

IntruSense is an AI-powered cybersecurity system designed to detect insider threats by analyzing user behavior patterns in real time. It leverages anomaly detection techniques to identify suspicious activities and assigns a dynamic Insider Threat Score (ITS) to evaluate risk levels.

---

## 🚀 Project Overview

Insider threats are among the most difficult cybersecurity risks to detect, as they originate from trusted users such as employees. Traditional systems focus on external attacks and often fail to identify abnormal internal behavior.

IntruSense addresses this gap by monitoring user activity, detecting anomalies, and providing actionable insights through interactive dashboards.

---

## 🎯 Key Features

- 🔍 **Behavioral Analysis** – Monitors login time, file access, and data transfer patterns  
- 🧠 **AI-Based Detection** – Uses Isolation Forest for anomaly detection  
- 📊 **Insider Threat Score (ITS)** – Quantifies risk level for each user  
- 🚨 **Real-Time Alerts** – Detects suspicious activities instantly  
- 👥 **User Dashboard** – Personalized activity insights and alerts  
- 🧑‍💼 **Admin Dashboard** – System-wide risk overview, trends, and distribution  
- 📈 **Data Visualization** – Interactive charts using Chart.js  

---

## 🏗️ Tech Stack

**Backend:**
- Python
- Flask
- scikit-learn
- Pandas, NumPy
- SQLite

**Frontend:**
- HTML, CSS, JavaScript
- Chart.js

---

## ⚙️ How It Works

1. User activity data is generated (login time, files accessed, data transfer, etc.)
2. The system analyzes behavior using anomaly detection
3. An Insider Threat Score (ITS) is calculated
4. Users are classified into:
   - **Normal**
   - **Medium**
   - **Critical**
5. Alerts and dashboards visualize the results in real time

---

## 📊 Dashboards

### 👤 User Dashboard
- View personal activity logs  
- Check risk level and ITS score  
- Receive real-time alerts  

### 🧑‍💼 Admin Dashboard
- Monitor all users  
- View system-wide ITS trends  
- Analyze global risk distribution  

---

## ▶️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/IntruSense.git

# Navigate to project folder
cd IntruSense

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

## 📁 Project Structure

IntruSense/
│── app.py
│── database.py
│── requirements.txt
│── static/
│   ├── style.css
│   ├── script.js
│── templates/
│   ├── index.html
│   ├── login.html
│   ├── user_dashboard.html
│   ├── admin_dashboard.html
│── assets/ (screenshots)
│── README.md
│── .gitignore
