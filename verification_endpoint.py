from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
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

    #Check if signature is valid
    #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
