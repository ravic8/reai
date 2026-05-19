"use client";

import { useEffect, useMemo, useState } from "react";
import { Building2, IndianRupee, MapPin, RefreshCw, Search, ShieldAlert, TrendingUp } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchMarkets, refreshSeedData, type Market } from "../lib/api";

const strategies = [
  { value: "balanced", label: "Balanced" },
  { value: "rental_income", label: "Rental" },
  { value: "appreciation", label: "Growth" },
  { value: "low_risk", label: "Low risk" },
];

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export default function Home() {
  const [strategy, setStrategy] = useState("balanced");
  const [budget, setBudget] = useState("9000000");
  const [markets, setMarkets] = useState<Market[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadMarkets() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchMarkets(strategy, Number(budget));
      setMarkets(data);
      setSelectedId((current) => current ?? data[0]?.id ?? null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMarkets();
  }, [strategy]);

  const selected = useMemo(
    () => markets.find((market) => market.id === selectedId) ?? markets[0],
    [markets, selectedId],
  );

  const chartData = markets.slice(0, 8).map((market) => ({
    locality: market.locality,
    score: market.investment_score,
    yield: market.gross_yield_pct,
  }));

  const mapBounds = {
    minLat: 17.18,
    maxLat: 17.58,
    minLng: 78.22,
    maxLng: 78.58,
  };

  return (
    <main>
      <section className="topbar">
        <div>
          <div className="brand">
            <Building2 size={24} />
            <span>RILL</span>
          </div>
          <h1>Hyderabad 50 km investment radar</h1>
        </div>
        <button
          className="iconButton"
          type="button"
          title="Refresh market signals"
          onClick={async () => {
            await refreshSeedData();
            await loadMarkets();
          }}
        >
          <RefreshCw size={18} />
        </button>
      </section>

      <section className="controls">
        <div className="field">
          <label>Strategy</label>
          <div className="segments">
            {strategies.map((item) => (
              <button
                key={item.value}
                type="button"
                className={strategy === item.value ? "active" : ""}
                onClick={() => setStrategy(item.value)}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
        <div className="field budgetField">
          <label htmlFor="budget">Max acquisition budget</label>
          <div className="inputWrap">
            <IndianRupee size={18} />
            <input
              id="budget"
              value={budget}
              inputMode="numeric"
              onChange={(event) => setBudget(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") loadMarkets();
              }}
            />
          </div>
        </div>
        <button className="searchButton" type="button" onClick={loadMarkets}>
          <Search size={18} />
          Analyze
        </button>
      </section>

      {error && <div className="error">{error}</div>}

      <section className="summaryGrid">
        <div className="metric">
          <span>Markets scanned</span>
          <strong>{markets.length}</strong>
        </div>
        <div className="metric">
          <span>Top score</span>
          <strong>{markets[0]?.investment_score ?? "--"}</strong>
        </div>
        <div className="metric">
          <span>Best yield</span>
          <strong>{Math.max(...markets.map((m) => m.gross_yield_pct), 0).toFixed(2)}%</strong>
        </div>
        <div className="metric">
          <span>Radius</span>
          <strong>50 km</strong>
        </div>
      </section>

      <section className="workspace">
        <div className="rankings">
          <div className="sectionTitle">
            <h2>Potential sites</h2>
            <span>{loading ? "Loading" : "Ranked by model"}</span>
          </div>
          <div className="cards">
            {markets.map((market) => (
              <button
                key={market.id}
                type="button"
                className={`siteCard ${selected?.id === market.id ? "selected" : ""}`}
                onClick={() => setSelectedId(market.id)}
              >
                <div>
                  <strong>{market.locality}</strong>
                  <span>{market.district}</span>
                </div>
                <div className="score">{market.investment_score}</div>
                <div className="siteStats">
                  <span>{formatCurrency(market.avg_price_per_sqft)}/sq ft</span>
                  <span>{market.gross_yield_pct}% yield</span>
                  <span>{market.distance_km} km</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="detail">
          {selected && (
            <>
              <div className="detailHeader">
                <div>
                  <p className="eyebrow">Research brief</p>
                  <h2>{selected.locality}</h2>
                </div>
                <div className="bigScore">{selected.investment_score}</div>
              </div>

              <p className="thesis">{selected.thesis}</p>

              <div className="signalGrid">
                <div>
                  <TrendingUp size={18} />
                  <span>Price YoY</span>
                  <strong>{selected.price_yoy_pct}%</strong>
                </div>
                <div>
                  <IndianRupee size={18} />
                  <span>2BHK rent</span>
                  <strong>{formatCurrency(selected.median_rent_2bhk)}</strong>
                </div>
                <div>
                  <MapPin size={18} />
                  <span>Distance</span>
                  <strong>{selected.distance_km} km</strong>
                </div>
                <div>
                  <ShieldAlert size={18} />
                  <span>Risk</span>
                  <strong>{selected.risk_score}/100</strong>
                </div>
              </div>

              <div className="mapPanel">
                <h3>Hyderabad area position</h3>
                <div className="miniMap" aria-label="Hyderabad area locality map">
                  {markets.map((market) => {
                    const x =
                      ((market.longitude - mapBounds.minLng) /
                        (mapBounds.maxLng - mapBounds.minLng)) *
                      100;
                    const y =
                      100 -
                      ((market.latitude - mapBounds.minLat) /
                        (mapBounds.maxLat - mapBounds.minLat)) *
                        100;
                    return (
                      <button
                        key={market.id}
                        type="button"
                        title={market.locality}
                        className={`mapDot ${selected.id === market.id ? "active" : ""}`}
                        style={{ left: `${x}%`, top: `${y}%` }}
                        onClick={() => setSelectedId(market.id)}
                      >
                        <span>{market.investment_score}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="chartPanel">
                <h3>Top locality score comparison</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="locality" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="score" fill="#2563eb" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="riskPanel">
                <h3>Risk flags</h3>
                {selected.risk_flags.map((flag) => (
                  <p key={flag}>{flag}</p>
                ))}
              </div>
            </>
          )}
        </div>
      </section>
    </main>
  );
}
