from setuptools import setup

setup(name="huginn",
      version = '0.0.1',
      description = 'Flight simulator for HITL and SITL simulations',
      author = 'Panagiotis Matigakis',
      author_email = 'pmatigakis@gmail.com',
      scripts=["scripts/huginn_start.py",
               "scripts/huginn_control.py",
               "scripts/huginn_data.py",
               "scripts/huginn_telemetry.py"],
      packages=["huginn"],
      package_data={'huginn': ['static/*.html',
                               'static/css/*.css',
                               'static/js/*.js',
                               'static/images/*.png',
                               'static/fonts/*.eot',
                               'static/fonts/*.woff',
                               'static/fonts/*.svg]',
                               'static/fonts/*.woff2',
                               'static/fonts/*.ttf']}
      )
