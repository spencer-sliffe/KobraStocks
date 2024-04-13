
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from  sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


time =datetime.now()
year=int(time.year)
yesterday = time - timedelta(days=1)
startyear=year-10
startStr=(str(startyear)+'-1-1')
yesterday=yesterday.strftime("%Y-%m-%d")

priceData= yf.Ticker('AAPL')
dataframe=priceData.history(period='1d',start=startStr,end=yesterday)
dataframe=dataframe.drop(['Dividends','Stock Splits'],axis=1)
dataframe.index=dataframe.index.date
dataframe['MA50']=dataframe['Close'].rolling(window=50).mean()
dataframe['MA9']=dataframe['Close'].rolling(window=9).mean()
dataframe['EMA12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
dataframe['EMA26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()

dataframe['MACD'] = dataframe['EMA12'] - dataframe['EMA26']
dataframe['Signal_Line'] = dataframe['MACD'].ewm(span=9, adjust=False).mean()
dataframe['Tomorrow'] =dataframe['Close']<dataframe['Close'].shift(-1)
dataframe.dropna(inplace=True)
print(dataframe)

X=dataframe.drop(['Tomorrow','High','Low','Open'],axis=1)
Y=dataframe['Tomorrow'].astype(int)

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=.2,random_state=40)
model=RandomForestClassifier()
model.fit(X_train,Y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(Y_test, predictions)
print("1) Model Accuracy:", accuracy)
print(dataframe)



param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [400,500,600,700,800],
    'criterion' :['gini', 'entropy']
}

# Create a RandomForest model
rf = RandomForestClassifier()

# Set up the GridSearchCV object
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                           cv = 3, n_jobs = -1, verbose = 2, scoring = 'accuracy')

# Fit the grid search to the data
grid_search.fit(X_train, Y_train)
best_grid = grid_search.best_estimator_

# Predict and check the accuracy
predictions = best_grid.predict(X_test)
print("Improved Accuracy:", accuracy_score(Y_test, predictions))

