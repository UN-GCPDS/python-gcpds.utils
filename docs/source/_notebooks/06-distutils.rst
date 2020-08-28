Distutils
=========

This tool launches a command-line application to create a Python package
for the `GCPDS repository <https://github.com/UN-GCPDS>`__, this package
includes a configured `Sphinx
documentation <https://www.sphinx-doc.org/en/master/>`__ environment and
a script example.

Create package
--------------

Move the terminal to desired location and execute ``gcpds_distutils``
command

$ gcpds_distutils

The application will ask about:

.. code:: plain

   > Package name:
   > Author:
   > Author email:
   > Maintainer:
   > Maintainer email: 
   > Requieres (separated by comma):

After that, a new directory with the given ``Package name`` will be
created:

.. code:: plain

   example/  #Package name created
     gcpds/  # Namespace
       dummy/
         # Exmaple scripts
         __init__.py
         dummy.py
         
       example/
         # Put here your main code
         __init__.py
         
     notebooks/
       # Documentation
       01-dummy.ipynb
       readme.ipynb
       
     docs/
       ...
       
     LICENSE.txt  # NO EDIT THIS FILE!
     README.md  # NO EDIT THIS FILE! 
     MANIFEST.in  # NO EDIT THIS FILE!
     setup.py

Add Python scripts
------------------

Add functions
~~~~~~~~~~~~~

This example package was created for be imported like:
``form gcpds import example``, let’s assume that we have a function
called ``super_awesome_function()`` and we want to call it with the
sctructure ``from gcpds.example import super_awesome_function``, then we
must write own function in ``example/gcpds/__init__.py``

.. code:: ipython3

    # example/gcpds/__init__.py
    
    def super_awesome_function(a: int, b: int) -> int:
        """Unnecessary funtion to compute power of a number."""
        
        return a ** b

NOTE: The `Type hint <https://docs.python.org/3/library/typing.html>`__
is not necessary but recommended.

Add classes
~~~~~~~~~~~

The best way to add a class is to write a new script file (avoid adding
classes to ``__inut__.py``)

.. code:: ipython3

    # example/gcpds/my_class.py
    
    class MyClass:
        """"""
    
        def __init__(self):
            """Constructor"""
    
        def super_awesome_function(self, a: int, b: int) -> int:
            """Unnecessary funtion to compute power of a number."""
    
            return a ** b
    
        def super_awesome_function_improved(self, a: float, b: float) -> float:
            """Unnecessary funtion to compute power of a number."""
    
            return a ** b

Then we can import ``MyClass`` with
``from gcpds.example.my_class import MyClass``.

A better structure for call ``MyClass`` could be
``from gcpds.example import MyClass``, for doing this we must edit the
``__init__.py`` file

.. code:: ipython3

    # example/gcpds/__init__.py
    
    from .my_class import MyClass

Add documentation
-----------------

This package is configured to use notebooks as documentation, the
**README** is located in ``notebooks/readme.ipynb``, this file will
compile as the main ``README.md``. Any extra documentation must be added
in this directory as notebooks, these notebooks will be included
alphabetically in the main documentation.

Compile documentation
~~~~~~~~~~~~~~~~~~~~~

In the ``docs`` folder execute:

$ make buildapi html

The documentation will be compiled to ``docs/build/html/index.html``

NOTE: Thi only works on GNU/Linux
