from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from NearMe import find_optimal_pickup
from twilio.rest import Client

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    input_str = request.values.get('Body', None)
    [start, end] = input_str.split(', ')
    msg_response = find_optimal_pickup(start,end)

    # Your Account SID from twilio.com/console
    account_sid = "ACbe7a7135cd5b1675f3cbf8bbd6043e55"
    # Your Auth Token from twilio.com/console
    auth_token  = "49249848da7658be4222e0d06e9221b5"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+15107102674", 
        from_="+13852132901",
        body=msg_response)
    
    # print (msg_response)
    # resp = MessagingResponse()
    # resp.message(msg_response)
    # # resp.message("USPS, Howard Street, South of Market, SF, California, 94104, United States of America")
    # return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

