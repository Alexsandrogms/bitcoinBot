import ssl
import json

import websocket
import bitstamp.client 
import credentials


def client():
    return bitstamp.client.trading(username=credentials.USERNAME, Key=credentials.KEY, secret=credentials.SECRET)


def buy(amount): # Função vender bitcoin 'sell' = 'vender'
    trading_client =  client()
    trading_client.buy_market_order(amount)


def sell(amount): # Função comprar bitcoin 'purchase' = 'comprar'
    trading_client = client()
    trading_client.sell_market_order(amount)


def open_conx(ws): # Funçâo para abrir conexâo
    print('initiating connection...')
    subscriptions_json = """
    {
        "event": "bts:subscribe",
        "data": {
            "channel":"live_trades_btcusd"
        }
    }
    """
    ws.send(subscriptions_json)


def exit_conx(ws): # Função para fechar conexâo
    print('terminating connection...')


def receive_msg(ws, msg): # Função para receber mensagem
    msg = json.loads(msg)
    price = msg['data']['price']
    print(f'dollar price $: {price}')

    if price > 9000:
        sell()

    elif price < 8000:
        purchase()

    else:
        print('Loading...')


def error_conx(ws, error): # Função para mostrar os erros 
    print('Error establishing connection')
    print(error)


if __name__ == '__main__': # Programa principal
    ws = websocket.WebSocketApp ("wss://ws.bitstamp.net",
                                 on_open=open_conx,
                                 on_close=exit_conx,
                                 on_error=error_conx,
                                 on_message=receive_msg)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
