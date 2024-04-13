
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

time =datetime.now()
year=int(time.year)
yesterday = time - timedelta(days=1)
startyear=year-5
startStr=(str(startyear)+'-1-1')
yesterday=yesterday.strftime("%Y-%m-%d")

priceData= yf.Ticker('GOOG')
dataframe=priceData.history(period='1d',start=startStr,end=yesterday)
dataframe=dataframe.drop(['Dividends','Stock Splits'],axis=1)
#dataframe.index=dataframe.index.date
dataframe['MA50']=dataframe['Close'].rolling(window=50).mean()
dataframe['MA9']=dataframe['Close'].rolling(window=9).mean()
dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()

dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
dataframe['Tomorrow'] =dataframe['Close']<dataframe['Close'].shift(-1)


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



print(dataframe)

mc = mpf.make_marketcolors(up='green', down='red', inherit=True)
s  = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=mc, facecolor='black')

add_plots = [
    mpf.make_addplot(dataframe['Close'].rolling(window=9).mean(), color='blue'),  # 10-day MA
    mpf.make_addplot(dataframe['Close'].rolling(window=50).mean(), color='orange'), # 20-day MA
    mpf.make_addplot(dataframe['Close'].rolling(window=180).mean(), color='Purple')  # 10-day MA
    
]

# Plot the candlestick chart
mpf.plot(dataframe, type='candle',addplot=add_plots, style=s, title='Goog Candlestick Chart', ylabel='Price ($)')

#X=dataframe.drop(['Tomorrow','High','Low','Open'],axis=1)
#Y=dataframe['Tomorrow'].astype(int)
#
#X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=40)

#param_grid = {
#    'n_estimators': [100, 200, 300],
#    'max_depth': [None, 10, 20],
#    'min_samples_split': [2, 5],
#    'min_samples_leaf': [1, 2],
#    'bootstrap': [True, False]
#}
#
#rf = RandomForestClassifier(random_state=42)
#grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2, scoring='accuracy')
#grid_search.fit(X_train, Y_train)
#best_grid = grid_search.best_estimator_
#
#predictions = best_grid.predict(X_test)
#print("RF Improved Accuracy:", accuracy_score(Y_test, predictions))
#print(classification_report(Y_test, predictions))



#param_grid = {
#    'C': [0.1, 1, 10],
#    'gamma': [1, 0.1, 0.01],
#    'kernel': ['rbf', 'poly', 'sigmoid']
#}

#svm = SVC()
#grid_search = GridSearchCV(svm, param_grid, cv=3, verbose=2, n_jobs=-1)
#grid_search.fit(X_train, Y_train)
#predictions = best_grid.predict(X_test)
#print("SVM Improved Accuracy:", accuracy_score(Y_test, predictions))
#
#
#
#
#param_grid = {
#    'n_estimators': [100, 200],
#    'learning_rate': [0.01, 0.1, 0.2],
#    'max_depth': [30, 50, 70]
#}

#gbm = GradientBoostingClassifier()
#grid_search = GridSearchCV(gbm, param_grid, cv=3, verbose=2, n_jobs=-1)
#grid_search.fit(X_train, Y_train)
#predictions = best_grid.predict(X_test)
#print("GBC Improved Accuracy:", accuracy_score(Y_test, predictions))
#
#
#
#knn_model = KNeighborsClassifier()
#knn_model.fit(X_train, Y_train)
#knn_pred = knn_model.predict(X_test)
#print("KNN Accuracy:", accuracy_score(Y_test, knn_pred))