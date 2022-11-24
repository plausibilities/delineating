import pandas as pd
import numpy as np

import src.data.coordinates


class Vectors:

    def __init__(self):
        """

        """

    @staticmethod
    def exc(data: pd.DataFrame) -> pd.DataFrame:
        """

        :return:
        """

        # coordinates
        coordinates = src.data.coordinates.Coordinates(data=data).exc()
        dictionary = coordinates['County']

        # extra features
        data.loc[:, 'ln_radon'] = np.log(data['activity'] + 0.1)
        data.loc[:, 'countyindex'] = data['county'].replace(dictionary)

        return data
