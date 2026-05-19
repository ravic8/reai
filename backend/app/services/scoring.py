from app.models import MarketSignal


STRATEGY_LABELS = {
    "balanced": "Balanced",
    "rental_income": "Rental income",
    "appreciation": "Appreciation",
    "low_risk": "Lower risk",
}


def gross_yield_pct(signal: MarketSignal) -> float:
    estimated_2bhk_size_sqft = 1100
    estimated_price = signal.avg_price_per_sqft * estimated_2bhk_size_sqft
    annual_rent = signal.median_rent_2bhk * 12
    return round((annual_rent / estimated_price) * 100, 2)


def investment_score(signal: MarketSignal, strategy: str = "balanced") -> int:
    price_momentum = min(max(signal.price_yoy_pct * 6, 0), 100)
    rent_momentum = min(max(signal.rent_yoy_pct * 7, 0), 100)
    yield_score = min(gross_yield_pct(signal) * 13, 100)
    liquidity_score = max(100 - signal.days_on_market, 10)
    supply_score = {"low": 82, "medium": 62, "high": 42}.get(signal.inventory_level.lower(), 55)

    weights = {
        "balanced": (0.22, 0.18, 0.18, 0.15, 0.12, 0.15),
        "rental_income": (0.12, 0.30, 0.24, 0.10, 0.09, 0.15),
        "appreciation": (0.34, 0.10, 0.10, 0.18, 0.13, 0.15),
        "low_risk": (0.12, 0.14, 0.16, 0.12, 0.16, 0.30),
    }.get(strategy, (0.22, 0.18, 0.18, 0.15, 0.12, 0.15))

    risk_adjusted = 100 - signal.risk_score
    raw = (
        price_momentum * weights[0]
        + yield_score * weights[1]
        + rent_momentum * weights[2]
        + signal.infrastructure_score * weights[3]
        + signal.employment_score * weights[4]
        + risk_adjusted * weights[5]
    )
    raw = raw * 0.85 + liquidity_score * 0.08 + supply_score * 0.07
    return round(min(max(raw, 0), 100))


def risk_flags(signal: MarketSignal) -> list[str]:
    flags: list[str] = []
    if signal.risk_score >= 65:
        flags.append("Elevated execution or livability risk")
    if signal.inventory_level.lower() == "high":
        flags.append("Higher supply could limit near-term price growth")
    if signal.days_on_market > 55:
        flags.append("Slower liquidity than stronger Hyderabad submarkets")
    if signal.avg_price_per_sqft > 10500:
        flags.append("Entry price is high, underwriting needs conservative rent assumptions")
    if not flags:
        flags.append("No major risk signal from current model inputs")
    return flags


def thesis(signal: MarketSignal, strategy: str = "balanced") -> str:
    fit = STRATEGY_LABELS.get(strategy, "Balanced")
    yield_value = gross_yield_pct(signal)
    score = investment_score(signal, strategy)
    return (
        f"{signal.locality} scores {score}/100 for {fit.lower()} investing. "
        f"The model sees {signal.price_yoy_pct:.1f}% price momentum, "
        f"{signal.rent_yoy_pct:.1f}% rent momentum, and an estimated gross yield of "
        f"{yield_value:.2f}% based on a representative 2BHK."
    )

