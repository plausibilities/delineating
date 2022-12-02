
<br>

### Notes

Notebook: radon.ipynb

> ``develop branch`` <br> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plausibilities/delineating/blob/develop/notebooks/radon.ipynb)

> ``master branch`` <br> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plausibilities/delineating/blob/master/notebooks/radon.ipynb)


<br>

Metrics

* High Density Interval (A Credible Interval)
* [Monte Carlo Standard Error](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/MCSE.html)
* [Effective Sample Size](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/ESS.html)
* [Gelman and Rubin's MCMC Convergence Diagnostic $R$](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/Gelman.Diagnostic.html)

<br>
<br>

### Snippets

Dictionaries:

```python
levels = ['Basement', 'Ground']
x = {'Level': dict(zip(levels, range(len(levels))))}
len(x.get('Level'))
```


Aesara:

```python 
logger.info(aesara.tensor.shape(...).eval())
```


PyMC Structures:

````python
import pymc
import numpy as np

ones = pymc.Data(name=str(''), value=np.ones(shape=...), dims='N', mutable=False)
alpha = pymc.Normal(str('alpha'), mu=0.0, sigma=10.0)

mu = (alpha * ones) + ...
````



<br>
<br>

### References

* [Engineering Statistics Handbook](https://www.itl.nist.gov/div898/handbook/)
* [A Primer on Bayesian Methods for Multilevel Modeling](https://www.pymc.io/projects/examples/en/latest/case_studies/multilevel_modeling.html)
* [Multilevel Modeling Primer in TensorFlow Probability](https://www.tensorflow.org/probability/examples/Multilevel_Modeling_Primer)  
* [Interesting Case Studies](https://psmits.github.io/paleo_book/varying-intercept-models.html)  
* [PYMC API](https://www.pymc.io/projects/docs/en/stable/api/model.html)  
  * [The PYMC Samplers](https://docs.pymc.io/en/latest/api/samplers.html)
* [ARVIZ API](https://arviz-devs.github.io/arviz/api/)
  * [arviz.plot_ppc](https://arviz-devs.github.io/arviz/api/generated/arviz.plot_ppc.html)
  * [arviz.InferenceData methods](https://arviz-devs.github.io/arviz/api/generated/arviz.InferenceData.html)
* Graphing
  * [seaborn.boxplot](https://seaborn.pydata.org/generated/seaborn.boxplot.html)
  * [maxplotlib.axes.Axes.boxplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html#matplotlib.axes.Axes.boxplot)
* [pandas API](https://pandas.pydata.org/docs/reference/index.html)
* [NumPy API](https://numpy.org/doc/stable/reference/index.html)
* [``xarray`` API](https://docs.xarray.dev/en/stable/api.html)
* JupyterLab
  * [Documentation](https://jupyterlab.readthedocs.io/en/stable/)
  * [API](https://jupyterlab.readthedocs.io/en/stable/api/index.html)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
