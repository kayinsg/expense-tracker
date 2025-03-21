from typing import TypeAlias

item: TypeAlias = str
dollars: TypeAlias = int | float
categorizedDataTuples: TypeAlias = list[tuple[item, dollars, dollars, dollars]]
