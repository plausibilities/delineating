import logging

import aesara.tensor as at
import pandas as pd
import pymc as pm


class MRVA:

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

            # deviations
            deviations_mvn = pm.Exponential('deviations_mvn', 0.5, shape=(2,))
            cholesky, correlations,deviations = pm.LKJCholeskyCov('cholesky', n=2, eta=2.0, sd_dist=deviations_mvn)

            # averages
            averages_mvn = pm.Normal('averages_mvn', mu=0.0, sigma=5.0, shape=2)

            # population varying effects
            structure = pm.Normal('var', 0.0, 1.0, dims=('ArgCholeskyDeviations', 'County'))
            effects = pm.Deterministic('effects', var=at.dot(cholesky, structure), dims=('County','ArgCholeskyDeviations'))

            # expected value
            mu = (averages_mvn[0] + effects[countyindex, 0] +
                  (averages_mvn[1] + effects[countyindex, 1]) * levelcode)

            # Model error
            sigma = pm.Exponential('sigma', 1.0)

            # Likelihood
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(likelihood)

            return model

    def exc(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data: The data set being modelled.
        :return:
        """

        # A Bayesian model: a varying intercept varying gradient model wherein we have
        # a multivariate Gaussian distribution of the intercepts & gradients; and, with
        # non-centred parameters.
        model = self.__model(data=data)

        # Is this the correct seeding method/approach?
        model.initial_point(seed=self.__seed)

        return model
