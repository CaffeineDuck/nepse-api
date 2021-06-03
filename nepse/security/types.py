import datetime
from dataclasses import dataclass
from typing import Any


@dataclass
class Instrument:
    id: int
    code: str
    description: str
    active_status: str


@dataclass
class ShareGroup:
    id: int
    name: str
    description: str
    capital_range_min: int
    modified_by: str
    modified_date: datetime.date
    active_status: str
    is_default: str


@dataclass
class SectorMaster:
    id: int
    sector_description: str
    active_status: str
    regulatory_body: str


@dataclass
class Company:
    id: int
    company_short_name: str
    company_name: str
    email: str
    company_website: str
    company_contact_person: str
    sector_master: SectorMaster
    company_registration_number: int
    active_status: str

    def __post_init__(self) -> None:
        self.sector_master = SectorMaster(**self.sector_master)


@dataclass
class Security:
    id: int
    symbol: str
    isin: str
    permitted_to_trade: bool
    listing_date: datetime.date
    credit_rating: Any  # TODO: Get the actual data type!
    tick_size: int
    instrument_type: Instrument
    capital_gain_base_date: datetime.date
    face_value: int
    high_range_dpr: Any  # TODO: Get the actual data type!
    issuer_name: str
    me_instance_number: int
    parent_id: int
    record_type: int
    scheme_description: str
    scheme_name: str
    secured: Any  # TODO: Get the actual data type!
    series: Any  # TODO: Get the actual data type!
    active_status: str
    divisor: int
    cds_stock_ref_id: int
    security_name: str
    trading_start_date: datetime.datetime
    networth_base_price: float
    security_trade_cycle: int
    is_promoter: bool
    company_id: Company
    share_group_id: ShareGroup

    def __post_init__(self) -> None:
        self.company_id = Company(**self.company_id)
        self.instrument_type = Instrument(**self.instrument_type)
        try:
            self.share_group_id = ShareGroup(**self.share_group_id)
        except TypeError:
            self.share_group_id = None


@dataclass
class DailyTrade:
    security_id: int
    open_price: int
    high_price: int
    low_price: int
    total_trade_quantity: int
    total_trades: int
    last_traded_price: int
    previous_close: int
    business_date: datetime.date
    close_price: int
    fifty_two_week_high: int
    fifty_two_week_low: int
    last_updated_date_time: datetime.time


@dataclass
class SecurityResponseDetailed:
    security_daily_trade_dto: DailyTrade
    security: Security
    stock_listed_shares: int
    paid_up_capital: int
    issued_capital: int
    market_capitalization: int
    public_shares: int
    public_percentage: int
    promoter_shares: int
    promoter_percentage: int
    updated_date: datetime.date
    security_id: int

    def __post_init__(self) -> None:
        self.security = Security(**self.security)
        self.security_daily_trade_dto = DailyTrade(**self.security_daily_trade_dto)


@dataclass
class SecurityResponse:
    security_id: int
    security_name: str
    symbol: str
    index_id: int
    open_price: int
    high_price: int
    low_price: int
    total_trade_quantity: int
    last_traded_price: int
    percentage_change: float
    last_updated_date_time: datetime.datetime
    last_traded_volume: Any
    previous_close: int


@dataclass
class LiveSecurityTrade:
    id: int
    business_date: datetime.date
    security_id: int
    symbol: str
    security_name: str
    open_price: int
    high_price: int
    low_price: int
    close_price: int
    total_traded_quantity: int
    total_traded_value: int
    previous_day_close_price: int
    fifty_two_week_high: int
    fifty_two_week_low: int
    last_updated_time: datetime.datetime
    last_updated_price: int
    total_trades: int
    average_traded_price: float
    market_capitalization: float
