import numpy as np
import pandas as pd
import financialanalysis as fa
import matplotlib.pyplot as plt

from flask import Flask, request, render_template
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


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
        # 2021-01-01
        year = date[:4]
        month = date[5:7]
        day = date[8:]

        if (int(day) < 10):
            day = day[1:]

        return months[month] + " " + day + ", " + year

    # reading data in
    df = pd.read_csv('../../Data/TSLA.csv')
    df.Date = pd.to_datetime(df.Date)
    df.Date = fa.datetimeToFloatyear(df.Date)

    # Using polynomial model from Lin_Poly_Regression-2.s5
    train, test = train_test_split(df, test_size=0.2, random_state=20)

    # Need to be sorted for polynomial regression to work properly
    train = train.sort_values(by=['Date'])
    test = test.sort_values(by=['Date'])

    X_train, X_test = train['Date'], test['Date']
    y_train, y_test = train['Close'], test['Close']

    X_train_og = X_train
    y_train_og = y_train

    # getting user input date
    # formatting the input date to be the same as the df
    date = [request.form.get('date')]
    dateArr = [np.array(date)]
    dateArr = pd.to_datetime(dateArr[0])
    dateArr = np.array(fa.datetimeToFloatyear(dateArr[0])).reshape(-1, 1)

    sc = StandardScaler()
    sc.fit(X_train_og.values.reshape(-1, 1))
    dateArr = sc.transform(dateArr)

    y_pred = model.predict(dateArr)
    sc.fit(y_train_og.values.reshape(-1, 1))
    prediction = sc.inverse_transform(y_pred)
    prediction_price = round(prediction[0][0], 2)

    return render_template('index.html', predictedDate=getDate(date[0]), predictedPrice=prediction_price)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
