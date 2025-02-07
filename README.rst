=======
BusRide
=======


.. image:: https://img.shields.io/pypi/v/messagebus.svg
        :target: https://pypi.python.org/pypi/bus_ride/

.. image:: https://readthedocs.org/projects/bus_ride/badge/?version=latest
        :target: https://bus_ride.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



A simple Message Bus implementation, based on
`Architecture Patterns With Python <https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/>`_
by Harry J.W. Percival And Bob Gregory, published by O’Reilly


To quote:

.. pull-quote::

    Commands capture *intent*. They express our wish for the system to do something. As
    a result, when they fail, the sender needs to receive error information.

    …

    Events capture *facts* about things that happened in the past. Since we don't know
    who's handling an event, senders should not care whether the receivers succeeded or
    failed.



* Free software: MIT
* Documentation: https://bus_ride.readthedocs.io/en/latest


Features
--------

* Commands, Receivers, Events, Handlers, ReturnMessages*.


.. note::

    The purpose fulfilled by the ``ReturnMessage`` class is discussed in the book as an “ugly hack,”
    but acceptable until you are ready to fully embrace Command-Query Responsibility Segregation,
    as discussed in Chapter 12. 😁


Roadmap
-------

* not much actually
* tox to support more Python versions
* maybe some more tests
* maybe some documentation improvements if there is feedback
* fix that one thing ``mypy`` is complaining about


Credits
-------

Based on `Architecture Patterns With Python <https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/>`_
by Harry J.W. Percival And Bob Gregory, published by O’Reilly


This package was initialized with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
