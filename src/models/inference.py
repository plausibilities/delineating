"""
Module: inference
"""
import pymc as pm
import arviz as az


class Inference:
    """
    Class: Inference
    """

    def __init__(self, model: pm.Model):
        """
        ref. https://docs.pymc.io/en/latest/api/generated/pymc.Model.html

        :param model:
        """

        self.__model = model

    def __sample_prior_predictive(self) -> az.InferenceData:
        """
        ref. https://docs.pymc.io/en/latest/api/generated/pymc.sample_prior_predictive.html

        :return:
        """

        with self.__model:
            inferences = pm.sample_prior_predictive()

        return inferences

    def __sample_posterior_predictive(self, trace: az.InferenceData) -> az.InferenceData:
        """
        ref. https://docs.pymc.io/en/latest/api/generated/pymc.sample_posterior_predictive.html

        :param trace:
        :return:
        """

        with self.__model:
            inferences = pm.sample_posterior_predictive(trace=trace)

        return inferences

    def __sample(self) -> az.InferenceData:
        """
        ref. https://docs.pymc.io/en/latest/api/generated/pymc.sample.html

        :return:
        """

        with self.__model:
            # these are default sample settings
            trace = pm.sample(draws=1000, cores=None, tune=1000)

        return trace

    def exc(self):
        """

        :return:
        """
