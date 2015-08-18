from setuptools import setup

setup(name="huginn",
      version = '0.0.1',
      description = 'Flight simulator for HITL and SITL simulations',
      author = 'Panagiotis Matigakis',
      author_email = 'pmatigakis@gmail.com',
      scripts=["scripts/huginn_start.py",
               "scripts/huginn_control.py",
               "scripts/huginn_data.py",
               "scripts/huginn_web.py"],
      packages=["huginn"],
      package_data={'huginn': ['data/aircraft/c172p/*.xml',
                               'data/engine/*.xml',
                               'data/scripts/*.xml',
                               'templates/*.html',
                               'static/css/*.css',
                               'static/js/*.js']})