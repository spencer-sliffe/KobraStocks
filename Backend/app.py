from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.offline as pyo
from main import retrieveData, addIndicators, makeChart

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Contact', methods=['GET'])
def contact():
    return render_template('Contact.html')

@app.route('/About', methods=['GET'])
def about():
    return render_template('About.html')

@app.route('/Services', methods=['GET'])
def services():
    return render_template('Services.html')



@app.route('/results', methods=['GET'])
def results_page():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default=1, type=int)
    mA9 = request.args.get('MA9', default=False, type=bool)
    mA50 = request.args.get('MA50', default=False, type=bool)
    mACD= request.args.get('MACD', default=False, type=bool)
    rSI = request.args.get('RSI', default=False, type=bool)

    dataframe = retrieveData(ticker,period)
    dataframe=addIndicators(dataframe,mA9,mA50,mACD,rSI)
    fig=makeChart(dataframe,mA9,mA50)

    

    
    graph_html = pyo.plot(fig, output_type='div', include_plotlyjs=True)
    return render_template('results.html', graph_html=graph_html,ticker=ticker)

   

@app.errorhandler(404)
def page_not_found(e):
    # your custom error page
    return 'This page does not exist', 404

# Define more routes as necessary

if __name__ == '__main__':
    app.run(debug=True)