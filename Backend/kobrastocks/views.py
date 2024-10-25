from flask import jsonify, request, render_template
from .services import get_stock_data

# Example API route to fetch stock data
def stock_data_view():
    """
    Handle requests for stock data.
    This function will be called by a route in `routes.py`.
    """
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default=1, type=int)
    
    stock_data = get_stock_data(ticker, period)
    return jsonify(stock_data)

# Optional: Server-side rendering for a page not handled by Vue
def legacy_page_view():
    """
    Example for rendering a legacy page using Flask templates (if needed).
    This can be called from `routes.py`.
    """
    return render_template('legacy_page.html')
