"""
Module: mapping
"""
import arviz as az
import xarray as xr


class Mapping:
    """
    Class: Mapping

    Notes:
        https://docs.xarray.dev/en/stable/api.html
        https://docs.xarray.dev/en/stable/generated/xarray.Dataset.assign_coords.html#xarray.Dataset.assign_coords
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

        posterior = self.__inferences['posterior']

        if 'Level' in  list(self.__inferences['posterior'].coords.keys()):
            posterior = posterior.assign_coords(LevelCode=list(self.__coords['Level'].values()))

        if 'County' in  list(self.__inferences['posterior'].coords.keys()):
            posterior = posterior.assign_coords(CountyIndex=list(self.__coords['County'].values()))

        return posterior

    def __observed_data(self) -> xr.Dataset:
        """

        :return:
        """

        observed_data = self.__inferences['observed_data']

        # The dwelling levels & labels
        if 'levelcode' in list(self.__inferences['constant_data'].variables.keys()):
            labels = self.__inferences['posterior']['Level'][self.__inferences['constant_data']['levelcode']]
            observed_data = observed_data.assign_coords(Level=labels)
            observed_data = observed_data.assign_coords(LevelCode=self.__inferences['constant_data']['levelcode'])

            # Sort, arrange, by level
            observed_data = observed_data.sortby('LevelCode')

        # The county indices & labels
        if 'countyindex' in list(self.__inferences['constant_data'].variables.keys()):
            labels = self.__inferences['posterior']['County'][self.__inferences['constant_data']['countyindex']]
            observed_data = observed_data.assign_coords(County=labels)
            observed_data = observed_data.assign_coords(CountyIndex=self.__inferences['constant_data']['countyindex'])

        return observed_data

    def exc(self) -> az.InferenceData:
        """

        :return:
        """

        inferences = self.__inferences.copy()
        inferences.posterior = self.__posterior()
        inferences.observed_data = self.__observed_data()

        return inferences
