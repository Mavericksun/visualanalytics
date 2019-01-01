Title: Install pyfmi with python3 compatibility
Date: 2018-05-09 10:50
Category: Misc
Slug: install-pyfmi-with-python3-compatibility
Authors: Qiang Chen

In order to be able to use the FMU API, you should have the `pyfmi` package
installed beforehand. However, at the point of writing this article, the
default version you can find on [PyPI](https://pypi.org/project/PyFMI/), is
only compatible with Python 2.7. This means that if you try to install `pyfmi`
with `pip install pyfmi` directly, and you are using Python 3.6 as recommended
by DAL.

Luckily, if you have the Anaconda suite installed, it also has another package
manager `conda`. In the anaconda hosted website, there is a precompiled binary
version of `pyfmi`, which can be directly installed by `conda`.

Just like you need to specify proxy when using the `pip` command for connecting
the external Internet, there is also some configuration needed for conda as
well. You need to create a file named as `.condarc` in your home directory,
e.g. `C:\Users\<your user name>`, with the following content:

```cmd
channels:
  - conda-forge
  - defaults

proxy_servers:
  http: http://172.28.41.32:8080
  https: https://172.28.41.32:8080
ssl_verify: true
```
