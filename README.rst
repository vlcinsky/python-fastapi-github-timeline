==========================
py-fastapi-github-timeline
==========================
Rewrite of Common Lisp htmx_ app _cl-github-timeline into Python using FastAPI_.

This project tries to prove, that with htmx_, templating of page components (using e.g. jinja2_) becomes more important than the actual framework serving HTTP requests and it shall be relatively easy to rewrite the app from one language/framework to another.

.. image:: cl-github-timeline.gif

Concepts
========
htmx_ based application. Components of page are generated on backend and updated on the page using htmx_ javascript code.

Installation
============
Assuming poetry_ and python 3.9 (3.6+ would work too) is installed::

  $ poetry install

From now on it is assumed commands are run from activated virtual environment::

  $ poetry shell
  (.venv) $

Usage
=====
::

  $ uvicorn app:app --reload --port=8000

or using invoke. First list available commands::

  $ inv -l
  Available tasks:

    app-run   Run web app in development mode

and then run it::

  $ inv app-run


Finally open the web app on http://localhost:8000, enter some existing GitHub user name and click button "Generate Timeline".

.. _htmx: https://htmx.org
.. _poetry: https://python-poetry.org/
.. _jinja2: https://palletsprojects.com/p/jinja/
.. _FastAPI: https://fastapi.tiangolo.com/

.. _cl-github-timeline: https://github.com/fukamachi/ningle
