import requests,  time, base64 , hmac , hashlib, json , logging , string , random , math


# Kucoin API endpoint for retrieving prices
PRICE_ENDPOINT = "https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol="

# Kucoin API endpoint for executing buy orders
BUY_ENDPOINT = "https://api.kucoin.com/api/v1/orders"

# Kucoin API endpoint for setting stop loss and take profit orders
STOP_LOSS_TAKE_PROFIT_ENDPOINT = "https://api.kucoin.com/api/v1/stop-order"

# Replace with your Kucoin API key
API_KEY = "63c7bec54891260001af322f"

# Replace with your Kucoin API secret
API_SECRET = "0b6f2cf5-153c-4b86-878f-9814ee7cde1d"

# Replace with your Kucoin API passphrase
API_PASSPHRASE = "uptrader"





def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



def get_price(symbol):
    endpoint = "https://api.kucoin.com/api/v1/market/orderbook/level2_20"
    params = {'symbol': symbol}
    response = requests.get(endpoint, params=params)
    data = json.loads(response.text)
    return float(data['data']['bids'][0][0])

def get_prices(parts):
    prices = {}
    for part in parts:
        prices[part] = get_price(part)
    return prices


def execute_buy_order(symbol , size ):

    # Configure logging
    logging.basicConfig(filename='logs/'+symbol+'.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)



    url = 'https://api.kucoin.com/api/v1/orders'
    now = int(time.time() * 1000)
            
    data = {
            "clientOid":"uniqueuuid" + get_random_string(8),
            "side":"buy",
            "symbol":symbol,
            "type":"market",
            "size": str(size)
            }
        

    data_json = json.dumps(data)
    str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
                    "KC-API-SIGN": signature,
                    "KC-API-TIMESTAMP": str(now),
                    "KC-API-KEY": API_KEY,
                    "KC-API-PASSPHRASE": passphrase,
                    "KC-API-KEY-VERSION": "2",
                    "Content-Type": "application/json" # specifying content type or using json=data in request
                    }

    try:
                response = requests.request('post', url, headers=headers, data=data_json)
                code = float(response.json()["code"])
                print(response.json())
                if(code == 200000):
                    logging.info("buying "+str(size)+symbol+" succesfully") 
                else:
                    logging.info("buying "+str(size)+symbol+" failed " + response.json()) 
                
    except requests.exceptions.RequestException as e: 
                logging.error(response.json()) 
    finally:
        return response.json()



def execute_sell_order(symbol , size ):
    # Configure logging
    logging.basicConfig(filename='logs/'+symbol+'.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

    url = 'https://api.kucoin.com/api/v1/orders'
    now = int(time.time() * 1000)
            
    data = {
            "clientOid":"uniqueuuid" + get_random_string(8),
            "side":"sell",
            "symbol":symbol,
            "type":"market",
            "size": str(size)
            }
        

    data_json = json.dumps(data)
    str_to_sign = str(now) + 'POST' + '/api/v1/orders' + data_json
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
                    "KC-API-SIGN": signature,
                    "KC-API-TIMESTAMP": str(now),
                    "KC-API-KEY": API_KEY,
                    "KC-API-PASSPHRASE": passphrase,
                    "KC-API-KEY-VERSION": "2",
                    "Content-Type": "application/json" # specifying content type or using json=data in request
                    }

    try:
                response = requests.request('post', url, headers=headers, data=data_json)
                code = float(response.json()["code"])
                print(response.json())
                if(code == 200000):
                    logging.info("selling "+str(size)+symbol+" succesfully") 
                else:
                    logging.info("selling "+str(size)+symbol+" failed " + response.json()) 
                
    except requests.exceptions.RequestException as e: 
                logging.info(response.json()) 
    finally:
        return response.json()



def set_stop_loss_take_profit(symbol , stop_loss_price, take_profit_price , size):
    logging.basicConfig(filename='logs/'+symbol+'.log', level=logging.INFO)
    url = 'https://api.kucoin.com/api/v1/stop-order'
    now = int(time.time() * 1000)
            
    data = {
            "clientOid":"uniqueuuid"+get_random_string(8),
            "side":"sell",
            "symbol":symbol,
            "type":"limit",
            "stop":"loss",
            "stopPrice": str(stop_loss_price),
            "price": str(take_profit_price), 
            "size": str(size)
            }
        

    data_json = json.dumps(data)
    str_to_sign = str(now) + 'POST' + '/api/v1/stop-order' + data_json
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
                    "KC-API-SIGN": signature,
                    "KC-API-TIMESTAMP": str(now),
                    "KC-API-KEY": API_KEY,
                    "KC-API-PASSPHRASE": passphrase,
                    "KC-API-KEY-VERSION": "2",
                    "Content-Type": "application/json" # specifying content type or using json=data in request
                    }

    try:
                response = requests.request('post', url, headers=headers, data=data_json)
                code = float(response.json()["code"])
                print(response.json())
                if(code == 200000):
                    logging.info(response.json()) 
                else:
                    logging.info(response.json()) 
                
    except requests.exceptions.RequestException as e: 
                logging.info(response.json()) 
    finally:
        return response.json()





def get_available_funds(currency):
    endpoint = "https://api.kucoin.com/api/v1/accounts"
    now = int(time.time() * 1000)
    data = {"type" : "trade" , "currency": currency}
    data_json = json.dumps(data)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts' + data_json
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
            }
    response = requests.request('get', endpoint, headers=headers, data=data_json)
    data = json.loads(response.text)['data']
    for account in data:
        if account['currency'] == currency:
            return float(account['balance'])
    return None


def get_tick_size(currency):
    endpoint = "https://api.kucoin.com/api/v1/currencies/"+currency
    response = requests.get(endpoint)
    data = json.loads(response.text)
    return int(data['data']["precision"])
    

def get_precision(symbol):
    endpoint = "https://api.kucoin.com/api/v1/symbols?symbol="+symbol
    response = requests.get(endpoint)
    data = json.loads(response.text)
    for account in data['data']:
        if account['symbol'] == symbol:
            print(account['baseIncrement'])
            return -math.log10(float(account['baseIncrement']))
    return None


def get_base_min_size(symbol):
     endpoint = "https://api.kucoin.com/api/v1/symbols="+symbol
     response = requests.get(endpoint)
     data = json.loads(response.text)
     for symbil_data  in data['data']:
        if symbil_data['symbol'] == symbol:
            return float(symbil_data['baseMinSize'])
     return None

 
def get_klines(symbol , type, startAt , endAt):
    endpoint = f"https://api.kucoin.com/api/v1/market/candles?type={type}&symbol={symbol}&startAt={startAt}&endAt={endAt}"
    response = requests.get(endpoint)
    data = json.loads(response.text)
    return data


def get_stop_orders():
    endpoint = f"https://api.kucoin.com/api/v1/stop-order"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/stop-order'
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
            }
    response =  requests.request('get', endpoint, headers=headers)
    data = json.loads(response.text)
    return data
   

def get_order_by_id(id):
    endpoint = f"https://api.kucoin.com/api/v1/stop-order/{id}"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/stop-order/' + id
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
            }
    response =  requests.request('get', endpoint, headers=headers)
    data = json.loads(response.text)
    return data

def get_symbols():
    endpoint = f"https://api.kucoin.com/api/v1/symbols"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/symbols'
    signature = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(API_SECRET.encode('utf-8'), API_PASSPHRASE.encode('utf-8'), hashlib.sha256).digest())
    headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": API_KEY,
            "KC-API-PASSPHRASE": passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json" # specifying content type or using json=data in request
            }
    response =  requests.request('get', endpoint, headers=headers)
    data = json.loads(response.text)
    return data

