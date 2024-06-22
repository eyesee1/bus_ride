Usage Example
#############


Create your commands, receivers, events, and handlers:

``yourapp/commands/add_item_to_cart.py:``

.. literalinclude:: yourapp/commands/add_item_to_cart.py
   :language: python


``yourapp/events/item_added_to_cart.py:``

.. literalinclude:: yourapp/events/item_added_to_cart.py
   :language: python


``yourapp/views.py:``

.. literalinclude:: yourapp/views.py
   :language: python


.. note::

    We recommend having unit tests which use `mock.patch`_ to make
    sure your receivers and handlers are being called as expected.
    Please see the unit tests of this library for examples.

.. _mock.patch: https://docs.python.org/3/library/unittest.mock.html#patch
