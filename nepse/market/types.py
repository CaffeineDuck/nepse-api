import datetime
from dataclasses import dataclass
from typing import Any


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


@dataclass
class FloorSheet:
    id: int
    contract_id: int
    contract_type: Any
    stock_symbol: str
    buyer_member_id: str
    seller_member_id: str
    contract_quantity: int
    contract_rate: int
    contract_amount: int
    business_date: datetime.date
    trade_book_id: int
    stock_id: int
    buyer_broker_name: str
    seller_broker_name: str
    trade_time: datetime.datetime
    security_name: str

    def __post_init__(self) -> None:
        year, month, day = self.business_date.split("-")
        self.business_date = datetime.date(int(year), int(month), int(day))
