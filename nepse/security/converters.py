from nepse.security.types import (
    Company,
    DailyTrade,
    Instrument,
    SectorMaster,
    Security,
    SecurityResponse,
    ShareGroup,
)


def create_sector_master_object(data: dict):
    model = SectorMaster(
        id=data.get("id"),
        description=data.get("description"),
        active_status=data.get("activeStatus"),
        regulatory_body=data.get("regulatoryBody"),
    )
    return model


def create_company_object(data: dict):
    sector_master = create_sector_master_object(data.get("sectorMaster"))
    model = Company(
        id=data.get("id"),
        short_name=data.get("shortName"),
        contact_person=data.get("contactPerson"),
        email=data.get("email"),
        website=data.get("website"),
        name=data.get("name"),
        sector_master=sector_master,
    )
    return model


def create_instrument_object(data: dict):
    model = Instrument(
        id=data.get("id"),
        code=data.get("code"),
        description=data.get("description"),
        active_status=data.get("activeStatus"),
    )
    return model


def create_share_group(data: dict):
    model = ShareGroup(
        id=data.get("id"),
        name=data.get("name"),
        active_status=data.get("activeStatus"),
        description=data.get("description"),
        is_default=data.get("isDefault"),
        capital_range_min=data.get("capitalRangeMin"),
        modified_by=data.get("modifiedBy"),
        modified_date=data.get("modifiedDate"),
    )
    return model


def create_security_object(data: dict):
    company = create_company_object(data.get("companyId"))
    instrument = create_instrument_object(data.get("instrumentType"))
    share_group = create_share_group(data.get("shareGroupId"))

    model = Security(
        company=company,
        instrument_type=instrument,
        share_group=share_group,
        id=data.get("id"),
        symbol=data.get("symbol"),
        isin=data.get("isin"),
        permitted_to_trade=data.get("permittedToTrade"),
        listing_date=data.get("listingDate"),
        credit_rating=data.get("creditRating"),
        tick_size=data.get("tickSize"),
        capital_gain_base_date=data.get("capitalGainBaseDate"),
        face_value=data.get("faceValue"),
        high_range_DPR=data.get("highRangeDpr"),
        issuer_name=data.get("issuerName"),
        me_instance_number=data.get("meInstanceNumber"),
        parent_id=data.get("parentId"),
        record_type=data.get("recordType"),
        scheme_name=data.get("schemeName"),
        scheme_description=data.get("schemeDescription"),
        secured=data.get("secured"),
        series=data.get("series"),
        active_status=data.get("activeStatus"),
        divisor=data.get("divisor"),
        cds_stock_ref_id=data.get("cdsStockRefId"),
        security_name=data.get("securityName"),
        is_promoter=data.get("isPromoter"),
        networth_base_price=data.get("networthBasePrice"),
        security_trade_cycle=data.get("securityTradeCycle"),
        trading_start_date=data.get("tradingStartDate"),
    )
    return model


def create_daily_trade_object(data: dict):
    model = DailyTrade(
        security_id=data.get("securityId"),
        open_price=data.get("openPrice"),
        high_price=data.get("highPrice"),
        low_price=data.get("lowPrice"),
        total_trade_quantity=data.get("totalTradeQuantity"),
        total_trades=data.get("totalTrades"),
        last_traded_price=data.get("lastTradedPrice"),
        previous_close=data.get("previousClose"),
        business_date=data.get("businessDate"),
        close_price=data.get("closePrice"),
        fifty_two_week_low=data.get("fiftyTwoWeekLow"),
        fifty_two_week_high=data.get("fiftyTwoWeekHigh"),
        last_updated_date_time=data.get("lastUpdatedDateTime"),
    )
    return model


def create_reponse_object(data: dict):
    daily_trade = create_daily_trade_object(data.get("securityDailyTradeDto"))
    security = create_security_object(data.get("security"))

    model = SecurityResponse(
        daily_trade=daily_trade,
        security=security,
        stock_listed_shares=data.get("stockListedShares"),
        paid_up_capital=data.get("paidUpCapital"),
        issued_capital=data.get("issuedCapital"),
        market_capitalization=data.get("marketCapitalization"),
        public_shares=data.get("publicShares"),
        public_percentage=data.get("publicPercentage"),
        promoter_shares=data.get("promoterShares"),
        promoter_percentage=data.get("promoterPercentage"),
        updated_date=data.get("updatedDate"),
        security_id=data.get("securityId"),
    )
    return model
