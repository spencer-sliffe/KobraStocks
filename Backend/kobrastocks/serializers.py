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
