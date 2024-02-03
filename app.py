from flask import Flask, render_template, request, url_for, redirect
import firebase_admin
from firebase_admin import db, credentials
from flask_mail import Mail, Message

app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://hap-project-7fa9f-default-rtdb.asia-southeast1.firebasedatabase.app/"})
ref = db.reference("/")

# Flask-Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'gpk2324heartattackprediction@gmail.com'
app.config['MAIL_PASSWORD'] = 'olgh nljx qrjm dsbi'
app.config['MAIL_DEFAULT_SENDER'] = 'gpk2324heartattackprediction@gmail.com'

mail = Mail(app)

@app.route("/")
def show_form():
    return render_template('index.html')
@app.route('/submit_form', methods=['POST'])
def submit_form():
    age = request.form['age']
    sex = request.form['sex']
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang']
    oldpeak = request.form['oldpeak']
    slope = request.form['slope']
    ca = request.form['ca']
    thal = request.form['thal']
    data1={"age": 18, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol, "fbs": fbs,
            "restecg": restecg, "thalach": thalach, "exang": exang, "oldpeak": oldpeak, "slope": slope,
            "ca": ca, "thal": thal}
    last_record = ref.child("Patients").order_by_key().limit_to_last(1).get()
    print(last_record)
    if last_record :
        b=list(last_record.keys())
        last_key =int( b[0])
    else:
        last_key = 0

    data = {"age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol, "fbs": fbs,
            "restecg": restecg, "thalach": thalach, "exang": exang, "oldpeak": oldpeak, "slope": slope,
            "ca": ca, "thal": thal}

    nlast_key=last_key +  1
    ref.child("Patients").child(str(nlast_key)).set(data)



    return render_template('inner-page.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message=request.form['message']

    # Send email
    subject = 'Feedback from {}'.format(name)
    body = 'Name: {}\nEmail: {}\nFeedback: {}\nMessage: {}'.format(name, email, subject, message)
    print(name,email,subject,message)
    msg = Message(subject, recipients=['gpk2324heartattackprediction@gmail.com'], body=body)
    mail.send(msg)

    return render_template('inner-page.html')

if __name__ == '__main__':
    app.run(debug=True)
