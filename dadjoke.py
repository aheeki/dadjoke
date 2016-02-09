import twilio.twiml, json
from random import randint
from flask import Flask, request, redirect

app = Flask(__name__)

# cue the deer
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)


@app.route("/", methods=['GET', 'POST'])
def dadjoke_ready(): 
    resp = twilio.twiml.Response()
    resp.message(jokes[randint(0,len(jokes)-1)])
    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
