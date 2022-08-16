"""Module to compute Basic Statistics.

This is part of the TeamInternational Python evaluation task.
A typical call sequence would be:

    import basic_stats as bs
    capture = bs.DataCapture()
    capture.add(3)
    capture.add(9)
    capture.add(3)
    capture.add(4)
    capture.add(6)
    stats = capture.build_stats()
    stats.less(4)
    stats.between(3, 6)
    stats.greater(4)
"""

from typing import List, Tuple, TypeVar


class BasicStats:
    """Keep summarized stats for values collected with a DataCapture object."""

    def __init__(self, tot_values: int, values_counters: list[int]) -> None:
        """Constructor, typically called through a DataCapture object."""

        # Each Nth value has a triad stored in <stats> as follows:
        #     Bth-Triad[0]: number of values equal to the Nth value.
        #     Bth-Triad[1]: number of values lesser then the Nth value.
        #     Bth-Triad[2]: number of values greater than the Nth value.
        #
        # <tot> is a helper triad used to compute the triads in <stat>, by
        # memoizing the changes when an additional value is considered to the
        # right. To compute the Nth triad, <tot> should meet the invariant::
        #     tot[0]: number of values equal to previous, at <Nth - 1>.
        #     tot[1]: number of values considered up to <Nth - 1>.
        #     tot[2]: Number of values not yet considered, greater than Nth.
        self.tot: list[int] = [ 0, 0, tot_values ]
        self.stats: list[list[int]] = [ self.__nth_stat(nth_cter) for nth_cter in values_counters ]

    def less(self, val: int) -> int:
        """Return how many values are less than a given value."""
        return self.stats[val][1]

    def greater(self, val: int) -> int:
        """Return how many values are greater than a given value."""
        return self.stats[val][2]

    def between(self, left: int, right: int) -> int:
        """Return how many values are in a range, including boundaries."""
        return self.stats[left][0] + self.stats[left][2] - self.stats[right][2]

    def get_state(self) -> tuple[list[int], list[list[int]]]:
        """Return the current instance state in a tuple."""
        return (self.tot, self.stats)

    def __nth_stat(self, cter: int) -> list[int]:
        """Compute the statistics for a value."""
        tmp = self.tot[0]
        self.tot[0] = cter
        self.tot[1] += tmp
        self.tot[2] -= cter
        return [ self.tot[0], self.tot[1], self.tot[2] ]

    def __str__(self) -> str:
        """Return a string representation of the internal instance state.

        Usage: str( <instance> )
        """
        return f'{type(self).__name__}(id:{id(self)}, ' \
               f'tot:{self.tot}, cters:{self.stats}' \
               f')'


class DataCapture:
    """Collect values to compute basic stats.

    Attributes
    ----------
    __max_val : int
        Maximum positive supported value. You may want to update it.
    """

    __max_val: int = 10

    def __init__(self) -> None:
        """Constructor, prepare the interanal state for quick execution.."""

        # <values_counters> is a vector containing counters for the collected
        # values, allowing quick insertions.
        #
        # <tot_collected> accumulates the number of collected values, avoiding
        # going through <values-counters> to summarize them.
        self.tot_collected: int = 0;
        self.values_counters: list[int] = [0] * (self.__max_val+1)

    def add(self, val: int) -> None:
        """Add another value to the working set."""
        self.tot_collected += 1;
        self.values_counters[val] += 1

    def build_stats(self) -> BasicStats:
        """Build and return the stats for the values collected so far."""
        return BasicStats(self.tot_collected, self.values_counters)

    def get_state(self) -> tuple[int, list[int]]:
        """Return the current instance state in a tuple."""
        return (self.tot_collected, self.values_counters)

    def __len__(self) -> int:
        """Return the working size, i.e., the maximum positive supported value.

        Usage: len( <instance> )
        """
        return self.__max_val

    def __str__(self) -> str:
        """Return a string representation of the internal instance state.

        Usage: str( <instance> )
        """
        return f'{type(self).__name__}(id:{id(self)}, ' \
               f'tot:{self.tot_collected}, cters:{self.values_counters}' \
               f')'
