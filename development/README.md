<br>

Development Environment Notes

<br>

### Development Environment

The requirements file generation is via

```shell
  conda activate augmentation
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

<br>
<br>

<br>
<br>

<br>
<br>
