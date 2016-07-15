[![Build Status](https://travis-ci.org/pmatigakis/Huginn.svg?branch=master)](https://travis-ci.org/pmatigakis/Huginn)
[![codecov](https://codecov.io/gh/pmatigakis/Huginn/branch/master/graph/badge.svg)](https://codecov.io/gh/pmatigakis/Huginn)

Introduction
============
Huginn is a flight simulator designed for software-in-the-loop and
hardware-in-the-loop simulations.

This is in very early stage of development. Many features need improvements and
some of them might not work as intended.

![Huginn flight simulator](/docs/images/huginn.png?raw=true "Huginn flight simulator")

Installation
============
Before installing Huginn you must download JSBSim and it's Python bindings.
JSBSim can be downloaded from it's official web page at http://jsbsim.sourceforge.net
or from the unofficial mirror at https://github.com/pmatigakis/jsbsim.

It is a good idea to install Huginn in a virtual environment.

```bash
virtualenv --python=python2.7 virtualenv
source virtualenv/bin/activate
```

The Python bindings can be downloaded from https://github.com/pmatigakis/PyJSBSim

```bash
git clone git@github.com:pmatigakis/PyJSBSim.git
cd PyJSBSim
python setup.py build_ext install    
```

Clone the Huginn repository and install it

```bash
git clone git@github.com:pmatigakis/Huginn.git
cd Huginn
python setup.py install
```

Run the tests to check if everything was installed correctly

```bash
python setup.py test
```

Running
=======
Huginn is started using the *huginn_start* command

```bash
huginn_start
```

By default the simulator will start paused with the aircraft in the air. You can
view the web front-end by connecting with your browser to http://localhost:8090/

Documentation
=============
You can find more information about the simulator and how to use it by reading
the documentation. First you have to build the documentation. This step requires
that you have Sphinx installed

```bash
cd docs
make html
```

With your browser open the file */docs/build/html/index.html*

License
=======
This software package is released under the BSD 3-Clause License except some of the
included third party components that fall under the licenses specified by their
owners. 

Third party components
======================
The web interface of Huginn is using the jQuery Flight Indicators by Sébastien Matton.

jQuery Flight Indicators: https://github.com/sebmatton/jQuery-Flight-Indicators  

The Rascal JSBSim aircraft model used by the simulator is taken from the PX4 autopilot

PX4 HIL: https://github.com/PX4/HIL
