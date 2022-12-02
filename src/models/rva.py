import logging

import pandas as pd
import pymc as pm


class RVA:

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
            # Centred:
            #       pm.Normal('intercepts', mu=intercept_mu, sigma=intercept_sigma, dims='County')
            # Non-centred:
            #       pm.Deterministic('intercepts', intercept_mu + (intercept_parameters * intercept_sigma), dims='County')
            intercept_mu = pm.Normal('intercept.mu', mu=0.0, sigma=10.0)
            intercept_sigma = pm.Exponential('intercept.sigma', 5.0)
            intercept_parameters = pm.Normal('intercept.parameters', mu=0, sigma=1, dims='County')
            intercepts = pm.Deterministic('intercepts', intercept_mu + (intercept_parameters * intercept_sigma), dims='County')

            # Random gradients
            gradient_mu = pm.Normal('gradient.mu', mu=0.0, sigma=10.0)
            gradient_sigma = pm.Exponential('gradient.sigma', 1.0)
            gradients = pm.Normal('gradients', mu=gradient_mu, sigma=gradient_sigma, dims='County')

            # Expected value
            mu = intercepts[countyindex] + gradients[countyindex] * levelcode

            # Model error
            sigma = pm.Exponential('sigma', 1.0)

            # Likelihood
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(likelihood)

            return model
