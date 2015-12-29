from os import walk, path, chdir
from distutils.core import setup

def get_package_data():
    chdir("huginn")
    package_data = []
    for dirname, dirnames, filenames in walk("static"):
        for filename in filenames:
            filepath = path.join(dirname, filename)
            package_data.append(filepath)
    
    for dirname, dirnames, filenames in walk("data"):
        for filename in filenames:
            filepath = path.join(dirname, filename)
            package_data.append(filepath)
        
    chdir("..")
    
    return package_data

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
      package_data={'huginn': get_package_data()}
      )
