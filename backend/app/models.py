from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MarketSignal(Base):
    __tablename__ = "market_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    locality: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    district: Mapped[str] = mapped_column(String(80), default="Hyderabad")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    distance_km: Mapped[float] = mapped_column(Float)
    avg_price_per_sqft: Mapped[int] = mapped_column(Integer)
    price_yoy_pct: Mapped[float] = mapped_column(Float)
    median_rent_2bhk: Mapped[int] = mapped_column(Integer)
    rent_yoy_pct: Mapped[float] = mapped_column(Float)
    inventory_level: Mapped[str] = mapped_column(String(20))
    days_on_market: Mapped[int] = mapped_column(Integer)
    infrastructure_score: Mapped[int] = mapped_column(Integer)
    employment_score: Mapped[int] = mapped_column(Integer)
    risk_score: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(120))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

