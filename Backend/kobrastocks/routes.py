from flask import Blueprint, jsonify, request
from .services import get_stock_data, send_contact_form
from .serializers import stock_data_schema, contact_form_schema

# Define a Flask blueprint for the main app routes
main = Blueprint('main', __name__)

@main.route('/api/stock_data', methods=['GET'])
def stock_data():
    """
    Example endpoint for fetching stock data.
    Vue will call this endpoint and receive a JSON response.
    """
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default=1, type=int)
    
    # Call your service layer function to get stock data
    stock_data = get_stock_data(ticker, period)
    
    # Use a serializer to return the data in a clean format
    return jsonify(stock_data_schema.dump(stock_data))

@main.route('/api/contact', methods=['POST'])
def contact():
    """
    Example POST endpoint to handle contact form submissions.
    Vue will post form data here.
    """
    data = request.get_json()
    errors = contact_form_schema.validate(data)
    
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Process the contact form (send email, etc.)
    success = send_contact_form(data)
    
    if success:
        return jsonify({"message": "Contact form submitted successfully"}), 200
    else:
        return jsonify({"error": "Failed to submit contact form"}), 500
