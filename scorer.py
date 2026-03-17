from config import MAX_ACTIVE_POSITIONS, MAX_TRADES_PER_DAY, MIN_TRADES_PER_DAY, MAX_COPIERS, TOP_N_WALLETS

def filter_traders(traders):
    filtered = []
    for t in traders:
        if t["active_positions"] > MAX_ACTIVE_POSITIONS:
            continue
        if t["trades_per_day"] > MAX_TRADES_PER_DAY:
            continue
        if t["trades_per_day"] < MIN_TRADES_PER_DAY:
            continue
        if t["copiers"] >= MAX_COPIERS:
            continue
        filtered.append(t)
    return filtered

def score_traders(traders):
    if not traders:
        return []
    max_profit = max(t["profit_30d"] for t in traders) or 1
    for t in traders:
        win_score = t["win_rate"] * 0.40
        consistency_score = min(t["trades_per_day"] / 10, 1) * 25
        copier_score = ((MAX_COPIERS - t["copiers"]) / MAX_COPIERS) * 20
        profit_score = (t["profit_30d"] / max_profit) * 15
        t["score"] = round(win_score + consistency_score + copier_score + profit_score, 1)
    ranked = sorted(traders, key=lambda x: x["score"], reverse=True)
    return ranked[:TOP_N_WALLETS]
