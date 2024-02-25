import pandas as pd
from prophet import Prophet
import numpy as np
import holidays
from prophet.diagnostics import cross_validation
import pandas as pd
import numpy as np
from datetime import date
import itertools
import holidays
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric



df = pd.read_csv('partners-table.csv')
df = df.drop('month', axis=1)
df = df.drop('Unnamed: 4', axis=1)
df = df[(df['merchant_name'] == "Burger King")]
df = df.drop('merchant_name', axis=1)
df = df.reset_index(drop=True)
df = df.rename(columns={"day": "ds", "cashback":"y"})
df['ds'] = pd.to_datetime(df['ds'])
df['day_of_week'] = df['ds'].dt.dayofweek


# Вкидываем праздники, для их учёта моделькой
holidays_dict = holidays.RU(years=(2022, 2023))
df_holidays = pd.DataFrame.from_dict(holidays_dict, orient='index') \
    .reset_index()
df_holidays = df_holidays.rename({'index':'ds', 0:'holiday'}, axis ='columns')
df_holidays['ds'] = pd.to_datetime(df_holidays.ds)
df_holidays = df_holidays.sort_values(by=['ds'])
df_holidays = df_holidays.reset_index(drop=True)


dif_days = int((pd.to_datetime(df["ds"].max()) - pd.to_datetime(df["ds"].min())).days) // 2


def best_params():
    # Покрутим разные комбинации гиперпараметров

    param_grid = {
        'changepoint_prior_scale': [0.25, 0.05, 0.1],  ## по умолчанию 0.05, попробуем увеличить и уменьшить в два раза
        'seasonality_prior_scale': [5.0, 10.0, 20.0],  ## по умолчанию 10.0, попробуем увеличить и уменьшить в два раза
        'holidays_prior_scale': [5.0, 10.0, 20.0],  ## по умолчанию 10.0, попробуем увеличить и уменьшить в два раза
    }

    # Создаем все комбинации параметров
    all_params = [dict(zip(param_grid.keys(), v)) for v in itertools.product(*param_grid.values())]
    mapes = []  # Сюда будем складывать метрику MAPE

    # Крутим кроссвалидацию со всеми комбинациями параметров
    for params in all_params:
        m = Prophet(**params, holidays=df_holidays, daily_seasonality="auto", weekly_seasonality="auto",
                    yearly_seasonality="auto")
        m.add_regressor('day_of_week')
        m.fit(df)  # Fit model with given params
        df_cv = cross_validation(m, initial=f'{dif_days} days', period=f'{dif_days // 6} days',
                                 horizon=f'{dif_days // 3} days', parallel="processes")
        df_p = performance_metrics(df_cv,
                                   rolling_window=1)  ## тут окно для подсчета метрики 1, чтобы метрика считалась по всему горизонту
        mapes.append(df_p['mape'].values[0])

    # Смотрим на результаты с разными параметрами
    tuning_results = pd.DataFrame(all_params)
    tuning_results['mape'] = mapes

best_params()

if __name__ == '__main__':
    best_params()