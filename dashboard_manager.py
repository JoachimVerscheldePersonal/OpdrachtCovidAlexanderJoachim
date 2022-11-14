import pandas as pd
import dataproviders as data
from dataproviders import CovidDataProvider
from models import CovidArimaModel
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from datetime import date
from dateutil.relativedelta import relativedelta

class CovidDashboardManager():

    def __init__(self):
        data_provider = CovidDataProvider()
        self.arima_model = CovidArimaModel(data_provider)
        self.dataset = data_provider.get_dataset()
        self.province = None
        self.year = None
        self.show_municipalities = False
        self.show_months = False
        self.show_total_reported = False
        self.show_hospital_admission = False
        self.show_deceased = False

    def update_current_state(self, year: int, show_total_reported: bool = True, show_hospital_admission: bool = True, show_deceased: bool = True, province: str = 'Netherlands', show_municipalities: bool = False, show_months: bool = False):
        """
        Updates the parameters set by the ipywidgets
        """
        self.year = year
        self.show_total_reported = show_total_reported
        self.show_hospital_admission = show_hospital_admission
        self.show_deceased = show_deceased
        self.province = province
        self.show_municipalities = show_municipalities
        self.show_months = show_months

    def get_years(self) -> list[int]:
        """
        Gets the years to populate the ipywidgets dropdown
        return: a list of years
        """
        return list(self.dataset.Date_of_publication.dt.year.unique())

    def get_provinces(self) -> list[str]:
        """
        Gets the provinces to populate the provinces ipywidgets dropdown
        return: a list of possible provinces
        """
        fixed_items = list(['Netherlands', 'All provinces'])
        return fixed_items + list(self.dataset.Province.unique())

    def get_data_for_barplot(self) -> pd.DataFrame:
        """
        Fetches the data for the bar plots using the covid data provider
        """
        dataset = CovidDataProvider.filter_by_year(self.dataset, self.year)
        if self.province.lower() == 'netherlands':
            dataset = CovidDataProvider.group_by(dataset, ['Year'])
        elif self.province.lower() == 'all provinces':
            dataset = CovidDataProvider.group_by(dataset, ['Year', 'Province'])
        else:
            dataset = CovidDataProvider.filter_by_province(dataset, self.province)
            
            if self.show_municipalities:
                dataset = CovidDataProvider.group_by(dataset, ['Year', 'Province' ,'Municipality_name'])
            elif self.show_months:
                dataset = CovidDataProvider.group_by(dataset, ['Year', 'Month'])
            else:
                dataset = CovidDataProvider.group_by(dataset, ['Year', 'Province'])

        return dataset

    def get_data_for_pie_plot(self) -> pd.DataFrame:
        """
        Fetches the covid data for the pie plots
        """
        dataset = CovidDataProvider.filter_by_year(self.dataset, self.year)
        if self.province.lower() == 'all provinces' or self.province.lower() == 'netherlands':
            dataset = CovidDataProvider.group_by(dataset, ['Year', 'Province'])
        else:
            dataset = CovidDataProvider.filter_by_province(dataset, self.province)
            dataset = CovidDataProvider.group_by(dataset, ['Year', 'Province' ,'Municipality_name'])

        return dataset

    def _get_barplot_parameters(self) -> tuple[str,list[str],str]:
        """
        Fetches the parameters needed to configure the matplotlib bar plot
        """

        title = None
        x = None
        y = []

        if self.province.lower() == 'netherlands':
            x = 'Year'
            title = f'The Netherlands in {self.year}'

        elif self.province.lower() == 'all provinces':
            x = 'Province'
            title = f'All provinces of The Netherlands in {self.year}'
        else:

            if self.show_municipalities:
                x = 'Municipality_name'
                title = f'Municipalities of {self.province} {self.year}'
            elif self.show_months:
                x = 'Month'
                title = f'{self.province} {self.year} by month'
            else:
                x = 'Province'
                title = f'{self.province} in {self.year}'

        if self.show_total_reported:
            y.append('Total_reported')

        if self.show_hospital_admission:
            y.append('Hospital_admission')

        if self.show_deceased:
            y.append('Deceased')

        return x,y,title

    def _get_pie_parameters(self, property:str) -> str:
        """
        Fetches the parameters needed to configure the matplotlib pie plot
        """
        title = None

        if self.province.lower() == 'all provinces' or self.province.lower() == 'netherlands':
            title = f'{property} for provinces of The Netherlands {self.year}'
        else:
            title = f'{property} for municipalities of {self.province} {self.year}'

        return  title

    def _get_line_parameters(self, days_to_forecast:int) -> str:
        """
        gets the title for the forecast plots
        """
        return  f'{days_to_forecast} days forecast The Netherlands {self.year}'
        
    def render_covid_barplot(self, axes: Axes):
        """
        fetches the data for the bar plot and plots it using matplotlib
        """
        df = self.get_data_for_barplot()
        x, y, title = self._get_barplot_parameters()
        ax = df.plot.bar(x=x, y=y,ax = axes)
        ax.set_title(title)
        ax.set_xlabel('')
        plt.setp(ax.get_xticklabels(), rotation=45)
        

    def render_covid_pieplot(self,axes: Axes, y:str):
        """
            fetches the data for the pie plot and plots it using matplotlib
        """
        df = self.get_data_for_pie_plot()
        df.set_index('Province' if self.province.lower() in ['netherlands','all provinces'] else 'Municipality_name', inplace=True)
        title = self._get_pie_parameters(y)
        ax = df.plot.pie(y=y, ax=axes, autopct='%1.1f%%', counterclock=False, startangle=90, legend=False)
        ax.set_ylabel('')
        ax.set_title(title)

    def render_line_chart(self, axes: Axes, property_to_forecast, months_window: int, days_to_forecast:int):
        """

        """
        prediction = self.arima_model.get_prediction(property_to_forecast, date.today() - relativedelta(months=months_window),days_to_forecast)
        axes.plot(prediction[property_to_forecast], label=property_to_forecast)
        axes.plot(prediction.predicted_mean[-days_to_forecast:], label='Forecast')
        title = self._get_line_parameters(days_to_forecast)
        axes.set_title(title)
        axes.legend(loc='upper left', fontsize=8)
        plt.setp(axes.get_xticklabels(), rotation=45)




    def render_dashboard(self,year: int, show_total_reported: bool = True, show_hospital_admission: bool = True, show_deceased: bool = True, province: str = 'Netherlands', show_municipalities: bool = False, show_months: bool = False):
        
        self.update_current_state(year, show_total_reported, show_hospital_admission, show_deceased, province, show_municipalities, show_months)
        
        fig = plt.figure(constrained_layout=True, figsize=(20,13))
        subfigures = fig.subfigures(1,2)
        left_figure = subfigures[0]
        right_figure = subfigures[1]

        gs_left = left_figure.add_gridspec(3,2)
        ax1 = left_figure.add_subplot(gs_left[0, :])
        ax2 = left_figure.add_subplot(gs_left[1, :])
        ax3 = left_figure.add_subplot(gs_left[2, :])

        gs_right = right_figure.add_gridspec(3,1)
        ax4 = right_figure.add_subplot(gs_right[0, 0])
        ax5 = right_figure.add_subplot(gs_right[1, 0])
        ax6 = right_figure.add_subplot(gs_right[2, 0])

        self.render_covid_barplot(ax1)
        self.render_line_chart(ax2, 'Total_reported', 3, 7)
        self.render_line_chart(ax3, 'Total_reported', 1, 3)

        if show_total_reported:
            self.render_covid_pieplot(ax4, 'Total_reported')
        if show_hospital_admission:
            self.render_covid_pieplot(ax5, 'Hospital_admission')
        if show_deceased:
            self.render_covid_pieplot(ax6, 'Deceased')

        plt.show(fig)
            
   

