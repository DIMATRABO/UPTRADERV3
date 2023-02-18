from model.model import *
import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient
import gate_way.kucoin_api as kucoin_api
from gate_way.action.sqlalchimyRepo import SqlAlchimy_repo as actionRepo
from gate_way.dataBaseSession.sessionContext import SessionContext
import math , time

action_repo = actionRepo()
sessionContext = SessionContext()


def save_action(action : Action):
     with sessionContext as session :
        action_repo.save(session=session , action=action)
   


def execute_buy_order(part: Part, price):
    quote_currency = part.symbol.split("-")[1]
    available_funds = kucoin_api.get_available_funds(quote_currency)
    funds_percentage =  part.funds
    precision = int(kucoin_api.get_precision(part.symbol))

    size = (available_funds/price) * funds_percentage /100
    size = size *( 1 - 0.01) # add a margin of error
    size = round(size,precision)

    print("\t available_funds= "+str(available_funds))
    print("\t precision= "+str(precision))
    print("\t size= " + str(size))
    print("\t buying "+ str(size) + " " + str(part.symbol))

    response =kucoin_api.execute_buy_order(part, size)
    return float(response["code"]) , size , precision


def execute_sell_order(part: Part):
    base_currency = part.split("-")[0]
    available_funds = kucoin_api.get_available_funds(base_currency)
    precision = int(kucoin_api.get_precision(part))

    size = available_funds - math.pow(10, -precision)
    size = round(size,precision)

    print("\t base_currency= "+ str(base_currency))
    print("\t available_funds= "+str(available_funds))
    print("\t precision= "+str(precision))
    print("\t size= " + str(size))
    print("\t selling  "+ str(size) + " " + str(part.symbol))

    response =kucoin_api.execute_sell_order(part, size)
    return float(response["code"]) , size , precision




def monitor(part: Part , price ):
    print(part.symbol +' is now  $'+ price +' is bought = ' + str(part.is_bought)+' min : $'+ str(part.min_price) + "  max : $"+ str(part.max_price)+ '  target_min : $'+ str(part.min_price * (1 + part.increase/100)) + "  target_max : $"+ str(part.max_price * (1 - part.decrease/100)))
    price  = float(price)
    
      #check if the part is already bought
    if not part.is_bought:
            # Update the minimum price if the current price is lower
            if price < part.min_price:
                part.min_price = price
            # Check if the price has increased by the specified percentage
            if price > part.min_price * (1 + part.increase/100):
                    # Execute the buy order
                    buyOrder = execute_buy_order(part , price)
                    if(buyOrder[0] == 200000):
                        print("\t" + "successfully bought")
                        save_action( Action(
                             symbol = part.symbol,
                             timestamp=time.time(),
                             direction="BUY",
                             amount=buyOrder[1],
                             price=price
                        ))
                        part.is_bought = True
                        part.min_price = 99999999999
                        part.amount = buyOrder[1]
                        part.buy_price = price
                        return part


    else: 
            # Update the max price if the current price is higher
            if price > part.max_price:
                part.max_price = price
            # Check if the price has decreased by the specified percentage
            if price < part.max_price * (1 - part.decrease/100):
                    print("\t" + part + " price")
                    print("\t" +  str(price) + ">" + str(part.max_price) + "* (1 - "+str(part.decrease)+"%)" )
                    # Execute the buy order
                    sellOrder = execute_sell_order(part)
                    if(sellOrder[0] == 200000 ):
                        print("\t" + "successfully selled")
                        # Set is_bought to false and m
                        save_action( Action(
                             symbol = part.symbol,
                             timestamp=time.time(),
                             direction="SELL",
                             amount=sellOrder[1],
                             price=price,
                             profit_percent= (price - part.buy_price)/price,
                             profit= part.amount * (price - part.buy_price)/price
                        ))
                        part.is_bought = False
                        part.max_price = 0
                        part.amount = None
                        part.buy_price = None
                        return part
    return part

                    

async def getPrices(loop , parts , subscriptionString , stop_event):
    async def deal_msg(msg):
        parts[msg['topic']]  = monitor( parts[msg['topic']] , msg["data"]["price"])
        
    client = WsToken()
    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)
    await ws_client.subscribe('/market/ticker:'+subscriptionString)
    while not stop_event.is_set():
        await asyncio.sleep(6, loop=loop)
  
def start_monitoring(bot , parts , result_queue):
    subscriptionString = ""
    first=True
    for part  in parts.items():
        if first:
            subscriptionString += part[1].symbol
            first = False
        else:
            subscriptionString += ','+part[1].symbol

    print(subscriptionString)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stop_event = asyncio.Event()
    result_queue.put(stop_event)
    loop.run_until_complete(getPrices(loop, parts , subscriptionString, stop_event ))
    
  