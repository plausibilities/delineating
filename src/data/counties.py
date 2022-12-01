import pandas as pd
import pymc as pm


class Counties:

    def __init__(self):
        """

        """

    @staticmethod
    def __read() -> pd.DataFrame:

        try:
            counties = pd.read_csv(filepath_or_buffer=pm.get_data('cty.dat'))
        except FileNotFoundError as err:
            raise Exception(err.strerror)

        # the state + county FIPS codes
        counties.loc[:, 'fips'] = counties.stfips.astype(str).str.zfill(2) + counties.ctfips.astype(str).str.zfill(3)

        return counties

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        return self.__read()
