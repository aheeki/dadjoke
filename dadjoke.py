from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def dadjoke_ready(): 
    resp = twilio.twiml.Response()
    resp.message("Daddys Home")
    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
