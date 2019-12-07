import json
import requests
from requests.exceptions import HTTPError

class BitcoinRequest(object):
    """
    Bitcoin API
    """

    def __init__(self):
        pass

    def _request(self, command, params):
        try:           
            headers = {'content-type': 'text/plain;',}
            params_ = []
            for par in params:
                if isinstance(par, str):
                    params_.append('"' + par + '"')
                    # print(par)
                if isinstance(par, bool):
                    params_.append(str(par).lower())
                if isinstance(par, int):
                    params_.append(str(par))
                if isinstance(par, float):
                    params_.append(str(par))

            data = '{"jsonrpc": "1.0", "id":"curltest", "method": "' + command + '", "params": [' + ','.join(params_) + '] }'
            response = requests.post('http://45.77.36.113:8332/', headers=headers, data=data, auth=('user', 'password'))
            
            json_data = json.loads(response.text)
            return json_data

        except HTTPError as err:
            print(err)

    def validate(self, address):
        json_data = self._request('getaddressinfo', [address])
        result = json_data['result']
        if result:
            return True
        return False

    def post(self, command, params):
        return self._request(command, params)

    def _getlabelbyaddress(self, address):
        json_data = self._request('getaddressinfo', [address])
        result = json_data['result']
        return result['label']

    def _gettransactionslistbylabel(self, label):
        transactions_list = []
        json_data = self._request('listtransactions', [label])
        result = json_data['result']
        def is_not_coinbase_tx(tx):
            return tx['category'] == 'send' or tx['category'] == 'receive'
        def get_transactionid(tx):
            return tx['txid']
        result = list(filter(is_not_coinbase_tx, result))
        result = list(map(get_transactionid, result))
        return result
    
    def gettransactionslistbyaddress(self, address):
        label = self._getlabelbyaddress(address)
        return self._gettransactionslistbylabel(label)
    
    def getconfirmedtransaction(self, txid):
        json_data = self._request('getrawtransaction', [txid, True])
        result = json_data['result']
        return result
