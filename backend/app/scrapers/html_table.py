import requests
from bs4 import BeautifulSoup

from app.schemas import MarketSignalCreate
from app.services.geo import distance_from_hyderabad_km


class HtmlTableTrendCollector:
    """Collects approved public trend tables with known column names."""

    REQUIRED_COLUMNS = {
        "locality",
        "latitude",
        "longitude",
        "avg_price_per_sqft",
        "price_yoy_pct",
        "median_rent_2bhk",
        "rent_yoy_pct",
    }

    def __init__(self, url: str):
        self.url = url

    def collect(self) -> list[MarketSignalCreate]:
        response = requests.get(self.url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return []

        headers = [cell.get_text(strip=True).lower() for cell in table.find_all("th")]
        if not self.REQUIRED_COLUMNS.issubset(set(headers)):
            return []

        rows = []
        for tr in table.find_all("tr")[1:]:
            values = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(values) != len(headers):
                continue
            item = dict(zip(headers, values))
            latitude = float(item["latitude"])
            longitude = float(item["longitude"])
            rows.append(
                MarketSignalCreate(
                    locality=item["locality"],
                    district=item.get("district", "Hyderabad"),
                    latitude=latitude,
                    longitude=longitude,
                    distance_km=distance_from_hyderabad_km(latitude, longitude),
                    avg_price_per_sqft=int(float(item["avg_price_per_sqft"])),
                    price_yoy_pct=float(item["price_yoy_pct"]),
                    median_rent_2bhk=int(float(item["median_rent_2bhk"])),
                    rent_yoy_pct=float(item["rent_yoy_pct"]),
                    inventory_level=item.get("inventory_level", "medium").lower(),
                    days_on_market=int(float(item.get("days_on_market", 45))),
                    infrastructure_score=int(float(item.get("infrastructure_score", 60))),
                    employment_score=int(float(item.get("employment_score", 60))),
                    risk_score=int(float(item.get("risk_score", 50))),
                    source=self.url,
                )
            )
        return rows
