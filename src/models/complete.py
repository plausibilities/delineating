import logging
import collections

import pandas as pd
import pymc as pm


class Complete:

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

        # Results collection object
        collections.namedtuple(typename='Model', field_names=[])

    def __model(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        with pm.Model(coords=self.__coords) as model:

            # the values of the <floor> field
            levelcode = pm.Data(name='levelcode', value=data['floor'].values, dims='N', mutable=True)
            self.__logger.info(levelcode.get_value().shape)
            self.__logger.info(levelcode.type())

            # <apriori> probably two elements because the object <Level> has two elements, therefore two random
            # values from a normal distribution
            apriori = pm.Normal(name='apriori', mu=0.0, sigma=10.0, dims='Level')

            # shape(mu) === shape(levelcode): <levelcode> is a N x 1 boolean object
            mu = apriori[levelcode]

            # sigma ~ pm.Exponential(name=, lam=)
            sigma = pm.Exponential('sigma', 1.0)

            # model
            y = pm.Normal('y', mu=mu, sigma=sigma, observed=data['ln_radon'].values, dims='N')
            self.__logger.info(y)

            return model

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        model = self.__model(data=data)
        model.initial_point(seed=self.__seed)

        return model
