import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Symbol: {data['s']}, Price: {data['c']}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("WebSocket connection opened")
    # Subscribe to the BTCUSDT ticker stream
    params = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@ticker"
        ],
        "id": 1
    }
    ws.send(json.dumps(params))

if __name__ == "__main__":
    websocket_url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
