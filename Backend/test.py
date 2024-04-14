
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from  sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np
import mplfinance as mpf
import plotly.graph_objects as go 

time =datetime.now()
year=int(time.year)
yesterday = time - timedelta(days=1)
startyear=year-5
startStr=(str(startyear)+'-1-1')
yesterday=yesterday.strftime("%Y-%m-%d")

priceData= yf.Ticker('AMC')
dataframe=priceData.history(period='1d',start=startStr,end=yesterday)
dataframe=dataframe.drop(['Dividends','Stock Splits'],axis=1)
#dataframe.index=dataframe.index.date
dataframe['MA50']=dataframe['Close'].rolling(window=50).mean()
dataframe['MA9']=dataframe['Close'].rolling(window=9).mean()
dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()

dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
dataframe['Month'] =dataframe['Close']<dataframe['Close'].shift(-30)
dataframe['Week'] =dataframe['Close']<dataframe['Close'].shift(-5)
dataframe['Tomorrow'] =dataframe['Close']<dataframe['Close'].shift(-1)
print()


dataframe['Price Diff'] = dataframe['Close'].diff()
dataframe['Gain'] = np.where(dataframe['Price Diff'] > 0, dataframe['Price Diff'], 0)
dataframe['Loss'] = np.where(dataframe['Price Diff'] < 0, -dataframe['Price Diff'], 0)

window_length = 14

# Calculate the exponential moving averages of gains and losses
dataframe['Avg Gain'] = dataframe['Gain'].ewm(alpha=1/window_length, min_periods=window_length).mean()
dataframe['Avg Loss'] = dataframe['Loss'].ewm(alpha=1/window_length, min_periods=window_length).mean()

dataframe['RS'] = dataframe['Avg Gain'] / dataframe['Avg Loss']
dataframe['RSI'] = 100 - (100 / (1 + dataframe['RS']))

dataframe.drop(['Price Diff', 'Gain', 'Loss', 'Avg Gain', 'Avg Loss', 'RS'], axis=1, inplace=True)



dataframe.dropna(inplace=True)


presentData = dataframe.tail(1)
print(presentData)


dataframe['Date'] = dataframe.index
dataframe['Date'] = pd.to_datetime(dataframe['Date'])


fig = go.Figure(data=[go.Candlestick(x=dataframe['Date'],
                open=dataframe['Open'], high=dataframe['High'],
                low=dataframe['Low'], close=dataframe['Close'],
                increasing_line_color= 'green', decreasing_line_color= 'red')])

fig.update_layout(title='Candlestick Chart', xaxis_title='Date',
                yaxis_title='Price', xaxis_rangeslider_visible=False)
#
fig.update_layout({
    'paper_bgcolor': 'black', 'font_color': '#00FF00'       # Sets the overall figure background color to black
})
    # Sets the plot background color to black
fig.update_xaxes(title_font=dict(color='#00FF00'))  # Specific axis title color
          # Sets the font color to Matrix green

fig.update_yaxes(title_font=dict(color='#00FF00'))
fig.show()
#mc = mpf.make_marketcolors(up='green', down='red', inherit=True)#
#    mpf.make_addplot(dataframe['Close'].rolling(window=9).mean(), color='blue'),  # 10-day MA
#s  = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=mc, facecolor='black')
##    mpf.make_addplot(dataframe['Close'].rolling(window=180).mean(), color='Purple')  # 10-day MA
#add_plots = [
##]
#    mpf.make_addplot(dataframe['Close'].rolling(window=50).mean(), color='orange'), # 20-day MA
### Plot the candlestick chart
#    
#
##

##mpf.plot(dataframe, type='candle',volume=True, addplot=add_plots, style=s, title='Goog Candlestick Chart', ylabel='Price ($)')#Accuracy for days
#X=dataframe.drop(['Month','Week','Tomorrow','High','Low','Open'],axis=1)

#

##
#Y=dataframe['Tomorrow'].astype(int)X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=40)
##    'n_estimators': [100, 200, 300],
#param_grid = {
##    'min_samples_split': [2, 5],#
#
##    'bootstrap': [True, False]
#    'max_depth': [None, 10, 20],
##
#    'min_samples_leaf': [1, 2],
##
#}rf = RandomForestClassifier(random_state=42)grid_search.fit(X_train, Y_train)
##
#
##grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
#print("RF DAY Improved Accuracy:", accuracy_score(Y_test, predictions))
##best_grid = grid_search.best_estimator_predictions = best_grid.predict(X_test)
#
##
#print(classification_report(Y_test, predictions))
###    'n_estimators': [100, 200],
##param_grid = {
###    'max_depth': [30, 50, 70]
#
###gbm = GradientBoostingClassifier()
###    'learning_rate': [0.01, 0.1, 0.2],
##grid_search.fit(X_train, Y_train)
###}
##print("GBC Improved Accuracy:", accuracy_score(Y_test, predictions))
###grid_search = GridSearchCV(gbm, param_grid, cv=3, verbose=2, n_jobs=-1)
##
###predictions = best_grid.predict(X_test)
##
##print(classification_report(Y_test, predictions))
##knn_model.fit(X_train, Y_train)
##
##print("KNN DAY Accuracy:", accuracy_score(Y_test, knn_pred))
#knn_model = KNeighborsClassifier()
##
#knn_pred = knn_model.predict(X_test)
##
#print(classification_report(Y_test, predictions))#Accuray for Week 
##
#
##
#X=dataframe.drop(['Month','Week','Tomorrow','High','Low','Open'],axis=1)
##
#
##Y=dataframe['Week'].astype(int)X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=40)
#    'n_estimators': [100, 200, 300],
##param_grid = {
#    'min_samples_split': [2, 5],
##
#    'bootstrap': [True, False]
##    'max_depth': [None, 10, 20],
#
##    'min_samples_leaf': [1, 2],
#
##}rf = RandomForestClassifier(random_state=42)grid_search.fit(X_train, Y_train)
##
#
##grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
#print("RF WEEK Improved Accuracy:", accuracy_score(Y_test, predictions))
##best_grid = grid_search.best_estimator_predictions = best_grid.predict(X_test)
#
##
#
##print(classification_report(Y_test, predictions))param_grid = {
#    'C': [0.1, 1, 10],
##
#    'kernel': ['rbf', 'poly', 'sigmoid']
##
##svm = SVC()
#    'gamma': [1, 0.1, 0.01],
##grid_search.fit(X_train, Y_train)
#}
##print("SVM WEEK Day Improved Accuracy:", accuracy_score(Y_test, predictions))
#grid_search = GridSearchCV(svm, param_grid, cv=3, verbose=2, n_jobs=-1)
##
#predictions = best_grid.predict(X_test)
##
#print(classification_report(Y_test, predictions))
##
#
##
#
###Accuracy for Month 
#X=dataframe.drop(['Month','Week','Tomorrow','High','Low','Open'],axis=1)
##
#
##
#
##Y=dataframe['Month'].astype(int)X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=40)
#    'n_estimators': [100, 200, 300],
##param_grid = {
##    'min_samples_split': [2, 5],
##
##    'bootstrap': [True, False]
##    'max_depth': [None, 10, 20],
##
#    'min_samples_leaf': [1, 2],
##
#}rf = RandomForestClassifier(random_state=42)grid_search.fit(X_train, Y_train)
##
#
##grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
#print("RF MONTH Improved Accuracy:", accuracy_score(Y_test, predictions))
##best_grid = grid_search.best_estimator_predictions = best_grid.predict(X_test)
#
##
#
##print(classification_report(Y_test, predictions))


param_grid = {
#    'C': [0.1, 1, 10],
##
#    'kernel': ['rbf', 'poly', 'sigmoid']
##
##svm = SVC()
#    'gamma': [1, 0.1, 0.01],
##grid_search.fit(X_train, Y_train)
#}
##print("SVM MONTH Improved Accuracy:", accuracy_score(Y_test, predictions))
#grid_search = GridSearchCV(svm, param_grid, cv=3, verbose=2, n_jobs=-1)
##
#predictions = best_grid.predict(X_test)
##print(classification_report(Y_test, predictions))#