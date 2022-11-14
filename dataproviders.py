import pandas as pd
from datetime import datetime, date
import pathlib


class CovidDataProvider():
    _INFECTIONS_AND_MORTALITIES_DATASET1_FILE_NAME = 'https://data.rivm.nl/data/covid-19/COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv'
    _INFECTIONS_AND_MORTALITIES_DATASET2_FILE_NAME = 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv'
    _HOSPITAL_ADMISSIONS_DATASET1_FILE_NAME = 'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames_tm_03102021.csv'
    _HOSPITAL_ADMISSIONS_DATASET2_FILE_NAME = 'https://data.rivm.nl/covid-19/COVID-19_ziekenhuisopnames.csv'
    _MERGE_COLUMNS = ['Date_of_publication', 'Municipality_name']

    def __init__(self):
        self.covid_dataset = None
        self._load_infections_and_mortalities(self._INFECTIONS_AND_MORTALITIES_DATASET1_FILE_NAME, self._INFECTIONS_AND_MORTALITIES_DATASET2_FILE_NAME)
        self._load_hospital_admissions(self._HOSPITAL_ADMISSIONS_DATASET1_FILE_NAME, self._HOSPITAL_ADMISSIONS_DATASET2_FILE_NAME)
        self._build_covid_dataset()

    def _load_infections_and_mortalities(self, *csv_paths: str):
        """
        Reads in the two parts of the infections and mortalities data and concats them into one single dataset
        param *csv_paths: csv paths to the csv resources that have to be read in and concatenated

        Happy path
        pre: *csv_paths are valid csv resources
        post: the infections and mortalities dataset is read in correctly based on the csv resources

        1: csv resource file is valid and exists
        >>> CovidDataProvider._load_infections_and_mortalities(CovidDataProvider,'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames_tm_03102021.csv')


        Pre broken path
        1: csv resource(s) does not exist
            raises HTTPError
        >>> CovidDataProvider._load_infections_and_mortalities(CovidDataProvider,'https://data.rivm.nl/data/covid-19/COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv_wrong_url')
        Traceback (most recent call last):
        ...  raise HTTPError(req.full_url, code, msg, hdrs, fp)
        urllib.error.HTTPError: HTTP Error 404: Not Found
        """
        infections_and_mortalities_datasets = [pd.read_csv(csv_path, delimiter=';',  encoding='utf8') for csv_path in csv_paths]
        self.infections_and_mortalities = self._concat_dataframes(infections_and_mortalities_datasets)

    def _load_hospital_admissions(self, *csv_paths: str):
        """
        Reads in the two parts of the hospital admissions data, concats them into one single dataset and renames the date column
        param *csv_paths: csv paths to the csv resources that have to be read in and concatenated

        Happy path
        pre: *csv_paths are valid csv resources
        post: the hospital admissions dataset is read in correctly based on the csv resources

        1: csv resource file is valid and exists
        >>> CovidDataProvider._load_hospital_admissions(CovidDataProvider,'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames_tm_03102021.csv')

        Pre broken path
        1: csv resource(s) does not exist
            raises HTTPError
        >>> CovidDataProvider._load_hospital_admissions(CovidDataProvider,'https://data.rivm.nl/data/covid-19/COVID-19_ziekenhuisopnames_tm_03102021.csv_wrong_url')
        Traceback (most recent call last):
        ...  raise HTTPError(req.full_url, code, msg, hdrs, fp)
        urllib.error.HTTPError: HTTP Error 404: Not Found
        """

        hospital_admissions_datasets = [pd.read_csv(csv_path, delimiter=';',  encoding='utf8') for csv_path in csv_paths]
        self.hospital_admissions = self._concat_dataframes(hospital_admissions_datasets)
        self.hospital_admissions.rename(columns={'Date_of_statistics': 'Date_of_publication'}, inplace=True)

    def get_dataset(self) -> pd.DataFrame:
        """
        Returns the build and cleaned covid dataset containing the infections, mortalities and hospital admissions
        """
        return self.covid_dataset


    @staticmethod
    def _concat_dataframes(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
        """
        concatenates multiple dataframes into one single dataframe
        param *datasets: dataframes that have to be concatenated
        return: the concatenated dataframe
        """

        return pd.concat(dataframes, ignore_index=True)

    @staticmethod
    def _drop_intermediary_rows(dataset: pd.DataFrame) -> pd.DataFrame:
        """
        The covid csv files contains intermediary rows to indicate when a new date starts, these rows are of no use
        to the program and thus have to be deleted, such a row is detected if the municipality name is not filled in
        param dataset: the dataframe where the intermediary rows have to be deleted
        return: a clean pandas dataframe without intermediary date rows

        Happy path:
        pre: the dataframe contains a column with the name Municipality_name
        post: the dataframe doesn't contain any intermediary rows anymore

        1: dataframe does contain any Municiipality_name column
        >>> CovidDataProvider._drop_intermediary_rows(pd.DataFrame([[3, 1, 4, 1]], columns=['test1', 'test2', 'Municipality_name', 'test4']))

        Pre broken path:
        1: dataframe doesn't contain column Municipality_name
            raises KeyError
        >>> CovidDataProvider._drop_intermediary_rows(pd.DataFrame([[3, 1, 4, 1]], columns=['test1', 'test2', 'test5', 'test4']))
        Traceback (most recent call last):
        ...  raise KeyError(np.array(subset)[check].tolist())
        KeyError: ['Municipality_name']
        """

        dataset.dropna(subset=['Municipality_name'], inplace=True)

    def _build_covid_dataset(self):
        """
        Build the covid dataset from the read in csv's by performing:
        1: preprocessing operations
        2: merging infections and mortalities and hospital admissions
        3: postprocessing operations

        Happy path
        pre: the infections and mortalities dataset exists and the merge columns exits
        post: the covid_dataset is build

        Pre broken path:
        1: the columns to merge the 2 datasets doesn't exist
            raise AttributeError
        """

        if not(set(self._MERGE_COLUMNS).issubset(self.infections_and_mortalities)):
            raise AttributeError("Merge columns not present on infections and mortalities")

        if not(set(self._MERGE_COLUMNS).issubset(self.hospital_admissions)):
            raise AttributeError("Merge columns not present on hospital_admissions")

        self._clean_infections_and_mortalities_dataset()
        self._clean_hospital_admissions_dataset()
        self.covid_dataset = pd.merge(self.infections_and_mortalities, self.hospital_admissions, on=self._MERGE_COLUMNS, how='left')
        self._clean_covid_dataset()

    def _fill_missing_municipalities(self):
        """
        Municipality name is a grouping columns that can be empty,
        To avoid incomplete data we fill in the empty municipality names by '[Province] gemeente onbekend'

        Happy path
        pre: the dataframe exists and the municipality name column exists
        post: all empty municipality names get filled in by the default value

        Pre broken path

        1: the dataframe does not contain a Municipality name, Province column
        Raise AttributeError
        """

        if not('Municipality_name' in self.infections_and_mortalities):
            raise AttributeError('No attribute Municipality_name')

        if not('Province' in self.infections_and_mortalities):
            raise AttributeError('No attribute Province')

        self.infections_and_mortalities.Municipality_name.fillna(self.infections_and_mortalities.Province + ' gemeente onbekend', inplace=True)

    def _clean_infections_and_mortalities_dataset(self):
        """
        Cleans the infections and mortalities dataset before merging
        1: the missing municipalities are defaulted
        2: the intermediary rows are deleted
        3: the columns that are not used get dropped
        4: the dataset gets summed by date, province and municipality

        Happy path:
        pre: The infections_and_mortalities dataset exist, the columns to get dropped exist and the columns to sum over exist on the dataset
        post: The dataset is cleaned as defined in the checks above

        Pre broken path:
        1: the columns to drop does not exist
            raises AttributeError
        2: the columns to sum over on does not exist
        """
        self._fill_missing_municipalities()
        self._drop_intermediary_rows(self.infections_and_mortalities)

        columns_to_drop = [
            'Version',
            'Date_of_report',
            'Municipality_code',
            'Security_region_code',
            'Security_region_name',
            'Municipal_health_service',
            'ROAZ_region',
        ]
        grouping_columns = ['Date_of_publication', 'Province', 'Municipality_name']

        if not(set(columns_to_drop).issubset(self.infections_and_mortalities.columns)):
            raise AttributeError('Columns to drop not in dataset')

        self.infections_and_mortalities.drop(columns=columns_to_drop, inplace=True)

        if not(set(grouping_columns).issubset(self.infections_and_mortalities.columns)):
            raise AttributeError('grouping columns not in dataset')

        self.infections_and_mortalities = self.group_by(self.infections_and_mortalities, grouping_columns)

    def _clean_hospital_admissions_dataset(self):
        """
            Cleans the infections and mortalities dataset before merging
            1: the intermediary rows are deleted
            3: the columns that are not used get dropped
            4: the dataset gets summed by date and municipality

            Happy path:
            pre: The hospital_admissions dataset exist, the columns to get dropped exist and the columns to sum over exist on the dataset
            post: The dataset is cleaned as defined in the checks above

            Pre broken path:
            1: the columns to drop does not exist
                raises AttributeError
            2: the columns to sum over on does not exist
                raises AttributeError
            """
        self._drop_intermediary_rows(self.hospital_admissions)

        columns_to_drop = [
            'Version',
            'Date_of_report',
            'Municipality_code',
            'Security_region_code',
            'Security_region_name',
            'Hospital_admission_notification',
        ]

        grouping_columns = ['Date_of_publication', 'Municipality_name']

        if not(set(columns_to_drop).issubset(self.hospital_admissions.columns)):
            raise AttributeError('Columns to drop not in dataset')

        self.hospital_admissions.drop(columns=columns_to_drop, inplace=True)

        if not(set(grouping_columns).issubset(self.hospital_admissions.columns)):
            raise AttributeError('grouping columns not in dataset')

        self.hospital_admissions = self.group_by(self.hospital_admissions, grouping_columns=grouping_columns)

    def _clean_covid_dataset(self):
        """
        Cleans the covid dataset, sets the na hospital admissions to 0, converts the date_of_publication to a datetime column and adds year and month columns
        """
        self.group_by(self.covid_dataset, self._MERGE_COLUMNS)
        self.covid_dataset.Hospital_admission.fillna(0, inplace=True)
        self.covid_dataset.Date_of_publication = pd.to_datetime(self.covid_dataset.Date_of_publication)
        self.covid_dataset['Year'] = self.covid_dataset.Date_of_publication.dt.strftime('%Y')
        self.covid_dataset['Month'] = self.covid_dataset.Date_of_publication.dt.strftime('%B')
    
    @staticmethod
    def group_by(dataset: pd.DataFrame, grouping_columns: list[str], as_index: bool = False, numeric_only: bool = True) -> pd.DataFrame:
        """
        Groups the dataframe by the columns defined in the grouping_columns parameter
        param as_index: weather the grouping_columns has to be set as index for the new dataframe
        param numeric_only: weather the grouping has to be performed only on numeric values
        return: the grouped dataframe

        Happy path
        pre: The dataset contains the columns defined in the grouping_columns parameter
        post: the dataframe is grouped by the grouping_columns

        >>> CovidDataProvider.group_by(pd.DataFrame([[3, 1, 4, 1],[3, 2, 5, 2],[3, 3, 6, 3]], columns=['test1', 'test2', 'test3', 'test4']), grouping_columns=['test1'])
           test1  test2  test3  test4
        0      3      6     15      6

        Pre broken path

        1: The columns to be grouped do not exist
            raise AttributeError

        >>> CovidDataProvider.group_by(pd.DataFrame([[3, 1, 4, 1],[3, 2, 5, 2],[3, 3, 6, 3]], columns=['test1', 'test2', 'test3', 'test4']), grouping_columns=['test12345'])
        Traceback (most recent call last):
        ... raise AttributeError('Columns not in dataset')
        AttributeError: Columns not in dataset

        """

        if not(set(grouping_columns).issubset(dataset.columns)):
            raise AttributeError('Columns not in dataset')

        return dataset.groupby(by=grouping_columns, as_index=as_index).sum(numeric_only=numeric_only)

    @staticmethod
    def filter_by_year(dataset: pd.DataFrame, year: int) -> pd.DataFrame:
        """
        Filters the dataset based on the year column
        param dataset: The dataset to filter
        param year: the term to filter on
        returns all the rows of the dataset that matches the filter term

        Happy path:
        pre: the dataframe contains a column with the name year
        post: the dataframe contains only rows with column value that matches the search term

        Pre broken path:
        1: dataframe doesn't contain column Date_of_publication
            raises KeyError
        >>> CovidDataProvider.filter_by_year(pd.DataFrame([[3, 1, 4, 1]], columns=['test1', 'test2', 'test3', 'test4']), 2022)
        Traceback (most recent call last):
        ... ... raise AttributeError('No attribute Date_of_publication')
        AttributeError: No attribute Date_of_publication
        """

        if 'Date_of_publication' not in dataset:
            raise AttributeError('No attribute Date_of_publication')

        return dataset[dataset.Date_of_publication.dt.year == year]

    @staticmethod
    def filter_by_province(dataset: pd.DataFrame, province: str) -> pd.DataFrame:
        """
        Filters the dataset based on the Province column
        param dataset: The dataset to filter
        param province: the term to filter on
        return: all the rows of the dataset that matches the filter term

        Happy path:
        pre: the dataframe contains a column with the name province
        post: the dataframe contains only rows with column value that matches the search term

        Pre broken path:
        1: dataframe doesn't contain column Province
            raises AttributeError
        >>> CovidDataProvider.filter_by_province(pd.DataFrame([[3, 1, 4, 1]], columns=['test1', 'test2', 'test3', 'test4']),'test_province')
        Traceback (most recent call last):
        ... raise AttributeError('No attribute Province')
        AttributeError: No attribute Province
        """

        if 'Province' not in dataset:
            raise AttributeError('No attribute Province')

        return dataset[dataset.Province.str.lower() == province.lower()]



