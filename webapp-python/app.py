import os
from flask import Flask, render_template
from flask import request
import datetime
import pytz
import socket
from flask_dynamo import Dynamo

from boto3.dynamodb.conditions import Key
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DYNAMO_TABLES'] = [
    {
        "TableName": "chatroom",
        "KeySchema": [
            {
                "KeyType": "HASH",
                "AttributeName": "room_id"
            },
            {
                "KeyType": "RANGE",
                "AttributeName": "time"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "room_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "time",
                "AttributeType": "S"
            }
        ],
        "BillingMode": "PROVISIONED",
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    }
]
dynamo = Dynamo(app)

with app.app_context():
    dynamo.create_all()

# host = os.uname()[1]
host = socket.gethostname() + '-' + socket.gethostbyname(socket.gethostname())


def convertLine(line):
    string = ''
    for item in line:
        string = string + str(item) + " "
    return string


def addItem(room, username, messages, cur_time):
    item = {
        "room_id": room,
        "username": username,
        "message": messages,
        "time": cur_time
    }
    dynamo.tables['chatroom'].put_item(
        Item=item
    )


def readItem(room):
    response = dynamo.tables['chatroom'].query(
        TableName='chatroom',
        KeyConditionExpression=Key("room_id").eq(room),
        # AttributesToGet=[
        #     'time', 'username', 'message'
        # ],
    )
    return response


@app.route("/", methods=['GET'])
def main_page():
    return render_template('index.html')


@app.route("/create", methods=['GET'])
@app.route("/chat/<room>")
def chat_room(room):
    return render_template('index.html')


@app.route("/<room>")
def chat_room2(room):
    return render_template('index.html')


@app.route("/api/chat/<room>", methods=['POST', 'GET'])
def chat(room):
    text_msg = ''
    if request.method == 'POST':

        tz_hcm = pytz.timezone('Asia/Ho_Chi_Minh')
        start_utc = datetime.datetime.now(tz_hcm)

        cur_time = start_utc.strftime("[%Y-%m-%d %H:%M:%S]")
        username = request.form['username']
        messages = request.form['msg']

        addItem(room, username, messages, cur_time)

        return ''

    else:

        text_msg = json.loads(json.dumps(readItem(room)))

        result = 'Load balancing server: ' + host + "\n\n"

        for data_index in range(text_msg['Count']):
            line = text_msg['Items'][data_index]['time'] + ' ' + text_msg['Items'][data_index]['username'] + '\t' + \
                   text_msg['Items'][data_index]['message'] + '\n'
            result = result + line

        return result

if __name__ == "__main__":
    app.run(debug=True)
