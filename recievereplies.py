from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid= "AC7a4b5fbc13f00328b31eb600b155eb5d"
auth_token= "85a4fd768eee6bf127e72bdc7d7398ed"

client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    sms_save = open('SMS_MSGS/%s.txt' % number, 'a+')
    sms_save.write('Him: ' + message_body + '\n')
    sms_save.close()
    
    client.messages.create(
         body='Him: ' + message_body + "   Num:" + number + '\n',
         from_='+17752275908',
         to='+17753860663'
     )
     
    print('Him: ' + message_body + "   Num:" + number + '\n')

    resp = MessagingResponse()

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
