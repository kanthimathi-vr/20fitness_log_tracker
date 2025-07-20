from flask import Flask, render_template, request, redirect, url_for, abort
import uuid
from datetime import datetime

app = Flask(__name__)

# In-memory workout logs
logs = []

@app.route('/')
def home():
    dates = sorted({log['date'] for log in logs}, reverse=True)
    selected_date = request.args.get('date')
    if selected_date:
        filtered = [l for l in logs if l['date'] == selected_date]
    else:
        filtered = logs
    return render_template('home.html', logs=filtered, dates=dates, selected_date=selected_date)

@app.route('/add', methods=['POST'])
def add_log():
    date = request.form['date']
    wtype = request.form['type']
    duration = request.form['duration']
    notes = request.form['notes']

    entry = {
        'id': str(uuid.uuid4()),
        'date': date,
        'type': wtype,
        'duration': duration,
        'notes': notes
    }
    logs.append(entry)
    return redirect(url_for('home', date=date))

@app.route('/log/<log_id>')
def log_detail(log_id):
    entry = next((l for l in logs if l['id'] == log_id), None)
    if not entry:
        abort(404)
    return render_template('log_detail.html', log=entry)

if __name__ == '__main__':
    app.run(debug=True)
