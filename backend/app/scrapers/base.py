from abc import ABC, abstractmethod

from app.schemas import MarketSignalCreate


class TrendCollector(ABC):
    @abstractmethod
    def collect(self) -> list[MarketSignalCreate]:
        raise NotImplementedError

