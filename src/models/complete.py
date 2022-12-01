import logging

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

    def __model(self, data: pd.DataFrame) -> pm.Model:
        """

        :param data:
        :return:
        """

        with pm.Model(coords=self.__coords) as model:

            # The values of the <floor> field
            #   self.__logger.info(levelcode.get_value().shape), self.__logger.info(levelcode.type())
            levelcode = pm.Data(name='levelcode', value=data['floor'].values, dims='N', mutable=True)

            # The <measures> object has two elements because the object <Level> has two elements, therefore two random
            # values are taken from a normal distribution
            #   measures: aesara.tensor.var.TensorVariable
            measures = pm.Normal(name='measures', mu=0.0, sigma=10.0, dims='Level')
            self.__logger.info(f'The # of level group elements: {measures.eval().shape}')

            # shape(mu) === shape(levelcode): <levelcode> is a N x 1 boolean object
            #   measures.eval()[levelcode.eval()]
            mu = measures[levelcode]
            self.__logger.info('The shape of mu, whereby mu = measures[levelcode]: %s', mu.eval().shape)

            # sigma ~ pm.Exponential(name=, lam=)
            sigma = pm.Exponential('sigma', 1.0)

            # model
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
