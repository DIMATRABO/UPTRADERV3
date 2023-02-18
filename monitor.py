import gate_way.kucoin_api as kucoin_api
import math

size=0
precision = 0

def start_monitoring(config_params):


    print("***************************************************")
    print("max prices    :     " + str(config_params["max_price"]))
    print("min prices    :     " + str(config_params["min_price"]))
    prices = kucoin_api.get_prices(config_params["parts"])
    print("current prices:     "+ str(prices))



    for part, price in prices.items():

        #check if the part is already bought
        if not is_bought(part , config_params):
            # Update the minimum price if the current price is lower
            if price < config_params["min_price"][part]:
                config_params["min_price"][part] = price
            # Check if the price has increased by the specified percentage
            if price > config_params["min_price"][part] * (1 + config_params["percent_increase"]/100):
                    print("\t" + part + " price")
                    print("\t" +  str(price) + ">" + str(config_params["min_price"][part]) + "* (1 + "+str(config_params["percent_increase"])+"%)" )
                    # Execute the buy order
                    buyOrder = execute_buy_order(part, price , config_params)
                    if(buyOrder[0] == 200000):
                        print("\t" + "successfully bought")
                        # Set the is_bought to True  and m
                        config_params["is_bought"][part] = True
                        config_params["min_price"][part] = 99999999999


        else: 
            # Update the max price if the current price is higher
            if price > config_params["max_price"][part]:
                config_params["max_price"][part] = price
            # Check if the price has decreased by the specified percentage
            if price < config_params["max_price"][part] * (1 - config_params["percent_decrease"]/100):
                    print("\t" + part + " price")
                    print("\t" +  str(price) + ">" + str(config_params["max_price"][part]) + "* (1 - "+str(config_params["percent_decrease"])+"%)" )
                    # Execute the buy order
                    sellOrder = execute_sell_order(part)
                    if(sellOrder[0] == 200000 or sellOrder[0] == 300000):
                        print("\t" + "successfully selled")
                        # Set is_bought to false and m
                        config_params["is_bought"][part] = False
                        config_params["max_price"][part] = 0

                    
        

def check_funds(part , funds_percentage, price  , currency):

    min_size = kucoin_api.get_base_min_size(part)
    available_funds = kucoin_api.get_available_funds(currency)

    if((available_funds/price) * funds_percentage /100 > min_size and available_funds * funds_percentage /100 > 10 ):
        return True
    else:
        return False



def execute_buy_order(part, price , config_params):
    base_currency = config_params["base_currency"]
    available_funds = kucoin_api.get_available_funds(base_currency)
    funds_percentage =  config_params["funds_percentage"]
    precision = int(kucoin_api.get_precision(part))

    size = (available_funds/price) * funds_percentage /100
    size = size *( 1 - 0.01) # add a margin of error
    size = round(size,precision)

    print("\t available_funds= "+str(available_funds))
    print("\t precision= "+str(precision))
    print("\t size= " + str(size))
    print("\t buying "+ str(size) + " " + str(part))

    response =kucoin_api.execute_buy_order(part, size)
    return float(response["code"]) , size , precision


def execute_sell_order(part):
    base_currency = part.split("-")[0]
    available_funds = kucoin_api.get_available_funds(base_currency)
    precision = int(kucoin_api.get_precision(part))

    size = available_funds - math.pow(10, -precision)
    size = round(size,precision)

    print("\t base_currency= "+ str(base_currency))
    print("\t available_funds= "+str(available_funds))
    print("\t precision= "+str(precision))
    print("\t size= " + str(size))
    print("\t selling  "+ str(size) + " " + str(part))

    response =kucoin_api.execute_sell_order(part, size)
    return float(response["code"]) , size , precision



def set_stop_loss_take_profit(part, price ,config_params , size , precision):
    # Set the stop loss and take profit using the Kucoin API
    #tick_size  = int(kucoin_api.get_tick_size(part.split("-")[0]))
    stop_loss_percentage = config_params["stop_loss_percentage"]
    take_profit_percentage = config_params["take_profit_percentage"]
    stop_loss_price = round(price * ( 1 - stop_loss_percentage/100) , precision ) 
    take_profit_price = round(price * ( 1 +  take_profit_percentage/100) , precision )
    print("\t pricosion= "+str(precision))
    print("\t size= " + str(size))
    print("\t setting  sp to "+ str(stop_loss_price) + "  and tp to " + str(take_profit_price))
    response = kucoin_api.set_stop_loss_take_profit(part, stop_loss_price, take_profit_price , size)
    return float(response["code"]) , response['data']['orderId']
    


def get_price(part):
    return kucoin_api.get_price(part)

def stop_order_open(part, config_params):
    try:
        if(not config_params["stop_order_id"][part] is None):
                order = kucoin_api.get_order_by_id(config_params["stop_order_id"][part])
                if order['data']["status"] == "NEW":
                    return True
        return False
    except:
        return False
    

def is_bought(part , config_params):
    return config_params["is_bought"][part]