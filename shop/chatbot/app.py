from flask import Flask, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/datasource")
def data():
    return render_template('source.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/disclaimer")
def dis():
    return render_template('dis.html')

@app.route("/sms", methods=['POST'])
def sms_reply():
   
    # Fetch the message
    msg = request.form.get('Body')
    phone_no = request.form.get('From')
    reply = fetch_reply(msg, phone_no)

    # Create reply
    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

