from datetime import datetime

from pydantic import BaseModel, Field


class MarketSignalBase(BaseModel):
    locality: str
    district: str = "Hyderabad"
    latitude: float
    longitude: float
    distance_km: float
    avg_price_per_sqft: int
    price_yoy_pct: float
    median_rent_2bhk: int
    rent_yoy_pct: float
    inventory_level: str
    days_on_market: int
    infrastructure_score: int = Field(ge=0, le=100)
    employment_score: int = Field(ge=0, le=100)
    risk_score: int = Field(ge=0, le=100)
    source: str


class MarketSignalCreate(MarketSignalBase):
    pass


class MarketSignalOut(MarketSignalBase):
    id: int
    investment_score: int
    gross_yield_pct: float
    strategy_fit: str
    thesis: str
    risk_flags: list[str]
    updated_at: datetime

    class Config:
        from_attributes = True


class RefreshRequest(BaseModel):
    source: str = "seed"
    url: str | None = None


class RefreshResponse(BaseModel):
    imported: int
    source: str

