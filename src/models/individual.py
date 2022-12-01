import logging

import pandas as pd
import pymc as pm


class Individual:

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

            # The values of the <floor> field
            #   self.__logger.info(levelcode.get_value().shape)
            levelcode = pm.Data(name='levelcode', value=data['floor'].values, dims='N', mutable=False)

            # Common intercept
            alpha = pm.Normal('alpha', mu=0.0, sigma=10.0)

            # Common gradient
            beta = pm.Normal('beta', mu=0.0, sigma=10.0)

            # Model expected value
            mu = alpha + (beta * levelcode)

            # Model error
            # sigma ~ pm.Exponential(name=, lam=)
            sigma = pm.Exponential('sigma', 1.0)

            # Likelihood
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(likelihood)

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
