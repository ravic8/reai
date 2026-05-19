from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MarketSignal
from app.schemas import MarketSignalCreate


def upsert_market_signals(db: Session, signals: list[MarketSignalCreate]) -> int:
    imported = 0
    for signal in signals:
        existing = db.scalar(select(MarketSignal).where(MarketSignal.locality == signal.locality))
        values = signal.model_dump()
        values["updated_at"] = datetime.utcnow()
        if existing:
            for key, value in values.items():
                setattr(existing, key, value)
        else:
            db.add(MarketSignal(**values))
        imported += 1
    db.commit()
    return imported


def list_market_signals(
    db: Session,
    radius_km: float,
    budget_max: int | None,
) -> list[MarketSignal]:
    query = select(MarketSignal).where(MarketSignal.distance_km <= radius_km)
    if budget_max:
        query = query.where(MarketSignal.avg_price_per_sqft * 1100 <= budget_max)
    return list(db.scalars(query).all())

