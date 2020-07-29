# noqa: D100

from typing import Iterable, Sequence

import pandas as pd

from .tonnage_list import TonnageList
from .column import Column
from .index_level import IndexLevel


class HistoricalTonnageList(Sequence):
    """Represents a Historical Tonnage List.
    
    A Historical Tonnage List contains a Tonnage List for every day between a
    start and end date specified when querying for the Historical Tonnage List.
    """

    def __init__(self, tonnage_lists: Iterable[TonnageList]):
        """Initializes the Historical Tonnage List.
        
        Args:
            tonnage_lists: Tonnage Lists contained within the Historical
                Tonnage List.
        """
        self.__tonnage_lists = tuple(tonnage_lists)

    def __getitem__(self, index):   # noqa: D105
        return self.__tonnage_lists.__getitem__(index)

    def __len__(self):  # noqa: D105
        return self.__tonnage_lists.__len__()

    def __repr__(self): # noqa: D105
        return f'{self.__class__.__name__}(tonnage_lists={self.__tonnage_lists!r})'

    def to_data_frame(self) -> pd.DataFrame:
        """Converts the Historical Tonnage List to a pandas data frame."""
        index_tuples = []
        data = []
        for tonnage_list in self.__tonnage_lists:
            for vessel in tonnage_list.vessels:
                index_tuples.append(
                        (tonnage_list.date.date(), vessel.imo)
                )
                data.append(Column._create_row(vessel))

        data_frame = pd.DataFrame(
            data,
            index=pd.MultiIndex.from_tuples(
                index_tuples,
                names=[IndexLevel.DATE, IndexLevel.IMO]
            ),
            columns=list(Column)
        )

        return data_frame.astype(Column._get_data_types())
