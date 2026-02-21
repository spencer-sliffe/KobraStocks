"""
------------------Prologue--------------------
File Name: serializers.py
Path: Backend/kobrastocks/serializers.py

Description:
Defines Marshmallow schemas for serializing and validating data structures. Includes:
- `StockDataSchema`: Serializer for stock data, ensuring fields like ticker, open price, and volume are correctly formatted.
- `ContactFormSchema`: Serializer and validator for contact form submissions, checking required fields and applying length validations.

Input:
Data dictionaries representing stock information and contact form submissions.

Output:
Serialized and validated data for API responses and form handling.

Collaborators: Spencer Sliffe
---------------------------------------------
"""

from marshmallow import Schema, fields, validate


class StockDataSchema(Schema):
    """
    Serializer for stock data.
    Ensures that the API response is formatted properly.
    """
    ticker = fields.Str(required=True)
    open_price = fields.Float(required=True)
    close_price = fields.Float(required=True)
    high_price = fields.Float(required=True)
    low_price = fields.Float(required=True)
    volume = fields.Int(required=True)
    name = fields.Str(required=True)
    percentage_change = fields.Float(required=True)


stock_data_schema = StockDataSchema()
stock_data_list_schema = StockDataSchema(many=True)


class ContactFormSchema(Schema):
    """
    Serializer and validator for contact form submissions.
    """
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    message = fields.Str(required=True, validate=validate.Length(min=10))


contact_form_schema = ContactFormSchema()


class PortfolioStockSchema(Schema):
    ticker = fields.Str(required=True)
    number_of_shares = fields.Int(required=True)
    pps_at_purchase = fields.Float(required=True)
    total_invested = fields.Float()
    current_value = fields.Float()
    profit_loss = fields.Float()
    profit_loss_percentage = fields.Float()
    open_price = fields.Float()
    close_price = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    volume = fields.Int()
    name = fields.Str()
    percentage_change = fields.Float()


portfolio_stock_schema = PortfolioStockSchema()
portfolio_stock_list_schema = PortfolioStockSchema(many=True)


class PortfolioSchema(Schema):
    stocks = fields.Nested(PortfolioStockSchema, many=True)


portfolio_schema = PortfolioSchema()


class PortfolioRecommendationsSchema(Schema):
    recommendations = fields.Dict(keys=fields.Str(), values=fields.Raw())


portfolio_recommendations_schema = PortfolioRecommendationsSchema()


class CryptoDataSchema(Schema):
    """
    Serializer for cryptocurrency data.
    Ensures that the API response is formatted properly.
    """
    ticker = fields.Str(required=True)
    crypto_id = fields.Str(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    market_cap = fields.Float(required=False)
    percentage_change_24h = fields.Float(required=False)
    volume = fields.Float(required=False)
    rank = fields.Int(required=False)
    symbol = fields.Str(required=False)


crypto_data_schema = CryptoDataSchema()
crypto_data_list_schema = CryptoDataSchema(many=True)


class CryptoResultsDataSchema(Schema):
    """
    Serializer for cryptocurrency data.
    Ensures that the API response is formatted properly.
    """
    ticker = fields.Str(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    market_cap = fields.Float(required=False)
    percentage_change_24h = fields.Float(required=False)
    volume = fields.Float(required=False)
    rank = fields.Int(required=False)
    symbol = fields.Str(required=False)


crypto_results_data_schema = CryptoResultsDataSchema()
crypto_results_data_list_schema = CryptoResultsDataSchema(many=True)


class StockResultsDataSchema(Schema):
    """
    Serializer for stock results data.
    Ensures that the API response is formatted properly.
    """
    ticker = fields.Str(required=True)
    name = fields.Str(required=True)
    long_name = fields.Str(required=False)
    sector = fields.Str(required=False)
    industry = fields.Str(required=False)
    market_cap = fields.Float(required=False)
    enterprise_value = fields.Float(required=False)
    price = fields.Float(required=True)
    previous_close = fields.Float(required=False)
    open = fields.Float(required=False)
    day_low = fields.Float(required=False)
    day_high = fields.Float(required=False)
    fifty_two_week_low = fields.Float(required=False)
    fifty_two_week_high = fields.Float(required=False)
    fifty_day_average = fields.Float(required=False)
    two_hundred_day_average = fields.Float(required=False)
    volume = fields.Int(required=False)
    regular_market_volume = fields.Int(required=False)
    regular_market_price = fields.Float(required=False)
    dividend_yield = fields.Float(required=False)
    trailing_pe = fields.Float(required=False)
    forward_pe = fields.Float(required=False)
    beta = fields.Float(required=False)
    total_cash = fields.Float(required=False)
    total_debt = fields.Float(required=False)
    revenue = fields.Float(required=False)
    revenue_per_share = fields.Float(required=False)
    gross_profit = fields.Float(required=False)
    ebitda = fields.Float(required=False)
    operating_cashflow = fields.Float(required=False)
    free_cashflow = fields.Float(required=False)
    profit_margins = fields.Float(required=False)
    return_on_assets = fields.Float(required=False)
    return_on_equity = fields.Float(required=False)
    earnings_quarterly_growth = fields.Float(required=False)
    earnings_growth = fields.Float(required=False)
    revenue_growth = fields.Float(required=False)
    operating_margins = fields.Float(required=False)
    ebitda_margins = fields.Float(required=False)
    gross_margins = fields.Float(required=False)
    book_value = fields.Float(required=False)
    price_to_book = fields.Float(required=False)
    cash_per_share = fields.Float(required=False)
    debt_to_equity = fields.Float(required=False)
    held_percent_institutions = fields.Float(required=False)
    held_percent_insiders = fields.Float(required=False)
    short_ratio = fields.Float(required=False)
    shares_outstanding = fields.Int(required=False)
    float_shares = fields.Int(required=False)
    implied_shares_outstanding = fields.Int(required=False)
    shares_short = fields.Int(required=False)
    shares_short_prior_month = fields.Int(required=False)
    short_percent_of_float = fields.Float(required=False)
    date_short_interest = fields.Int(required=False)
    last_split_date = fields.Int(required=False)
    last_split_factor = fields.Str(required=False)
    address = fields.Str(required=False)
    website = fields.Str(required=False)
    full_time_employees = fields.Int(required=False)
    company_officers = fields.List(fields.Dict(), required=False)
    recommendation_key = fields.Str(required=False)
    recommendation_mean = fields.Float(required=False)
    number_of_analyst_opinions = fields.Int(required=False)
    target_high_price = fields.Float(required=False)
    target_low_price = fields.Float(required=False)
    target_mean_price = fields.Float(required=False)
    target_median_price = fields.Float(required=False)
    exchange = fields.Str(required=False)
    quote_type = fields.Str(required=False)
    currency = fields.Str(required=False)
    financial_currency = fields.Str(required=False)
    earnings_date = fields.List(fields.Int(), required=False)
    most_recent_quarter = fields.Int(required=False)
    last_fiscal_year_end = fields.Int(required=False)
    next_fiscal_year_end = fields.Int(required=False)
    long_business_summary = fields.Str(required=False)


# Create the single and multiple item schemas
stock_results_data_schema = StockResultsDataSchema()
stocks_results_data_list_schema = StockResultsDataSchema(many=True)
