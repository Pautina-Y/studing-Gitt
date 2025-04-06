from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from pandas import DataFrame, Series
from pathlib import Path
from sys import path
from numpy import fliplr


dir_path = Path(path[0])

data_raw = load_breast_cancer()

data = DataFrame(data_raw['data'], columns = data_raw['feature_names'])
target = Series(data_raw['target'])

data_all = DataFrame(
    dict(zip(
        data_raw['feature_names'],
        data_raw['data'].T
    ))
    | {'target' : data_raw['target']}
)
print(data_all.info())

#data_all['target'].value_counts()
#data_all.describe().round(2).transpose()

data - data.describe().loc['mean']

#нормализация данных
data_norm = (data - data.describe().loc['mean']) / data.describe().loc['std']

print(data_norm)

mean_0 = data_norm.loc[target == 0].mean().round(3)
mean_1 = data_norm.loc[target == 1].mean().round(3)

groupped = DataFrame({
    'mean 0': mean_0,
    'mean 1': mean_1,
    'diff': abs(mean_0 - mean_1)
}).sort_values(by = 'diff', ascending = False)

print(groupped)

#fig = plt.figure(figsize = (8, 4))
#axs = fig.subplots()
#
#for var_name in groupped.index[:10]:
#    axs.clear()
#    axs.hist(
#        data_norm.loc[target == 0, var_name],
#        bins = 15,
#        alpha = 0.5,
#        label = '(0) злокачественная'
#    )
#    axs.hist(
#        data_norm.loc[target == 1, var_name],
#        bins = 15,
#        alpha = 0.5,
#        label = '(1) доброкачественная'
#    )
#    axs.set(xlabel = var_name, ylabel = 'Количество значений в интервале')
#    fig.savefig(dir_path / f'breast_cancer/{var_name}.png', dpi = 200)

X = data_norm.loc[:, groupped.index[:10]]

x_train, x_test, y_train, y_test = train_test_split(
    X, target,
    test_size = 0.2,
    random_state = 1
)

model = LogisticRegression()

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

conf_matr = confusion_matrix(abs(y_test - 1), abs(y_pred - 1))
print(conf_matr)

print(1 - (sum(fliplr(conf_matr).diagonal() / sum(conf_matr.diagonal()))))