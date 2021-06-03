.. nepse-api documentation master file, created by
   sphinx-quickstart on Thu Jun  3 03:44:40 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nepse-api's documentation!
=====================================

nepse-api is a mordern, easy to use, feature-rich and async ready API wrapper
for NEPSE.

Features
--------
*  Modern Pythonic API using ``async``\/``await`` syntax
*  Easy to use with an object oriented design
*  Optimised for both speed and memory
*  Optional cache for faster data fetching

Getting started
-----------------

Is this your first time using the library? This is the place to get started!

- **First steps:** :ref:`intro <intro>` | :ref:`quickstart <quickstart>`
- **Examples:** Many examples are available in the :resource:`repository <examples>`.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:
   
   ./usage/intro
   ./usage/quickstart
   

.. toctree::
   :maxdepth: 3
   :caption: Core:

   ./modules/core/Client
   ./modules/core/errors
   ./modules/core/utils


.. toctree::
   :maxdepth: 2
   :caption: Modules:
   
   ./modules/nepse.security
   ./modules/nepse.market


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`