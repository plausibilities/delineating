import pandas as pd
import pymc as pm

import src.data.counties


class Radioactivity:

    def __init__(self):
        """

        """

    @staticmethod
    def __read() -> pd.DataFrame:

        try:
            data = pd.read_csv(filepath_or_buffer=pm.get_data('srrs2.dat'))
        except FileNotFoundError as err:
            raise Exception(err.strerror)

        # ascertaining field name consistency
        data.rename(mapper=str.strip, axis='columns', inplace=True)

        return data

    @staticmethod
    def __structure(data: pd.DataFrame) -> pd.DataFrame:
        """
        Structuring; concatenating the `pure state` & `pure county` codes
            1. FIPS States: https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code
            2. FIPS Counties: https://en.wikipedia.org/wiki/List_of_United_States_FIPS_codes_by_county

        :param data:
        :return:
        """

        # the state + county FIPS codes
        data.loc[:, 'fips'] = data.stfips.astype(str).str.zfill(2) + data.cntyfips.astype(str).str.zfill(3)
        data.loc[:, 'county'] = data['county'].str.strip().str.upper()

        return data

    @staticmethod
    def __merge(data: pd.DataFrame) -> pd.DataFrame:
        """
        Merge dwelling & county level [uranium] data.

        :param data:
        :return:
        """

        counties = src.data.counties.Counties().exc()
        data = data.merge(counties[['fips', 'Uppm']], how='left', on='fips')

        return data

    def exc(self, state: str = None):
        """

        :param state:
        :return:
        """

        # the data
        data = self.__read()
        data = self.__structure(data=data.copy())
        data = self.__merge(data=data.copy())

        # focusing on a single state?
        if state is not None:
            data = data.copy().loc[data['state'] == state, :]

        # deduplicate
        data.drop_duplicates(inplace=True)

        return data