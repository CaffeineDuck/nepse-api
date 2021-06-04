import datetime
from dataclasses import dataclass


@dataclass
class MarketCap:
    business_date: datetime.date
    mar_cap: float
    sen_mar_cap: float
    float_mar_cap: float
    sen_float_mar_cap: float

    def __post_init__(self) -> None:
        year, month, day = self.business_date.split("-")
        self.business_date = datetime.date(int(year), int(month), int(day))
