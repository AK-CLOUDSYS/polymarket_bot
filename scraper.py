import requests

def get_traders():
    url = "https://data-api.polymarket.com/v1/leaderboard"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print("Status: " + str(response.status_code))
        data = response.json()
        if isinstance(data, dict):
            data = data.get("data", [])
        traders = []
        for t in data:
            traders.append({
                "address": t.get("proxyWallet", "unknown"),
                "name": t.get("userName", "unknown"),
                "profit_30d": float(t.get("pnl", 0)),
                "win_rate": float(t.get("percentPositive", 0)),
                "trades_per_day": 1.0,
                "active_positions": int(t.get("positionsOwned", 0)),
                "copiers": int(t.get("followers", 0)),
            })
        print("Got " + str(len(traders)) + " traders!")
        return traders
    except Exception as e:
        print("Error: " + str(e))
        return []
