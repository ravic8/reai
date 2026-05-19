from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.models import MarketSignal
from app.repository import list_market_signals, upsert_market_signals
from app.schemas import MarketSignalOut, RefreshRequest, RefreshResponse
from app.scrapers.html_table import HtmlTableTrendCollector
from app.scrapers.seed import SeedTrendCollector
from app.services.scoring import gross_yield_pct, investment_score, risk_flags, thesis

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_market_out(signal: MarketSignal, strategy: str) -> MarketSignalOut:
    return MarketSignalOut(
        id=signal.id,
        locality=signal.locality,
        district=signal.district,
        latitude=signal.latitude,
        longitude=signal.longitude,
        distance_km=signal.distance_km,
        avg_price_per_sqft=signal.avg_price_per_sqft,
        price_yoy_pct=signal.price_yoy_pct,
        median_rent_2bhk=signal.median_rent_2bhk,
        rent_yoy_pct=signal.rent_yoy_pct,
        inventory_level=signal.inventory_level,
        days_on_market=signal.days_on_market,
        infrastructure_score=signal.infrastructure_score,
        employment_score=signal.employment_score,
        risk_score=signal.risk_score,
        source=signal.source,
        updated_at=signal.updated_at,
        investment_score=investment_score(signal, strategy),
        gross_yield_pct=gross_yield_pct(signal),
        strategy_fit=strategy,
        thesis=thesis(signal, strategy),
        risk_flags=risk_flags(signal),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/refresh", response_model=RefreshResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> RefreshResponse:
    if payload.source == "seed":
        collector = SeedTrendCollector()
    elif payload.source == "html_table" and payload.url:
        collector = HtmlTableTrendCollector(payload.url)
    else:
        raise HTTPException(status_code=400, detail="Use source='seed' or source='html_table' with url")

    imported = upsert_market_signals(db, collector.collect())
    return RefreshResponse(imported=imported, source=payload.source)


@app.get("/api/markets", response_model=list[MarketSignalOut])
def markets(
    db: Session = Depends(get_db),
    radius_km: float = Query(default=50, le=50, ge=1),
    strategy: str = Query(default="balanced"),
    budget_max: int | None = Query(default=None, ge=1000000),
) -> list[MarketSignalOut]:
    if not list_market_signals(db, radius_km, None):
        upsert_market_signals(db, SeedTrendCollector().collect())

    signals = list_market_signals(db, radius_km, budget_max)
    ranked = sorted(signals, key=lambda item: investment_score(item, strategy), reverse=True)
    return [to_market_out(signal, strategy) for signal in ranked]


@app.get("/api/markets/{market_id}", response_model=MarketSignalOut)
def market_detail(
    market_id: int,
    db: Session = Depends(get_db),
    strategy: str = Query(default="balanced"),
) -> MarketSignalOut:
    signal = db.get(MarketSignal, market_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Market not found")
    return to_market_out(signal, strategy)

