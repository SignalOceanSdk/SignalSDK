# noqa: D100

from typing import Iterable, Sequence, overload, Union

import pandas as pd  # type: ignore

from .tonnage_list import TonnageList
from .column import Column
from .index_level import IndexLevel


class HistoricalTonnageList(Sequence[TonnageList]):
    """The class that represents a Historical Tonnage List.

    A Historical Tonnage List consists from an collection of Tonnage Lists
    one for every day between the start and end date specified
    when querying the Historica Tonnage List API.
    """

    def __init__(self, tonnage_lists: Iterable[TonnageList]):
        """Initializes the Historical Tonnage List.

        Args:
            tonnage_lists: Tonnage Lists contained within the Historical
                Tonnage List.
        """
        self.__tonnage_lists = tuple(tonnage_lists)

    @overload
    def __getitem__(self, index: int) -> TonnageList:  # noqa: D105
        ...

    @overload
    def __getitem__(self, slice: slice) -> Sequence[TonnageList]:  # noqa: D105
        ...

    def __getitem__(
        self, i: Union[int, slice]
    ) -> Union[TonnageList, Sequence[TonnageList]]:  # noqa: D105
        return self.__tonnage_lists.__getitem__(i)

    def __len__(self) -> int:  # noqa: D105
        return self.__tonnage_lists.__len__()

    def __repr__(self) -> str:  # noqa: D105
        class_name = self.__class__.__name__
        return f"{class_name}(tonnage_lists={self.__tonnage_lists!r})"

    def to_data_frame(self) -> pd.DataFrame:
        """Converts the Historical Tonnage List to a pandas data frame."""
        index_tuples = []
        data = []
        for tonnage_list in self.__tonnage_lists:
            for vessel in tonnage_list.vessels:
                index_tuples.append((tonnage_list.date, vessel.imo))
                data.append(Column._create_row(vessel))

        data_frame = pd.DataFrame(
            data,
            index=pd.MultiIndex.from_tuples(
                index_tuples, names=[IndexLevel.DATE, IndexLevel.IMO]
            ),
            columns=list(Column),
        )

        return data_frame.astype(Column._get_data_types())
