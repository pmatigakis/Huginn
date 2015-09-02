from setuptools import setup, Extension

jsbsim_wrapper_extension = Extension("_huginn_jsbsim",
                                     include_dirs=["jsbsim_wrapper", 
                                                   "/usr/local/include", 
                                                   "/usr/local/include/JSBSim",
                                                   "/usr/include",
                                                   "/usr/include/JSBSim"],
                                     sources=["huginn_jsbsim.i", 
                                              "jsbsim_wrapper/FGFDMExec.cpp"],
                                     library_dirs=["/usr/local/lib",
                                                   "/usr/lib"],
                                     libraries=["JSBSim"],
                                     swig_opts=['-c++']
                                     )

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
      package_data={'huginn': ['templates/*.html',
                               'static/css/*.css',
                               'static/js/*.js']},
      ext_modules=[jsbsim_wrapper_extension],
      py_modules=["huginn_jsbsim"])