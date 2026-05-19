export type Market = {
  id: number;
  locality: string;
  district: string;
  latitude: number;
  longitude: number;
  distance_km: number;
  avg_price_per_sqft: number;
  price_yoy_pct: number;
  median_rent_2bhk: number;
  rent_yoy_pct: number;
  inventory_level: string;
  days_on_market: number;
  infrastructure_score: number;
  employment_score: number;
  risk_score: number;
  source: string;
  updated_at: string;
  investment_score: number;
  gross_yield_pct: number;
  strategy_fit: string;
  thesis: string;
  risk_flags: string[];
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export async function fetchMarkets(strategy: string, budgetMax?: number): Promise<Market[]> {
  const params = new URLSearchParams({ radius_km: "50", strategy });
  if (budgetMax) params.set("budget_max", String(budgetMax));
  const response = await fetch(`${API_BASE}/api/markets?${params.toString()}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Unable to fetch market signals");
  }
  return response.json();
}

export async function refreshSeedData(): Promise<void> {
  const response = await fetch(`${API_BASE}/api/refresh`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ source: "seed" }),
  });
  if (!response.ok) {
    throw new Error("Unable to refresh market signals");
  }
}

