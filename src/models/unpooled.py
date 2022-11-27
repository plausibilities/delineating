"""
Module unpooled
"""
import logging

import pandas as pd
import pymc as pm


class Unpooled:
    """
    Class: Unpooled
    """

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

        :param data:
        :return:
        """

        with pm.Model(coords=self.__coords) as model:

            # the values of the <floor> field
            levelcode = pm.Data(name='levelcode', value=data['floor'].values, dims='N', mutable=True)
            self.__logger.info(levelcode.get_value().shape)
            self.__logger.info(levelcode.type())

            # the values of the <countyindex> field
            countyindex = pm.Data(name='countyindex', value=data['countyindex'].values, dims='N', mutable=True)
            self.__logger.info(countyindex.get_value().shape)
            self.__logger.info(countyindex.type())

            # <measures> is probably has 85 x 2 elements because there are 85 distinct counties w.r.t. MN, and 2 distinct
            # dwelling/floor levels.  Hence, 85 x 2 random values from a normal distribution
            measures = pm.Normal(name='measures', mu=0.0, sigma=10.0, dims=('County', 'Level'))
            self.__logger.info(type(measures))
            self.__logger.info(f'The county & level groups: {measures.eval().shape}')

            # shape(mu) === shape(levelcode): <levelcode> is a N x 1 boolean object
            mu = measures[countyindex, levelcode]
            self.__logger.info('The shape of mu: %s', mu.eval().shape)

            # sigma ~ pm.Exponential(name=, lam=)
            sigma = pm.Exponential('sigma', 1.0)
            y = pm.Normal('y', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(y)

            return model

    def exc(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data:
        :return:
        """

        # A Bayesian model: complete pooling
        model = self.__model(data=data)

        # Is this the correct seeding method/approach?
        model.initial_point(seed=self.__seed)

        return model
