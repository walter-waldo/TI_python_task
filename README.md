# TI_python_task
TemInternational Python Task

Project Directory Layout
------------------------
    [$PROJECT_DIR]          Any directory, top of the project tree.
    |
    |__basic_stats.py       Python classes.
    |__test_basic_stats.py  Unit test.
    |__README.md            This document.

Setup
-----

Besides the Python interpreter, it is only required an static type checker.

    pip install mypy

Execution
---------

Perform static type checking

        # Move to the source directory and
    mypy basic_stats py
    mypy test_basic_stats py

Perform Unit Testing

        # Move to the source directory and
    python basic_stats. py

Data Structures
---------------

Because its unmutability, Tuples are better suited for type checking but have
a penalty for frequent updates, as that operation requires reallocation. For
that reason it was selected to use Lists for the more internal containers.
With the proper strategy, that ensures O(1) for access and retrieving
operations and O(n) for maintenance.

Dictionaries, Hash tables and sorting were avoided for synthesized statistics,
as none of them provides O(n) complexity for creation, nor consistent O(1) for
retrieving.

Type Checking
-------------
