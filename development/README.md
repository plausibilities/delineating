<br>

Development Environment Notes

<br>

### Development Environment

The requirements file generation is via

```shell
  conda activate uncertainty
  pip freeze -r docs/filter.txt > requirements.txt
```

Whilst

```shell
  pylint --generate-rcfile > .pylintrc
```

generates the dotfile that ``pylint`` - the static code analyser - uses for code analysis.

<br>

Libraries

> ``arviz.__version__``
> 
> ``pymc.__version__``
> 
> ``numpy.__version__``


<br>
<br>

### Snippets

Updating dictionaries:

````python
A = {'ArgCholeskyDeviations': ['intercept', 'gradient'], 
     'ArgCholeskyCorrelations': ['intercept', 'gradient']}
B = {'Level': ['Basement', 'Ground'], 
     'County': {'AITKIN': 0, 'ANOKA': 1, 'BECKER': 2, 'BELTRAMI': 3, 'BENTON': 4, 'BIG STONE': 5}}

for key in B.keys():
    if key not in A.keys():
        A.update({key: B[key]})
````

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
