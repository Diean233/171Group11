import pickle
import numpy as np
import pandas as pd
import financialanalysis as fa
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

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

# Reshape data (sklearn gets mad if I don't)
X_train = StandardScaler().fit_transform(X_train.values.reshape(-1, 1))
y_train = StandardScaler().fit_transform(y_train.values.reshape(-1, 1))
X_test = StandardScaler().fit_transform(X_test.values.reshape(-1, 1))
y_test = StandardScaler().fit_transform(y_test.values.reshape(-1, 1))

# Degree 25
polyreg = make_pipeline(PolynomialFeatures(
    25), StandardScaler(), LinearRegression())
polyreg.fit(X_train, y_train)

pickle.dump(polyreg, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))
