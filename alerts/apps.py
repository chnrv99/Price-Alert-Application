# alerts/apps.py

from django.apps import AppConfig
import threading
import websocket
import json

class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'

    def ready(self):
        from alerts.models import TargetPriceOfCoin
        from alerts.tasks import trigger_alert
        def on_message(ws, message):
            data = json.loads(message)
            symbol = data['s']
            price = float(data['c'])
            print(f"Symbol: {symbol}, Price: {price}")

            # Check against target prices
            target_prices = TargetPriceOfCoin.objects.filter(coin=symbol)
            for target in target_prices:
                if price <= target.target_price:
                    # Trigger alert
                    trigger_alert.delay(target.user.email, symbol, price)

        def on_error(ws, error):
            print(f"Error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            print("WebSocket connection opened")
            params = {
                "method": "SUBSCRIBE",
                "params": [
                    "btcusdt@ticker"
                ],
                "id": 1
            }
            ws.send(json.dumps(params))

        def start_websocket():
            websocket_url = "wss://stream.binance.com:9443/ws"
            ws = websocket.WebSocketApp(websocket_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open
            ws.run_forever()

        thread = threading.Thread(target=start_websocket)
        thread.start()
