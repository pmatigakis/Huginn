Installation
============
Requirements
------------
Huginn requires that you have installed the JSBsim flight dynamics model library. You can download this
from http://jsbsim.sourceforge.net.

You must also install the Python bindings for JSBSim. You can download it from this Github repository.
https://github.com/pmatigakis/PyJSBSim

The simulator can be installed by downloading the source code and running the following commands on the console.

.. code-block:: bash

    python setup.py install

This will download the requirements, build the JSBSim python extension and install Huginn. It is recommended to use a
virtual environment to install Huginn.

Testing
-------
You can execute the unit tests with the following command.  

.. code-block:: bash

    python setup.py nosetests

A Robot test suite also exists. This can be run by entering the robot directory and
using the following command.

.. code-block:: bash

    ./run_robot.sh

Documentation
-------------
The documentation can be build using Sphinx. Go to the *docs* directory and run the following command to create 
the html documentation

.. code-block:: bash

    make html 
    
The documentation will be in the *build/html* directory.