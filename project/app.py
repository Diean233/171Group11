import numpy as np
import pandas as pd
import financialanalysis as fa
import matplotlib.pyplot as plt

from flask import Flask, request, render_template
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    def getDate(date):
        months = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }
        #2021-01-01
        year = date[:4]
        month = date[5:7]
        day = date[8:]

        if (int(day) < 10):
            day = day[1:]

        return months[month] + " " + day + ", " + year

    # reading data in 
    df = pd.read_csv('../Data/TSLA.csv')
    df.Date = pd.to_datetime(df.Date)
    df.Date = fa.datetimeToFloatyear(df.Date)

    # getting user input date
    # formatting the input date to be the same as the df
    date = [request.form.get('date')]
    dateArr = [np.array(date)]
    dateArr = pd.to_datetime(dateArr[0])
    dateArr = np.array(fa.datetimeToFloatyear(dateArr[0])).reshape(-1,1)

    # Using polynomial model from Lin_Poly_Regression-2.s5
    train, test = train_test_split(df, test_size=0.2, random_state=20)

    # Need to be sorted for polynomial regression to work properly
    train = train.sort_values(by=['Date'])
    test = test.sort_values(by=['Date'])

    X_train, X_test = train['Date'], test['Date']
    y_train, y_test = train['Close'], test['Close']

    X_train_og = X_train
    y_train_og = y_train

    # Reshape data (sklearn gets mad if I don't)
    X_train = StandardScaler().fit_transform(X_train.values.reshape(-1,1))
    y_train = StandardScaler().fit_transform(y_train.values.reshape(-1,1))
    X_test = StandardScaler().fit_transform(X_test.values.reshape(-1,1))
    y_test = StandardScaler().fit_transform(y_test.values.reshape(-1,1))

    sc = StandardScaler()
    sc.fit(X_train_og.values.reshape(-1,1))
    dateArr = sc.transform(dateArr)

    # Degree 25
    polyreg = make_pipeline(PolynomialFeatures(25), StandardScaler(), LinearRegression())
    polyreg.fit(X_train, y_train)
    y_pred = polyreg.predict(dateArr)

    # Predicting closing price with date
    sc.fit(y_train_og.values.reshape(-1,1))
    y_pred = sc.inverse_transform(y_pred)
    output = y_pred[0][0]
   
    predDate = getDate(date[0])
    price = str(output)
    price = price[:6]
    return render_template('index.html', predictedDate=predDate, predictedPrice=price)

if __name__ == '__main__':
    app.run(port=3000, debug=True)