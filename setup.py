from os import walk, path, chdir
from setuptools import setup

def get_web_static_files():
    chdir("huginn")
    package_data = []
    for dirname, dirnames, filenames in walk("static"):
        for filename in filenames:
            filepath = path.join(dirname, filename)
            if path.isfile(filepath) and not path.islink(filepath):
                package_data.append(filepath)
    
    chdir("..")
    
    return package_data

def get_jsbsim_data():
    chdir("huginn")
    
    package_data = []

    for dirname, dirnames, filenames in walk("data"):
        for filename in filenames:
            filepath = path.join(dirname, filename)
            if path.isfile(filepath) and not path.islink(filepath):
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
               "scripts/huginn_record.py"],
      packages=["huginn"],
      package_data={'huginn': get_web_static_files() + get_jsbsim_data()},
      install_requires = ["protobuf>=2.6.1",
                          "requests>=2.9.1",
                          "Twisted>=15.5.0"],
      tests_require=["coverage>=4.0.3",
                     "mock>=1.3.0",
                     "nose>=1.3.7",
                     "PyHamcrest>=1.9.0"],
      test_suite="nose.collector",
      zip_safe=False,
      )
