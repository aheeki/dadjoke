import twilio.twiml, json
from random import randint
from flask import Flask, request, redirect

app = Flask(__name__)

# cue the deer
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)


@app.route("/", methods=['GET', 'POST'])
def dadjoke_ready():

    txt = request.values.get('Body').lower()
    dad_joke = ['dad joke', 'dadjoke', 'dad-joke']
    #if txt is received asking for a dad joke
    if any(x in txt for x in dad_joke):
        resp = twilio.twiml.Response()
        resp.sms(jokes[randint(0,len(jokes)-1)])
        return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
