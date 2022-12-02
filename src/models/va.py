import logging

import pandas as pd
import pymc as pm


class VA:

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

            levelcode = pm.MutableData(name='levelcode', value=data['floor'].values, dims='N')
            countyindex = pm.MutableData(name='countyindex', value=data['countyindex'].values, dims='N')

            # Random intercepts
            intercept_mu = pm.Normal('intercept.mu', mu=0.0, sigma=10.0)
            intercept_sigma = pm.Exponential('intercept.sigma', 1.0)
            intercepts = pm.Normal('intercepts', mu=intercept_mu, sigma=intercept_sigma, dims='County')

            # Random gradients
            gradient_mu = pm.Normal('gradient.mu', mu=0.0, sigma=10.0)
            gradient_sigma = pm.Exponential('gradient.sigma', 1.0)
            gradients = pm.Normal('gradients', mu=gradient_mu, sigma=gradient_sigma, dims='County')

            # Expected value
            mu = intercepts[countyindex] + gradients[countyindex] * levelcode

            # Model error
            sigma = pm.Exponential('sigma', 1.0)

            # Likelihood
            likehood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')

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
