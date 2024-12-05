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