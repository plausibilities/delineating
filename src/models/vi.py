import logging

import pandas as pd
import pymc as pm


class VI:

    def __init__(self, coords: dict, seed: int):
        """

        :param coords: Inference Data Coordinates
        :param seed: Modelling seed
        """

        self.__coords = coords
        self.__seed = seed

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __model(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data:The data set being modelled.
        :return:
        """

        with pm.Model(coords=self.__coords) as model:

            pm.Data(name='levelcode', value=data['floor'].values, dims='N', mutable=True)

            return model

    def exc(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data: The data set being modelled.
        :return:
        """

        # A Bayesian model: a varying intercept model
        model = self.__model(data=data)

        # Is this the correct seeding method/approach?
        model.initial_point(seed=self.__seed)

        return model
