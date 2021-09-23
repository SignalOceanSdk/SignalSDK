# noqa: D100

from typing import Iterable, Sequence, Union, overload

import pandas as pd  # type: ignore

from ..historical_tonnage_list import Vessel, Column


class TonnageList(Sequence[Vessel]):
    """A collection of vessels representing a tonnage list."""

    def __init__(self, vessels: Iterable[Vessel]):
        """Initializes the tonnage list.

        Args:
            vessels: Vessels in the tonnage list.
        """
        self.__vessels = tuple(vessels)

    @overload
    def __getitem__(self, index: int) -> Vessel:  # noqa: D105
        ...

    @overload
    def __getitem__(self, slice: slice) -> Sequence[Vessel]:  # noqa: D105
        ...

    def __getitem__(
        self, i: Union[int, slice]
    ) -> Union[Vessel, Sequence[Vessel]]:  # noqa: D105
        return self.__vessels.__getitem__(i)

    def __len__(self) -> int:  # noqa: D105
        return self.__vessels.__len__()

    def __repr__(self) -> str:  # noqa: D105
        class_name = self.__class__.__name__
        return f"{class_name}(vessels={self.__vessels!r})"

    def to_data_frame(self) -> pd.DataFrame:
        """Converts the tonnage list to a pandas data frame."""
        vessels_by_imo = {v.imo: Column._create_row(v) for v in self.__vessels}
        data_frame = pd.DataFrame.from_dict(
            vessels_by_imo, orient="index", columns=list(Column)
        )

        return data_frame.astype(Column._get_data_types())
