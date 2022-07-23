The WikiRoulette project.
=========================

.. toctree::
   :hidden:
   :maxdepth: 1

   license

This project provides a command-line interface that allows a user to print the
introduction and title of a random article using the
`Wikipedia API <https://en.wikipedia.orga/api/rest_v1/#/>`_ or its equivalent
in another language. The project follows the tutorials from the
`Hypermodern Python <https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769>`_
series of articles.


Installation
____________


To install the WikiRoulette project, run this command in your terminal:

.. code-block:: console

   $ pip install wiki-roulette


Usage
-----

The usage of WikiRoulette looks like:

.. code-block:: console

   $ wiki-roulette [OPTIONS]

.. option:: -l <language>, --language <language>

   The Wikipedia language edition,
   as identified by its subdomain on
   `wikipedia.org <https://www.wikipedia.org/>`_.
   By default, the English Wikipedia is selected.

.. option:: --version

   Display the version and exit.

.. option:: --help

   Display a short usage message and exit


License
=======

.. include:: ../LICENSE
