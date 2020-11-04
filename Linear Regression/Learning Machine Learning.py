import matplotlib.pyplot as plot
import pandas as p
from sklearn import linear_model
info = p.read_csv('Base Data.csv')
plot.scatter(info.x, info.y, color = 'red')
reg = linear_model.LinearRegression()
reg.fit(info[['x']], info.y)
plot.plot((-3, 7), (reg.predict([[-3]]), reg.predict([[7]])))
d = p.read_csv('Test Data.csv')
d['prices'] = reg.predict(d)
d.to_csv('predictions.csv')
plot.show()
