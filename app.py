from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store weekly logs in memory
weekly_logs = []

# Simple burnout prediction
def predict_burnout(logs):
    if not logs:
        return "No data yet"
    
    avg_sleep = sum([entry['sleep'] for entry in logs]) / len(logs)
    avg_physical = sum([entry['physical'] for entry in logs]) / len(logs)
    avg_study = sum([entry['study'] for entry in logs]) / len(logs)
    
    score = (avg_sleep * 0.4 + avg_physical * 0.3 + avg_study * 0.3)
    
    if score < 50:
        return "High Risk of Burnout"
    elif score < 75:
        return "Moderate Risk"
    else:
        return "Low Risk"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        sleep = float(request.form.get('sleep', 0))
        physical = float(request.form.get('physical', 0))
        study = float(request.form.get('study', 0))
        
        weekly_logs.append({
            'date': date,
            'sleep': sleep,
            'physical': physical,
            'study': study
        })
        return redirect(url_for('index'))
    
    prediction = predict_burnout(weekly_logs)
    return render_template('index.html', logs=weekly_logs, prediction=prediction)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
