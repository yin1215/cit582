from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine, select, MetaData, Table
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only

from models import Base, Order, Log

engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)


# These decorators allow you to use g.session to access the database inside the request code
@app.before_request
def create_session():
    g.session = scoped_session(
        DBSession)  # g is an "application global" https://flask.palletsprojects.com/en/1.1.x/api/#application-globals


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    g.session.commit()
    g.session.remove()


"""
-------- Helper methods (feel free to add your own!) -------
"""


def log_message(d):
    # Takes input dictionary d and writes it to the Log table
    msg = json.dumps(d)
    msg_obj = Log(message=msg)
    g.session.add(msg_obj)
    g.session.commit()


def verify(content):
    sig = content['sig']
    payload = content['payload']
    message = payload['message']
    pk = payload['pk']
    platform = payload['platform']

    if platform == 'Ethereum':

        eth_encoded_msg = eth_account.messages.encode_defunct(text=message)
        sig_eth = hex(int(sig, 16))

        if eth_account.Account.recover_message(eth_encoded_msg, signature=sig_eth) == pk:
            result = True
        else:
            result = False

    else:
        if algosdk.util.verify_bytes(message.encode('utf-8'), sig, pk):
            result = True
        else:
            result = False

    return result
"""
---------------- Endpoints ----------------
"""


@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print(f"content = {json.dumps(content)}")
        columns = ["sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform"]
        fields = ["sig", "payload"]
        error = False
        for field in fields:
            if not field in content.keys():
                print(f"{field} not received by Trade")
                print(json.dumps(content))
                log_message(content)
                return jsonify(False)

        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print(f"{column} not received by Trade")
                error = True
        if error:
            print(json.dumps(content))
            log_message(content)
            return jsonify(False)

        # Your code here
        # Note that you can access the database session using g.session
        payload = content['payload']

        fields = ["sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "signature"]
        if verify(content):
            order = {}
            order['signature'] = content['sig']
            order['sender_pk'] = payload['sender_pk']
            order['receiver_pk'] = payload['receiver_pk']
            order['buy_currency'] = payload['buy_currency']
            order['sell_currency'] = payload['sell_currency']
            order['buy_amount'] = payload['buy_amount']
            order['sell_amount'] = payload['sell_amount']
            order_obj = Order(**{f: order[f] for f in fields})
            g.session.add(order_obj)
            g.session.commit()
        else:
            log_message(payload)



@app.route('/order_book')
def order_book():
    # Your code here
    # Note that you can access the database session using g.session
    data = []
    for order in g.session.query(Order):
        content = {}
        content['sender_pk'] = order.sender_pk
        content['receiver_pk'] = order.receiver_pk
        content['buy_currency'] = order.buy_currency
        content['sell_currency'] = order.sell_currency
        content['buy_amount'] = order.buy_amount
        content['sell_amount'] = order.sell_amount
        content['signature'] = order.signature

        data.append(content)

    result = {}
    result['data'] = data
    return jsonify(result)


if __name__ == '__main__':
    app.run(port='5002')
