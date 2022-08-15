from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/new_alarm')
def new_alarm():
    return render_template('new_alarm.html')

if __name__ == '__main__':
    app.run(debug=True)