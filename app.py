import json
import urllib2
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "SNS requests listener!"

@app.route("/notification_listener", methods=['POST'])
def notification_listener():
    request_data = json.loads(request.data)
    request_type = request_data['Type']
    if request_type == 'SubscriptionConfirmation':
        if request_data['SubscribeURL']:
            confirm_subscription(request_data['SubscribeURL'])
        else:
            return 'Bad request', 400
    elif request_type == 'UnsubscribeConfirmation':
        print_request(request_data)
    elif request_type == 'Notification':
        print_request(request_data)
    else:
        print('Bad request')
        print_request(request_data)
        return 'Bad request', 400
    return 'OK', 200

@app.before_request
def log_request():
    print request.headers

def confirm_subscription(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        print("Confirming subscription...")
        print(html)
    except urllib2.HTTPError as e:
        print(e.code)

def print_request(request_data):
    for key, value in request_data.iteritems():
        print('%s: %s' % (key, value))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)
