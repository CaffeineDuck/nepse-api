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
    description: str
    active_status: str
    regulatory_body: str


@dataclass
class Company:
    id: int
    short_name: str
    name: str
    email: str
    website: str
    contact_person: str
    sector_master: SectorMaster


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
    high_range_DPR: Any  # TODO: Get the actual data type!
    issuer_name: str
    me_instance_number: int
    parent_id: int
    record_type: int
    scheme_description: str
    scheme_name: str
    secured: Any  # TODO: Get the actual data type!
    series: Any  # TODO: Get the actual data type!
    share_group: ShareGroup
    active_status: str
    divisor: int
    cds_stock_ref_id: int
    security_name: str
    trading_start_date: datetime.datetime
    networth_base_price: float
    security_trade_cycle: int
    is_promoter: bool
    company: Company


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
class SecurityResponse:
    daily_trade: DailyTrade
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


@dataclass
class BaseSecurity:
    id: int
    symbol: str
    name: str
    active_status: str
