Installation
============
Requirements
------------
Huginn requires the following Python packages to be installed on your system.

- requests >= 2.7.0
- Twisted >= 15.3.0

Huginn also requires that you have installed the JSBsim flight dynamics model library. You can download this
from http://jsbsim.sourceforge.net/.

The simulator can be installed by downloading the source code and running the following commands on the console.

.. code-block:: bash

    python setup.py build_ext install

Testing
-------
Go to the source code directory and run the tests with the following command.

.. code-block:: bash

    ./run_tests.sh

A Robot test suite also exists. This can be run by entering the robot directory and
using the following command.

.. code-block:: bash

    pybot regression.txt

Documentation
-------------
The documentation can be build using Sphinx. Go to the *docs* directory and run the following command to create 
the html documentation

.. code-block:: bash

    make html 
    
The documentation will be in the *build/html* directory.