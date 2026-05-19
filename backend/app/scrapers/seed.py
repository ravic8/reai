from app.schemas import MarketSignalCreate
from app.services.geo import distance_from_hyderabad_km


SEED_MARKETS = [
    ("Gachibowli", "Hyderabad", 17.4401, 78.3489, 9800, 8.5, 42000, 9.0, "low", 28, 88, 95, 42),
    ("Kokapet", "Rangareddy", 17.3973, 78.3333, 10400, 11.8, 43000, 10.5, "medium", 34, 91, 86, 48),
    ("Tellapur", "Sangareddy", 17.4634, 78.2763, 7200, 12.5, 31000, 9.8, "medium", 39, 82, 78, 44),
    ("Nallagandla", "Rangareddy", 17.4757, 78.3216, 8200, 9.6, 36000, 8.7, "low", 31, 82, 83, 39),
    ("Kondapur", "Rangareddy", 17.4647, 78.3648, 8900, 7.9, 39000, 8.1, "low", 30, 80, 91, 43),
    ("Miyapur", "Hyderabad", 17.4933, 78.3915, 6800, 7.1, 28500, 7.8, "medium", 43, 76, 75, 45),
    ("Kompally", "Medchal-Malkajgiri", 17.5385, 78.4820, 6100, 8.8, 26000, 7.2, "medium", 46, 73, 68, 41),
    ("Shamshabad", "Rangareddy", 17.2512, 78.4377, 5600, 10.4, 23000, 6.8, "medium", 51, 84, 62, 52),
    ("Adibatla", "Rangareddy", 17.2358, 78.5426, 4700, 9.9, 18500, 6.4, "high", 58, 78, 64, 57),
    ("Uppal", "Medchal-Malkajgiri", 17.4058, 78.5591, 5900, 6.5, 25000, 6.9, "medium", 45, 79, 70, 46),
    ("Bachupally", "Medchal-Malkajgiri", 17.5500, 78.3853, 6300, 8.4, 27500, 7.5, "medium", 42, 75, 72, 44),
    ("Patancheru", "Sangareddy", 17.5333, 78.2645, 5200, 8.7, 21000, 6.9, "high", 54, 70, 66, 55),
]


class SeedTrendCollector:
    def collect(self) -> list[MarketSignalCreate]:
        results = []
        for row in SEED_MARKETS:
            (
                locality,
                district,
                latitude,
                longitude,
                price,
                price_yoy,
                rent,
                rent_yoy,
                inventory,
                dom,
                infra,
                employment,
                risk,
            ) = row
            results.append(
                MarketSignalCreate(
                    locality=locality,
                    district=district,
                    latitude=latitude,
                    longitude=longitude,
                    distance_km=distance_from_hyderabad_km(latitude, longitude),
                    avg_price_per_sqft=price,
                    price_yoy_pct=price_yoy,
                    median_rent_2bhk=rent,
                    rent_yoy_pct=rent_yoy,
                    inventory_level=inventory,
                    days_on_market=dom,
                    infrastructure_score=infra,
                    employment_score=employment,
                    risk_score=risk,
                    source="seed:hyderabad-50km",
                )
            )
        return results

