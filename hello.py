from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    if form.validate_on_submit():
        if 'button1' in request.form:
            return 'This thing'
        elif '2' in request.form:
            return 'Other thing'
    return 'Hello, World!'