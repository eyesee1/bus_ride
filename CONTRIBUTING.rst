.. highlight:: shell

============
Contributing
============

Code of Conduct
---------------

- If contributing or participating in this project in any way, including posting issues or feature requests, you are
  expected to abide by
  the [Python Software Foundation's Code of Conduct](https://policies.python.org/python.org/code-of-conduct/).

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/eyesee1/bus_ride/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

BusRide could always use more documentation, whether as part of the
official BusRide docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/eyesee1/bus_ride/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `bus_ride` for local development.

#. Fork the `bus_ride` repo on GitHub.
#. Clone your fork locally::

    $ git clone git@github.com:your_name_here/bus_ride.git

#. Ensure `uv is installed`_.
#. Install dependencies and start your virtualenv::

    $ uv sync --all-groups
    $ source .venv/bin/activate
    $ pre-commit install

#. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

#. When you're done making changes, check that your changes pass the tests::

    $ pytest


#. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitHub website.

.. _uv is installed: https://docs.astral.sh/uv/getting-started/installation/

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests and updates to any affected tests.
2. If the pull request adds functionality, the docs should be updated. Make sure
   your new code has docstrings, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.11 through latest stable release.
   Make sure that the tests pass for all supported Python versions.
4. Code will be linted and formatted using `Ruff`_ by pre-commit.

.. _Ruff: https://docs.astral.sh/ruff/

Tips
----

To run a subset of tests::

$ pytest tests.test_messagebus


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags
$ uv build
$ uv publish
