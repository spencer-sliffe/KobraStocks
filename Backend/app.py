from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
from main import retrieveData, addIndicators, makeChart, trainModels

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/Contact.html', methods=['GET'])
def contact():
    return render_template('Contact.html')

@app.route('/About.html', methods=['GET'])
def about():
    return render_template('About.html')

@app.route('/Services.html', methods=['GET'])
def services():
    return render_template('Services.html')



@app.route('/results.html', methods=['GET'])
def results_page():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default=1, type=int)
    mA9 = request.args.get('MA9', default=False, type=bool)
    mA50 = request.args.get('MA50', default=False, type=bool)
    mACD= request.args.get('MACD', default=False, type=bool)
    rSI = request.args.get('RSI', default=False, type=bool)
    if(mA9 == 'on'):
        mA9=True
    if(mA50=='on'):
        mA50=True
    if(mACD=='on'):
        mACD=True
    if(rSI=='on'):
        rSI=True


    dataframe = retrieveData(ticker,period)
    dataframe=addIndicators(dataframe,mA9,mA50,mACD,rSI)
    daccuracy,dprediction=trainModels(dataframe,1)
    waccuracy,wprediction=trainModels(dataframe,2)
    maccuracy,mprediction=trainModels(dataframe,3)
   
    fig=makeChart(dataframe,mA9,mA50)
    graph_html = pyo.plot(fig, output_type='div', include_plotlyjs=True)

   #remove this
    
    if(dprediction==1):
        dprediction='BUY'
    else:
        dprediction='SELL'
    if(wprediction==1):
        wprediction='BUY'
    else:
        wprediction='SELL'
    if(mprediction==1):
        mprediction='BUY'
    else:
        mprediction='SELL'
        
    
    today=dataframe.tail(1).drop(['Month', 'Week', 'Tomorrow'], axis=1)
    today['Date'] = today.index
    today['Date'] = pd.to_datetime(today['Date'])

    
    return render_template('results.html', graph_html=graph_html,ticker=ticker,
                           dprediction=dprediction,wprediction=wprediction,mprediction=mprediction,
                           daccuracy=format(daccuracy,".2f"),waccuracy=format(waccuracy,".2f"),maccuracy=format(maccuracy,".2f"),
                           
                           popen=format(today['Open'].iloc[0],".2f"),pclose=format(today['Close'].iloc[0],".2f"),phigh=format(today['High'].iloc[0],".2f"),plow=format(today['Low'].iloc[0],".2f"),volume=today['Volume'].iloc[0])



@app.errorhandler(404)
def page_not_found(e):
    # your custom error page
    return 'This page does not exist', 404

# Define more routes as necessary

if __name__ == '__main__':
    app.run(debug=True)