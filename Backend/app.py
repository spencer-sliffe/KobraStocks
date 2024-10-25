from flask import Flask, jsonify, request
import pandas as pd
from main import retrieveData, addIndicators, makeChart, trainModels

app = Flask(__name__)

@app.route('/api/stock_data', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default=1, type=int)
    mA9 = request.args.get('MA9', default=False, type=bool)
    mA50 = request.args.get('MA50', default=False, type=bool)
    mACD = request.args.get('MACD', default=False, type=bool)
    rSI = request.args.get('RSI', default=False, type=bool)

    dataframe = retrieveData(ticker, period)
    dataframe = addIndicators(dataframe, mA9, mA50, mACD, rSI)

    # Serialize the stock data to JSON and return it
    return dataframe.to_json()

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../client/dist', template_folder='../client/dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
