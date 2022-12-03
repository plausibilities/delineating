"""
Module: frequencies
"""
import pandas as pd


class Frequencies:
    """
    Class: Frequencies

    Observations counts w.r.t. (with respect to) a field, and sometimes categories.
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def county(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data: The Radon data set, or an excerpt of it
        :return:
        """

        frequencies = data[['county', 'countyindex', 'floor']].groupby(by=['county', 'countyindex', 'floor'], sort=False).value_counts()
        frequencies.rename('N', inplace=True)
        frequencies = frequencies.to_frame()
        frequencies.reset_index(drop=False, inplace=True)

        return frequencies
