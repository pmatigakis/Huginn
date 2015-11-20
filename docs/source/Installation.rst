Installation
============
Requirements
------------
Huginn requires the following Python packages to be installed on your system.

- requests >= 2.7.0
- Twisted >= 15.3.0

Huginn also requires that you have installed the JSBsim flight dynamics model library. You can download this
from http://jsbsim.sourceforge.net/. After you install JSBsim you must create an environment variable
named JSBSIM_HOME that points to the directory of the JSBSim source code.

You also need to download and install the JSBSim Python binding from the following Github page

https://github.com/pmatigakis/PyJSBSim

The simulator can be installed by downloading the source code and running the following commands on the console.

.. code-block:: bash

    python setup.py install

Testing
-------
In order to run the tests you will also need to install the following packages.

- coverage >= 3.7.1
- nose >= 1.3.7
- mock >= 1.3.0
- PyHamcrest >= 1.8.5

Go to the source code directory and run the tests with the following command.

.. code-block:: bash

    ./run_tests.sh

Documentation
-------------
The documentation can be build using Sphinx. Go to the *docs* directory and run the following command to create 
the html documentation

.. code-block:: bash

    make html 
    
The documentation will be in the *build/html* directory.