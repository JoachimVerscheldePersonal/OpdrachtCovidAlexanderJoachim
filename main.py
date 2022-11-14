import pandas as pd

from dashboard_manager import CovidDashboardManager
from dataproviders import CovidDataProvider
import ipywidgets as widgets
import matplotlib.pyplot as plt
from ipywidgets import interact

covid_dashboard_manager = CovidDashboardManager()
plt.rcParams["figure.figsize"] = (20,15)
years = covid_dashboard_manager.get_years()
provinces = covid_dashboard_manager.get_provinces()
def update_plot(year: int, show_total_reported: bool = True, show_hospital_admission: bool = True, show_deceased: bool = True, province: str = 'Netherlands', show_municipalities: bool = False, show_months: bool = False):
    covid_dashboard_manager.render_dashboard(year, show_total_reported, show_hospital_admission, show_deceased, province, show_municipalities, show_months)


total_reported_checkbox = widgets.Checkbox(value=True, description = 'Total_reported', disabled= False)
hospital_admission_checkbox = widgets.Checkbox(value=True, description = 'Hospital_admission', disabled= False)
deceased_checkbox = widgets.Checkbox(value=True, description = 'Deceased', disabled= False)
show_municipalities_checkbox = widgets.Checkbox(value=False, description = 'Municipalities', disabled= False)
show_months_checkbox = widgets.Checkbox(value=False, description = 'Months', disabled= False)
    
update_plot(2020,True,True,True,'Utrecht', show_municipalities=False, show_months=False)
interact(update_plot, year = years, show_total_reported = total_reported_checkbox, show_hospital_admission = hospital_admission_checkbox, show_deceased= deceased_checkbox, province = provinces, show_municipalities= show_municipalities_checkbox, show_months= show_months_checkbox)
