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

Static Type Checking

        # Move to the source directory and
    mypy basic_stats.py
    mypy test_basic_stats.py

Unit Testing

        # Move to the source directory and
    python test_basic_stats.py -v

Display the internal documentation

        # Move to the source directory and
    python -c "import basic_stats as bs; help(bs)"
    python -c "import test_basic_stats as tbs; help(tbs)"


Data Structures
---------------

Because its unmutability, Tuples are better suited for type checking but have
a penalty for frequent updates, as that operation requires reallocation. For
that reason it was selected to use Lists for the more internal containers.
With the proper strategy, that ensures O(1) for access and retrieving
operations and O(n) for maintenance.

Dictionaries, Hash tables and sorting were avoided for synthesized statistics,
as none of them provides O(n) complexity for creation, nor consistent O(1) for
access and retrieving.

Type Checking
-------------

Type checking was enabled with annotated type hints in variables and functions
fingerprints using the **`mypy`** type checker. This provides intrisic static
type checking without needing a supporting package. It was not clear that, for
this project and the simple types used, the **`typing`** package could provide
any advantage.

Error Handling
--------------

Error checking was limited to the input provided by the calling context and
reported with exceptions. That way, the final error reporting mechanism and
severity is kept open to the specific nature of the application, being it a
user interface or a logger service.
