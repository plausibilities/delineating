import pandas as pd


class Coordinates:

    def __init__(self, data: pd.DataFrame):
        """

        """

        self.data = data

    @staticmethod
    def __levels() -> dict:

        levels = ['Basement', 'Ground']
        indices = range(len(levels))

        return dict(zip(levels, indices))

    def __counties(self) -> dict:

        counties = self.data['county'].unique()
        indices = range(len(counties))

        return dict(zip(counties, indices))

    def exc(self) -> dict:

        coordinates = {'Level': self.__levels(), 'County': self.__counties()}

        return coordinates
