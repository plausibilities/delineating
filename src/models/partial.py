import logging

import pandas as pd
import pymc as pm


class Partial:

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

            # The values of the <countyindex> field
            #   self.__logger.info(countyindex.get_value().shape), self.__logger.info(countyindex.type())
            countyindex = pm.MutableData(name='countyindex', value=data['countyindex'].values, dims='N')

            # Random intercepts
            mu_ = pm.Normal('intercept.mu', mu=0.0, sigma=10)
            sigma_ = pm.Exponential('intercept.sigma', 1)
            intercepts = pm.Normal('intercepts', mu=mu_, sigma=sigma_, dims='County')

            # Model expected value
            mu = intercepts[countyindex]
            self.__logger.info('The shape of mu, whereby mu = intercepts[countyindex]: %s', mu.eval().shape)

            # Model error
            # sigma ~ pm.Exponential(name=, lam=)
            sigma = pm.Exponential('sigma', 1)

            # Likelihood
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(likelihood)

            return model

    def exc(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data: The data set being modelled.
        :return:
        """

        # A Bayesian model: hierarchical modelling, partial pooling
        model = self.__model(data=data)

        # Is this the correct seeding method/approach?
        model.initial_point(seed=self.__seed)

        return model
