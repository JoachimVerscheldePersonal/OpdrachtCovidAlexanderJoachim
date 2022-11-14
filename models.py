import pandas as pd
from dataproviders import CovidDataProvider
from statsmodels.tsa.arima.model import ARIMA
from datetime import date
from dateutil.relativedelta import relativedelta


class CovidArimaModel():

    def __init__(self, data_provider: CovidDataProvider):
        self.covid_dataset = data_provider.get_dataset()[:]

        
    def get_covid_time_series(self) -> pd.DataFrame:

        dataset = self.covid_dataset
        dataset =  CovidDataProvider.group_by(dataset, ['Date_of_publication'])
        dataset = dataset.set_index('Date_of_publication')
        dataset = dataset.asfreq('d')
        return dataset

    def get_prediction(self , property_to_predict: str , from_date: date, days_to_forecast: int) -> pd.DataFrame:
        df = self.get_covid_time_series()
        # the order was determined in the timeseries_analysis notebook
        model = ARIMA(df[property_to_predict], order=(4, 1, 4))  
        fitted = model.fit()

        forecast = fitted.get_forecast(days_to_forecast)
        conf_interval = forecast.conf_int(alpha=0.45)

        df_forecasts = pd.DataFrame(index = forecast.row_labels, data = forecast.predicted_mean)
        df = (pd.concat([df, df_forecasts]))
        df = df.join(conf_interval)
        df = df[df.index.date >= from_date]

        return df

        
        