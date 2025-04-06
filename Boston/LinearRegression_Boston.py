from pandas import read_csv, DataFrame, Series
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
from matplotlib import rcParams
from random import choice, seed

from pathlib import Path
from sys import path

rcParams['text.color'] = 'black'

dir_path = Path(path[0])
data_path = dir_path / 'boston.csv'
data = read_csv(data_path, comment = '#')
#data.info())
#data.describe().round(2))

fig = plt.figure(figsize = (5, 5))
axs = fig.subplots()
axs.scatter(data['MEDV'].index, data['MEDV'])
#plt.show()

corr_matrix_pearson = data.corr('pearson').round(2)
corr_matrix_spearman = data.corr('spearman').round(2)

fig = plt.figure(figsize = (56, 56))
axs = fig.subplots(14, 14)

for i, col1 in enumerate(data):
    for j, col2 in enumerate(data):
        if i > j:
            axs[i][j].scatter(data[col1], data[col2], s = 7)
            axs[i][j].text(
                data[col1].max(),
                data[col2].max(),
                f'p = {corr_matrix_pearson.loc[col1, col2]}\n'
                f's = {corr_matrix_spearman.loc[col1, col2]}',
                horizontalalignment = 'right',
                verticalalignment = 'top',
            )
            axs[i][j].set(
                xticks = [],
                yticks = [],
                xlabel = col1,
                ylabel = col2,
            )
        else:
            axs[i][j].axis('off')
#fig.savefig(dir_path / 'boston_14x14_graphs.png', dpi = 300)

#print(
#    'до отбраковки выбросов',
#    corr_matrix_pearson,
#    corr_matrix_spearman,
#    sep = '\n\n',
#    end = '\n\n'
#)

data_out = data.loc[data['MEDV'] != data['MEDV'].max()]

print(
    'после отбраковки выбросов',
    data_out.corr('pearson').round(2),
    data_out.corr('spearman').round(2),
    sep = '\n\n',
    end = '\n\n'
)

X = data_out.loc[:, ['CRIM', 'INDUS', 'RM', 'AGE', 'LSTAT']]
Y = data_out['MEDV']

test_rate = 0.2
test_len = int(X.shape[0] * test_rate)
train_len = X.shape[0] - test_len

#x_train, y_train, x_test, y_test = {}, {}, {}, {}

#seed(1)

#for _ in range(train_len):
#    while True:
#        rand_index = choice(X.index)
#        if rand_index in x_train:
#            continue
#        break
#    x_train[rand_index] = X.loc[rand_index]
#    y_train[rand_index] = Y.loc[rand_index]

#x_train = DataFrame(x_train).transpose()
#y_train = pd.Series(y_train)

#for rand_index in set(X.index) - set(x_train.index):
#    x_test[rand_index] = X.loc[rand_index]
#    y_test[rand_index] = Y.loc[rand_index]

#x_test = DataFrame(x_test).transpose()
#y_test = Series(y_test)

#for i in range(100):
#    x_train, x_test, y_train, y_test = train_test_split(
#        X, Y,
#        test_size = 0.2,
#        random_state = i,
#    )


x_train, x_test, y_train, y_test = train_test_split(
        X, Y,
        test_size = 0.2,
        random_state = 17,
    )
#создание модели
model = LinearRegression()

#обучение модели
model.fit(x_train, y_train)

#вычисление предсказанных значений для тестовой выборки
y_pred = model.predict(x_test)

#оценка эффективности с помощью метрик R-квадрат и среднеквадратичной ошибки
R2 = r2_score(y_test, y_pred)
RMSE = (sum((y_test - y_pred) ** 2) / y_test.shape[0])

print(f'seed = 17 R2 = {R2:.3f}\nRMSE = {RMSE:.1f}')