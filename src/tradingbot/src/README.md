You need a config.py file that is setup like this:
```
ALPACA_CONFIG = {
    "API_KEY": "INSERT PUBLIC KEY",
    "API_SECRET": "INSERT SECRET KEY",
    # If you want to go live, you must change this. It is currently set for paper trading
    "ENDPOINT": "https://paper-api.alpaca.markets"
}
```