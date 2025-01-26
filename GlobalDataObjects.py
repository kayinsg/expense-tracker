from typing import NamedTuple
from pandas import DataFrame, Series


class Data(NamedTuple):
    table: DataFrame
    summary: Series
