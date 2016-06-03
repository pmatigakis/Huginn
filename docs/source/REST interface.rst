REST interface
======================

Huginn has a REST interface that can be used to get information about the
simulation and the aircraft sensors as well as control the simulator.

The following endpoints are available

Sensors
-------

GET **/aircraft**

Returns the name of the aircraft. Currently only the rascal is available

.. code-block:: javascript

    {
        "aircraft_type": "Rascal"
    }  

GET **/aircraft/sensors/accelerometer**

Returns the accelerometer sensor measurements in meters/sec^2

.. code-block:: javascript

    {
        "y": 0.13182434306640045,
        "x": -2.554742567826436,
        "z": -8.265250834780698
    }

GET **/aircraft/sensors/gyroscope**

Returns the measurements from the gyroscope. The measurements will be in
degrees/sec

.. code-block:: javascript

    {
        "pitch_rate": -3.2365655923917513,
        "yaw_rate": 1.046958740868002,
        "roll_rate": 1.1552234891655875
    }

GET **/aircraft/sensors/thermometer**

Returns the temperature in Kelvins

.. code-block:: javascript

    {
        "temperature": 286.9437303264973
    }

GET **/aircraft/sensors/pressure_sensor**

Returns the atmospheric pressure in Pascals

.. code-block:: javascript

    {
        "static_pressure": 97867.13418249096
    }

GET **/aircraft/sensors/pitot_tube**

Returns the pressure measurement from the aircraft pitot tube in Pascals

.. code-block:: javascript

    {
        "total_pressure": 98318.97270037886
    }

GET **/aircraft/sensors/ins**

Returns the data from the aircrafts inertial navigation system

.. code-block:: javascript

    {
        "altitude": 310.9825444157268,
        "airspeed": 31.31915341070005,
        "longitude": 23.92204132322211,
        "heading": 47.9231793904896,
        "pitch": -2.222240986380215,
        "latitude": 37.9235159716135,
        "roll": 1.7642327847025083
    }

Instruments
-----------

GET **/aircraft/instruments/gps**

Returns the measurements from the gps module

.. code-block:: javascript

    {
        "latitude": 37.92343666537175,
        "altitude": 300.1070281313986,
        "airspeed": 27.577964685844144,
        "longitude": 23.922006458085477,
        "heading": 46.01929472213956
    }

Engine
------

GET **/aircraft/engine**

Returns information about the aircraft engine. The engine thrust is in newtons.
The throttle position is a value between 0.0 and 1.0

.. code-block:: javascript

    {
        "thrust": -5.207974004747296e-05,
        "throttle": 0.0
    }

Flight controls
---------------

GET **/aircraft/flight_controls**

Return the flight controls values. These values will be in the range -1.0 to
1.0 for the flight surfaces and 0.0 to 1.0 for the throttle

.. code-block:: javascript

    {
        "rudder": 0.0,
        "aileron": 0.0,
        "throttle": 0.0,
        "elevator": 0.0
    }

Simulator control
-----------------

GET **/simulator**

Return the state of the simulator

.. code-block:: javascript

    {
        "dt": 0.0033333333333333335,
        "running": false,
        "time": 1.0033333333333294
    }

Flight dynamics model
---------------------

GET **/fdm**

Return the flight dynamics model data

.. code-block:: javascript

    {
        "y_acceleration": 0.3002616289666179,
        "pitch": -2.6703138294418745,
        "z_acceleration": -8.096813548880482,
        "temperature": 286.1993964039612,
        "altitude": 300.1070281313986,
        "airspeed": 27.577964685844144,
        "elevator": 0.0,
        "rudder": 0.0,
        "roll_rate": 1.1530883125003415,
        "latitude": 37.92343666537175,
        "total_pressure": 98224.70874839165,
        "roll": 1.0836139829188483,
        "x_acceleration": -2.386305281926219,
        "thrust": -5.207974004747296e-05,
        "dt": 0.0033333333333333335,
        "pitch_rate": -3.238622291356018,
        "yaw_rate": 1.0454829753441017,
        "aileron": 0.0,
        "throttle": 0.0,
        "longitude": 23.922006458085477,
        "time": 1.0033333333333294,
        "heading": 46.01929472213956,
        "static_pressure": 97771.69903080986
    }