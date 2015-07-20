from setuptools import setup

setup(name="flightsim",
      version = '0.0.1',
      description = 'Flight simulator for Python',
      author = 'Panagiotis Matigakis',
      author_email = 'pmatigakis@gmail.com',
      scripts=["flightsimulator.py",
               "flightsimulator_control.py"],
      packages=["flightsim"],
      package_data={'flightsim': ['data/aircraft/c172p/*.xml',
                                  'data/engine/*.xml',
                                  'data/scripts/*.xml',
                                  'templates/*.html',
                                  'static/css/*.css',
                                  'static/js/*.js']})