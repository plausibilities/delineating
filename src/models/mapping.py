"""
Module: mapping
"""
import arviz as az
import xarray as xr


class Mapping:
    """
    Class: Mapping
    """

    def __init__(self, inferences: az.InferenceData, coords: dict):
        """

        :param inferences:
        :param coords:
        """

        self.__inferences = inferences
        self.__coords = coords

    def __posterior(self) -> xr.Dataset:
        """

        :return:
        """

        posterior = self.__inferences['posterior'].assign_coords(LevelCode=list(self.__coords['Level'].values()))

        return posterior

    def __observed_data(self) -> xr.Dataset:
        """

        :return:
        """

        labels = self.__inferences['posterior']['Level'][self.__inferences['constant_data']['levelcode']]

        observed_data = self.__inferences['observed_data'].assign_coords(Level=labels)
        observed_data = observed_data.assign_coords(LevelCode=self.__inferences['constant_data']['levelcode'])
        observed_data = observed_data.sortby('LevelCode')

        return observed_data

    def exc(self) -> az.InferenceData:
        """

        :return:
        """

        inferences = self.__inferences.copy()
        inferences.posterior = self.__posterior()
        inferences.observed_data = self.__observed_data()

        return inferences
